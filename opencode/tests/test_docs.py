"""Docs and example config stay in step with what ships — run: python3 -m unittest discover tests"""

import json
import os
import re
import unittest

from test_party_models import REPO

import party_models

README = os.path.join(REPO, "README.md")
EXAMPLE = os.path.join(REPO, "opencode.example.jsonc")
FRAGMENT = os.path.join(REPO, "AGENTS.fragment.md")
INSTALL = os.path.join(REPO, "install.sh")

# The README's role table is the one whose header names this column.
KEY_HEADER = "`party-models.jsonc` key"


def readme_role_rows():
    """{role: (model, effort)} from the README's role table."""
    with open(README, encoding="utf-8") as f:
        lines = f.read().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("|") and KEY_HEADER in l)
    except StopIteration:
        raise AssertionError("README.md has no table with a %r column" % KEY_HEADER)
    header = [c.strip() for c in lines[start].strip("|").split("|")]
    key_col, model_col, effort_col = (header.index(KEY_HEADER), header.index("Model"),
                                      header.index("Effort"))
    rows = {}
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        role = cells[key_col].strip("`")
        rows[role] = (cells[model_col].strip("`"), cells[effort_col].strip("`"))
    return rows


class ReadmeTests(unittest.TestCase):

    def test_role_table_matches_party_models(self):
        shipped = party_models.load_jsonc(os.path.join(REPO, party_models.MASTER))
        want = {role: (e["model"], e.get("effort", "model default"))
                for role, e in shipped.items()}
        self.assertEqual(
            readme_role_rows(), want,
            "README.md's role table must list every role in party-models.jsonc with the same "
            "model and effort (\"model default\" when it has none). Changed a default? "
            "Update the table too.")
        self.assertEqual(set(want), set(party_models.ROLES))

    def test_no_personal_paths(self):
        with open(README, encoding="utf-8") as f:
            text = f.read()
        for needle in ("~/dev/", "/Users/", "opencode-ap"):
            self.assertFalse(needle in text,
                             "README.md is read by strangers; no personal paths (%r)" % needle)


class ExampleConfigTests(unittest.TestCase):

    def setUp(self):
        self.config = party_models.load_jsonc(EXAMPLE)

    def test_build_pin_matches_root_model(self):
        # The TUI seeds a new session from the default (build) agent's model,
        # ahead of the root "model": if they differ, sessions start on the pin.
        self.assertEqual(self.config["agents"]["build"]["model"], self.config["model"])

    def test_openrouter_anthropic_models_turn_on_caching(self):
        # OpenCode adds no cache breakpoints on OpenRouter routes; without
        # cache_control an Anthropic model there never caches (every turn full price).
        defined = self.config["providers"]["openrouter"]["models"]
        used = {a["model"].split("#")[0] for a in self.config["agents"].values()}
        used.add(self.config["model"])
        anthropic = sorted(m[len("openrouter/"):] for m in used
                           if m.startswith("openrouter/anthropic/"))
        self.assertTrue(anthropic, "expected the helpers on an openrouter/anthropic model")
        for mid in anthropic:
            self.assertEqual(defined.get(mid, {}).get("settings", {}).get("cache_control"),
                             {"type": "ephemeral"}, mid)


class FragmentTests(unittest.TestCase):

    def test_markers_match_install_sh(self):
        # install.sh strips an old block by these exact strings; changing them
        # in the fragment would leave a duplicate block in existing installs.
        with open(INSTALL, encoding="utf-8") as f:
            sh = f.read()
        begin = re.search(r'^MARK_BEGIN="(.*)"$', sh, re.M).group(1)
        end = re.search(r'^MARK_END="(.*)"$', sh, re.M).group(1)
        with open(FRAGMENT, encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
        self.assertTrue(lines[0].startswith(begin), lines[0])
        self.assertEqual(lines[-1], end)


if __name__ == "__main__":
    unittest.main()
