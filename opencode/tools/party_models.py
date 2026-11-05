#!/usr/bin/env python3
"""Render each party role's model into its agent/command file.

Reads party-models.jsonc (the shipped defaults) and, if present,
party-models.local.jsonc (the user's overrides), checks every role against
OpenCode's model catalog, and writes copies of the six agent/command files to
.generated/{agents,commands}/ with the frontmatter `model:` line replaced.

    python3 tools/party_models.py              render, checking against OpenCode
    python3 tools/party_models.py --no-check   render without the catalog check

PARTY_MODEL_CATALOG=<file> reads the catalog from a saved copy of
`opencode api get /api/model` instead of asking OpenCode (used by the tests).

Exit 0 on success (a catalog that can't be reached only warns), 1 on any
error in the models files, the catalog check or the source files.

Stdlib only, and keep it Python 3.9-compatible: macOS's /usr/bin/python3 is
3.9 and is often first on PATH when install.sh runs.
"""

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

MASTER = "party-models.jsonc"
LOCAL = "party-models.local.jsonc"
OUT_DIR = ".generated"
CATALOG_ENV = "PARTY_MODEL_CATALOG"
CATALOG_CMD = ["opencode", "api", "get", "/api/model"]
CATALOG_TIMEOUT = 60  # seconds

# role -> source file, relative to the repo root.
ROLES = {
    "guide": "commands/party.md",
    "planner": "commands/plan.md",
    "long-rest": "commands/long-rest.md",
    "fighter": "agents/fighter.md",
    "cleric": "agents/cleric.md",
    "wizard": "agents/wizard.md",
}
ENTRY_KEYS = ("model", "effort")

MODEL_LINE = re.compile(r"^model:[^\r\n]*", re.MULTILINE)


class PartyModelsError(Exception):
    """A problem the user has to fix; the message says what and where."""


# ── JSONC ────────────────────────────────────────────────────────────────────

def strip_jsonc(text):
    """Remove // and /* */ comments and trailing commas, outside strings.

    String contents pass through untouched, so model IDs ("~deepseek/…") and
    URLs inside strings survive. Newlines inside block comments are kept so
    json's error line numbers still match the file.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"':
                    break
                j += 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            end = n if j < 0 else j + 2
            out.append("\n" * text.count("\n", i, end))
            i = end
        elif c in "]}":
            # Drop a trailing comma: the last non-space thing we emitted.
            k = len(out) - 1
            while k >= 0 and (not out[k] or out[k].isspace()):
                k -= 1
            if k >= 0 and out[k] == ",":
                out[k] = ""
            out.append(c)
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def load_jsonc(path):
    with open(path, encoding="utf-8") as f:
        text = strip_jsonc(f.read())
    if not text.strip():
        return {}
    try:
        data = json.loads(text)
    except ValueError as e:
        raise PartyModelsError("%s: not valid JSON: %s" % (path, e))
    if not isinstance(data, dict):
        raise PartyModelsError("%s: must be one { … } object of roles" % path)
    return data


# ── Models files ─────────────────────────────────────────────────────────────

def _check_entry(path, role, entry):
    where = "%s: %s" % (path, role)
    if not isinstance(entry, dict):
        raise PartyModelsError('%s: must be an object like { "model": "provider/model" }' % where)
    extra = sorted(set(entry) - set(ENTRY_KEYS))
    if extra:
        raise PartyModelsError("%s: unknown field %s (fields: model, effort)"
                               % (where, ", ".join(repr(k) for k in extra)))
    model = entry.get("model")
    if not isinstance(model, str) or not model.strip():
        raise PartyModelsError('%s: needs "model": "provider/model-id"' % where)
    if model != model.strip() or any(ch.isspace() for ch in model):
        raise PartyModelsError("%s: model %r contains spaces" % (where, model))
    if "#" in model:
        raise PartyModelsError('%s: model %r contains "#"; put the part after "#" in "effort"'
                               % (where, model))
    if "effort" in entry:
        effort = entry["effort"]
        if not isinstance(effort, str) or not effort or any(ch.isspace() for ch in effort) \
                or "#" in effort:
            raise PartyModelsError("%s: effort %r must be one variant name, e.g. \"high\""
                                   % (where, effort))


def load_models(root):
    """Return {role: {"model": ..., ["effort": ...]}} for every role.

    A role listed in the .local file replaces the master's whole entry: effort
    names belong to one model, so a new model must never inherit the old
    effort.
    """
    master_path = os.path.join(root, MASTER)
    if not os.path.exists(master_path):
        raise PartyModelsError("%s: not found" % master_path)
    master = load_jsonc(master_path)
    for role in ROLES:
        if role not in master:
            raise PartyModelsError("%s: missing role %r" % (master_path, role))
    for role, entry in master.items():
        if role not in ROLES:
            raise PartyModelsError("%s: unknown role %r (roles: %s)"
                                   % (master_path, role, ", ".join(ROLES)))
        _check_entry(master_path, role, entry)

    models = {role: dict(master[role]) for role in ROLES}

    local_path = os.path.join(root, LOCAL)
    if os.path.exists(local_path):
        local = load_jsonc(local_path)
        for role, entry in local.items():
            if role not in ROLES:
                hint = difflib.get_close_matches(role, ROLES, n=1)
                raise PartyModelsError("%s: unknown role %r%s (roles: %s)"
                                       % (local_path, role,
                                          " — did you mean %r?" % hint[0] if hint else "",
                                          ", ".join(ROLES)))
            _check_entry(local_path, role, entry)
            models[role] = dict(entry)
    return models


def model_value(entry):
    """The frontmatter value: `model` or `model#effort`."""
    if "effort" in entry:
        return "%s#%s" % (entry["model"], entry["effort"])
    return entry["model"]


# ── Catalog ──────────────────────────────────────────────────────────────────

def parse_catalog(text):
    """{ "provider/model": [variant ids] } from `opencode api get /api/model` output."""
    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get("data")
    if not isinstance(data, list):
        raise ValueError("expected a list of models under \"data\"")
    catalog = {}
    for m in data:
        if not isinstance(m, dict) or "providerID" not in m or "id" not in m:
            continue
        variants = [v["id"] for v in (m.get("variants") or [])
                    if isinstance(v, dict) and "id" in v]
        catalog["%s/%s" % (m["providerID"], m["id"])] = variants
    if not catalog:
        raise ValueError("no models in the list")
    return catalog


def load_catalog():
    """Return (catalog, None), or (None, reason) when it can't be had."""
    path = os.environ.get(CATALOG_ENV)
    if path:
        source = path
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            return None, "%s: %s" % (source, e.strerror or e)
    else:
        source = "`%s`" % " ".join(CATALOG_CMD)
        # stdout goes to a file, not a pipe: opencode 2.0.20 cuts `api get`
        # output off at 256 KiB on a pipe, and the catalog is ~290 KB.
        with tempfile.TemporaryFile() as out:
            try:
                proc = subprocess.run(CATALOG_CMD, stdout=out, stderr=subprocess.PIPE,
                                      stdin=subprocess.DEVNULL, timeout=CATALOG_TIMEOUT)
            except FileNotFoundError:
                return None, "opencode is not on PATH"
            except subprocess.TimeoutExpired:
                return None, "%s timed out after %ds" % (source, CATALOG_TIMEOUT)
            except OSError as e:
                return None, "%s: %s" % (source, e)
            if proc.returncode != 0:
                err = proc.stderr.decode("utf-8", "replace").strip().splitlines()
                return None, "%s exited %d%s" % (source, proc.returncode,
                                                  ": " + err[-1] if err else "")
            out.seek(0)
            text = out.read().decode("utf-8", "replace")
    try:
        return parse_catalog(text), None
    except ValueError as e:
        return None, "%s: unreadable model list (%s)" % (source, e)


def check_models(models, catalog):
    """Return a list of error messages, one per role that doesn't resolve."""
    errors = []
    for role, entry in models.items():
        model = entry["model"]
        if model not in catalog:
            near = difflib.get_close_matches(model, list(catalog), n=3, cutoff=0.6)
            msg = "%s: model %s is not in OpenCode's model list." % (role, model)
            if near:
                msg += " Close matches: %s." % ", ".join(near)
            msg += " See `opencode api get /api/model`."
            errors.append(msg)
            continue
        effort = entry.get("effort")
        if effort is None:
            continue
        variants = catalog[model]
        if effort not in variants:
            if variants:
                errors.append("%s: model %s has no effort %r. Its variants: %s."
                              % (role, model, effort, ", ".join(variants)))
            else:
                errors.append("%s: model %s has no effort %r. It has no variants; "
                              "leave \"effort\" out." % (role, model, effort))
    return errors


# ── Rendering ────────────────────────────────────────────────────────────────

def replace_model_line(text, value, path):
    """Replace the frontmatter's top-level `model:` line; the body is untouched."""
    m = re.match(r"---\r?\n", text)
    if not m:
        raise PartyModelsError("%s: no frontmatter (file must start with ---)" % path)
    close = re.compile(r"^---[ \t]*\r?$", re.MULTILINE).search(text, m.end())
    if not close:
        raise PartyModelsError("%s: frontmatter has no closing ---" % path)
    front = text[m.end():close.start()]
    lines = MODEL_LINE.findall(front)
    if len(lines) != 1:
        raise PartyModelsError("%s: frontmatter needs exactly one `model:` line, found %d"
                               % (path, len(lines)))
    front = MODEL_LINE.sub(lambda _: "model: " + value, front)
    return text[:m.end()] + front + text[close.start():]


def render(root, models):
    """Write .generated/<dir>/<name>.md for every role; return [(path, value)].

    Every file is prepared before any is written, so a bad source file leaves
    the previous render intact.
    """
    out = []
    for role, rel in ROLES.items():
        src = os.path.join(root, rel)
        try:
            with open(src, encoding="utf-8", newline="") as f:
                text = f.read()
        except OSError as e:
            raise PartyModelsError("%s: %s" % (src, e.strerror or e))
        value = model_value(models[role])
        out.append((os.path.join(root, OUT_DIR, rel), replace_model_line(text, value, src), value))
    for dest, text, _ in out:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = dest + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, dest)
    return [(dest, value) for dest, _, value in out]


# ── CLI ──────────────────────────────────────────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--no-check", action="store_true",
                    help="skip checking models and efforts against OpenCode's model list")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="party repo root (default: this script's repo)")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)

    try:
        models = load_models(root)
        if not args.no_check:
            catalog, why = load_catalog()
            if catalog is None:
                print("party-models: warning: couldn't verify models against OpenCode (%s); "
                      "rendering unchecked." % why, file=sys.stderr)
            else:
                errors = check_models(models, catalog)
                if errors:
                    for e in errors:
                        print("party-models: " + e, file=sys.stderr)
                    print("party-models: fix %s (or %s) and run again; nothing was rendered."
                          % (LOCAL, MASTER), file=sys.stderr)
                    return 1
        written = render(root, models)
    except PartyModelsError as e:
        print("party-models: %s" % e, file=sys.stderr)
        return 1

    for dest, value in written:
        print("rendered %s  model: %s" % (os.path.relpath(dest, root), value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
