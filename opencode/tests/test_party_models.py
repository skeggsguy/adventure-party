"""Tests for tools/party_models.py — run: python3 -m unittest discover tests"""

import contextlib
import io
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "tools", "party_models.py")
sys.path.insert(0, os.path.join(REPO, "tools"))
import party_models  # noqa: E402

# The shipped defaults as the renderer must write them.
SHIPPED = {
    "commands/party.md": "openrouter/qwen/qwen3.8-flash#high",
    "commands/plan.md": "openrouter/xiaomi/mimo-v2.6-pro",
    "commands/long-rest.md": "openrouter/qwen/qwen3.8-flash#high",
    "agents/fighter.md": "openrouter/qwen/qwen3.8-flash#high",
    "agents/cleric.md": "openrouter/~deepseek/deepseek-flash-latest#high",
    "agents/wizard.md": "openrouter/xiaomi/mimo-v2.6-pro",
}

# A small catalog in the shape `opencode api get /api/model` returns.
FAKE_MODELS = [
    ("openrouter", "qwen/qwen3.8-flash", ["none", "high", "max"]),
    ("openrouter", "~deepseek/deepseek-flash-latest", ["none", "low", "high", "max"]),
    ("openrouter", "xiaomi/mimo-v2.6-pro", ["none", "thinking"]),
    ("local", "qwen-flash-next", ["fast", "deep"]),
    ("local", "plain", []),
]


def catalog_json(models=FAKE_MODELS):
    return json.dumps({
        "location": "test",
        "data": [{"id": mid, "modelID": mid, "providerID": prov, "name": mid,
                  "settings": {"baseURL": "https://example.invalid/v1"},
                  "variants": [{"id": v, "settings": {}} for v in variants]}
                 for prov, mid, variants in models],
    })


def frontmatter_model(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    front = text.split("---", 2)[1]
    return [l for l in front.splitlines() if l.startswith("model:")]


class Fixture(unittest.TestCase):
    """A temp copy of the repo's real models file and agent/command sources."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="party-models-test-")
        self.addCleanup(shutil.rmtree, self.tmp)
        self.root = os.path.join(self.tmp, "repo")
        os.makedirs(self.root)
        shutil.copy(os.path.join(REPO, party_models.MASTER), self.root)
        for rel in party_models.ROLES.values():
            os.makedirs(os.path.join(self.root, os.path.dirname(rel)), exist_ok=True)
            shutil.copy(os.path.join(REPO, rel), os.path.join(self.root, rel))
        self.catalog = os.path.join(self.tmp, "catalog.json")
        self.write(self.catalog, catalog_json())

    def write(self, path, text):
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)

    def write_local(self, text):
        self.write(os.path.join(self.root, party_models.LOCAL), text)

    def gen(self, rel):
        return os.path.join(self.root, party_models.OUT_DIR, rel)

    def run_main(self, *args, catalog=None):
        """Run main() in-process; return (exit code, stdout, stderr)."""
        env = {party_models.CATALOG_ENV: catalog or self.catalog}
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, env), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = party_models.main(["--root", self.root] + list(args))
        return code, out.getvalue(), err.getvalue()

    def assert_nothing_rendered(self):
        self.assertFalse(os.path.exists(os.path.join(self.root, party_models.OUT_DIR)),
                         "a failed run must not write .generated/")


class RenderTests(Fixture):

    def test_defaults_render(self):
        code, out, err = self.run_main()
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        for rel, value in SHIPPED.items():
            self.assertEqual(frontmatter_model(self.gen(rel)), ["model: " + value], rel)
            self.assertIn("model: " + value, out)

    def test_only_the_model_line_changes(self):
        code, _, err = self.run_main()
        self.assertEqual(code, 0, err)
        for rel in party_models.ROLES.values():
            with open(os.path.join(self.root, rel), encoding="utf-8") as f:
                src = f.read().splitlines(True)
            with open(self.gen(rel), encoding="utf-8") as f:
                dst = f.read().splitlines(True)
            self.assertEqual(len(src), len(dst), rel)
            diff = [(a, b) for a, b in zip(src, dst) if a != b]
            self.assertLessEqual(len(diff), 1, rel)
            for a, b in diff:
                self.assertTrue(a.startswith("model:") and b.startswith("model:"), (a, b))

    def test_local_replaces_whole_role_dropping_old_effort(self):
        self.write_local('{ "fighter": { "model": "local/qwen-flash-next" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 0, err)
        self.assertEqual(frontmatter_model(self.gen("agents/fighter.md")),
                         ["model: local/qwen-flash-next"])
        # Roles the .local file leaves out keep the shipped value.
        for rel, value in SHIPPED.items():
            if rel != "agents/fighter.md":
                self.assertEqual(frontmatter_model(self.gen(rel)), ["model: " + value], rel)

    def test_local_with_effort(self):
        self.write_local('// mine\n{ "guide": { "model": "local/qwen-flash-next", "effort": "deep" }, }\n')
        code, _, err = self.run_main()
        self.assertEqual(code, 0, err)
        self.assertEqual(frontmatter_model(self.gen("commands/party.md")),
                         ["model: local/qwen-flash-next#deep"])

    def test_local_with_only_comments_changes_nothing(self):
        self.write_local("// { \"fighter\": { \"model\": \"local/x\" } }\n")
        code, _, err = self.run_main()
        self.assertEqual(code, 0, err)
        self.assertEqual(frontmatter_model(self.gen("agents/fighter.md")),
                         ["model: " + SHIPPED["agents/fighter.md"]])

    def test_unknown_role_in_local_fails(self):
        self.write_local('{ "figher": { "model": "local/qwen-flash-next" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("'figher'", err)
        self.assertIn("did you mean 'fighter'", err)
        self.assertIn("guide, planner, long-rest, fighter, cleric, wizard", err)
        self.assert_nothing_rendered()

    def test_unknown_model_fails(self):
        self.write_local('{ "cleric": { "model": "openrouter/qwen/qwen3.8-flsh", "effort": "high" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("cleric: model openrouter/qwen/qwen3.8-flsh is not in OpenCode's model list", err)
        self.assertIn("Close matches: openrouter/qwen/qwen3.8-flash", err)
        self.assert_nothing_rendered()

    def test_unknown_effort_fails_listing_variants(self):
        self.write_local('{ "fighter": { "model": "openrouter/qwen/qwen3.8-flash", "effort": "deep" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("fighter: model openrouter/qwen/qwen3.8-flash has no effort 'deep'. "
                      "Its variants: none, high, max.", err)
        self.assert_nothing_rendered()

    def test_effort_on_model_without_variants_fails(self):
        self.write_local('{ "wizard": { "model": "local/plain", "effort": "high" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("wizard: model local/plain has no effort 'high'. It has no variants", err)
        self.assert_nothing_rendered()

    def test_every_bad_role_is_reported(self):
        self.write_local('{ "fighter": { "model": "openrouter/qwen/qwen3.8-flash", "effort": "deep" },'
                         '  "cleric": { "model": "nope/nope" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("fighter:", err)
        self.assertIn("cleric:", err)

    def test_missing_catalog_only_warns(self):
        code, _, err = self.run_main(catalog=os.path.join(self.tmp, "no-such-catalog.json"))
        self.assertEqual(code, 0, err)
        self.assertIn("couldn't verify", err)
        self.assertEqual(frontmatter_model(self.gen("agents/cleric.md")),
                         ["model: " + SHIPPED["agents/cleric.md"]])

    def test_garbage_catalog_only_warns(self):
        self.write(self.catalog, "<html>not json</html>")
        code, _, err = self.run_main()
        self.assertEqual(code, 0, err)
        self.assertIn("couldn't verify", err)

    def test_no_check_skips_the_catalog(self):
        self.write_local('{ "fighter": { "model": "nope/nope", "effort": "whatever" } }')
        code, _, err = self.run_main("--no-check")
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertEqual(frontmatter_model(self.gen("agents/fighter.md")),
                         ["model: nope/nope#whatever"])

    def test_unknown_field_in_entry_fails(self):
        self.write_local('{ "fighter": { "model": "openrouter/qwen/qwen3.8-flash", "efort": "max" } }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("unknown field 'efort'", err)
        self.assert_nothing_rendered()

    def test_effort_inside_model_id_fails(self):
        self.write_local('{ "fighter": { "model": "openrouter/qwen/qwen3.8-flash#max" } }')
        code, _, err = self.run_main("--no-check")
        self.assertEqual(code, 1)
        self.assertIn('put the part after "#" in "effort"', err)

    def test_master_missing_a_role_fails(self):
        master = os.path.join(self.root, party_models.MASTER)
        with open(master, encoding="utf-8") as f:
            text = f.read()
        self.write(master, text.replace('"wizard":', '"wizzard":'))
        code, _, err = self.run_main("--no-check")
        self.assertEqual(code, 1)
        self.assertIn("missing role 'wizard'", err)

    def test_invalid_local_json_names_the_file(self):
        self.write_local('{ "fighter": { "model": "local/qwen-flash-next" }')
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn(party_models.LOCAL, err)
        self.assertIn("not valid JSON", err)

    def test_rerender_overwrites(self):
        self.assertEqual(self.run_main()[0], 0)
        self.write_local('{ "cleric": { "model": "local/qwen-flash-next", "effort": "fast" } }')
        self.assertEqual(self.run_main()[0], 0)
        self.assertEqual(frontmatter_model(self.gen("agents/cleric.md")),
                         ["model: local/qwen-flash-next#fast"])


    def test_bad_source_file_leaves_previous_render_intact(self):
        self.assertEqual(self.run_main()[0], 0)
        self.write_local('{ "guide": { "model": "local/qwen-flash-next" } }')
        wizard = os.path.join(self.root, "agents/wizard.md")  # last role rendered
        with open(wizard, encoding="utf-8") as f:
            text = f.read()
        self.write(wizard, text.replace("\nmodel:", "\nmodle:"))
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("wizard.md: frontmatter needs exactly one `model:` line, found 0", err)
        self.assertEqual(frontmatter_model(self.gen("commands/party.md")),
                         ["model: " + SHIPPED["commands/party.md"]],
                         "a failed render must not half-update .generated/")


class DefaultCatalogTests(Fixture):
    """The default catalog source: the real script, with `opencode` from PATH."""

    def run_script(self, fake_opencode=None):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir, exist_ok=True)
        if fake_opencode is not None:
            path = os.path.join(bindir, "opencode")
            self.write(path, fake_opencode)
            os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
        env = {k: v for k, v in os.environ.items() if k != party_models.CATALOG_ENV}
        env["PATH"] = bindir + os.pathsep + "/bin:/usr/bin"
        if fake_opencode is None:
            env["PATH"] = bindir  # no opencode anywhere
        return subprocess.run([sys.executable, SCRIPT, "--root", self.root],
                              env=env, capture_output=True, text=True, timeout=60)

    def test_reads_opencode_api_output_in_full(self):
        # opencode 2.0.20 cuts `api get` output at 256 KiB when stdout is a
        # pipe (complete when it's a file); the live catalog is ~290 KB. The
        # fake reproduces that, so reading through a pipe fails this test.
        filler = [("openrouter", "filler/model-%04d-%s" % (i, "x" * 400), ["low", "high"])
                  for i in range(4000)]
        big = os.path.join(self.tmp, "big.json")
        self.write(big, catalog_json(filler + FAKE_MODELS))
        self.assertGreater(os.path.getsize(big), 1000000)
        script = ('#!/bin/sh\n[ "$*" = "api get /api/model" ] || exit 9\n'
                  'if [ -p /dev/stdout ]; then head -c 262144 "%s"; else cat "%s"; fi\n'
                  % (big, big))
        proc = self.run_script(script)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "", "opencode's output was read truncated")
        self.assertEqual(frontmatter_model(self.gen("agents/cleric.md")),
                         ["model: " + SHIPPED["agents/cleric.md"]])

    def test_default_catalog_catches_bad_effort(self):
        self.write_local('{ "fighter": { "model": "openrouter/qwen/qwen3.8-flash", "effort": "deep" } }')
        proc = self.run_script('#!/bin/sh\ncat "%s"\n' % self.catalog)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Its variants: none, high, max", proc.stderr)

    def test_opencode_not_installed_only_warns(self):
        proc = self.run_script(None)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("couldn't verify", proc.stderr)
        self.assertIn("not on PATH", proc.stderr)

    def test_opencode_not_running_only_warns(self):
        proc = self.run_script('#!/bin/sh\necho "connection refused" >&2\nexit 1\n')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("couldn't verify", proc.stderr)
        self.assertIn("connection refused", proc.stderr)


class FrontmatterTests(unittest.TestCase):

    def test_body_model_lines_untouched(self):
        text = "---\nmode: subagent\nmodel: old\n---\nmodel: in the body stays\n"
        self.assertEqual(party_models.replace_model_line(text, "new#high", "f.md"),
                         "---\nmode: subagent\nmodel: new#high\n---\nmodel: in the body stays\n")

    def test_nested_model_key_is_not_the_model_line(self):
        text = "---\nopts:\n  model: nested\nmodel: old\n---\n"
        self.assertEqual(party_models.replace_model_line(text, "new", "f.md"),
                         "---\nopts:\n  model: nested\nmodel: new\n---\n")

    def test_crlf_preserved(self):
        text = "---\r\nmodel: old\r\nagent: build\r\n---\r\nbody\r\n"
        self.assertEqual(party_models.replace_model_line(text, "new", "f.md"),
                         "---\r\nmodel: new\r\nagent: build\r\n---\r\nbody\r\n")

    def test_missing_or_duplicate_model_line_fails(self):
        for text in ("---\nagent: build\n---\n", "---\nmodel: a\nmodel: b\n---\n",
                     "no frontmatter\nmodel: x\n", "---\nmodel: a\n"):
            with self.assertRaises(party_models.PartyModelsError, msg=text):
                party_models.replace_model_line(text, "new", "f.md")


class JsoncTests(unittest.TestCase):

    def parse(self, text):
        return json.loads(party_models.strip_jsonc(text))

    def test_slashes_inside_strings_survive(self):
        text = ('// see https://openrouter.ai/models\n'
                '{ "a": "openrouter/~deepseek/deepseek-flash-latest", // trailing\n'
                '  "b": "https://x.example//y", "c": "/* not a comment */" }')
        self.assertEqual(self.parse(text), {
            "a": "openrouter/~deepseek/deepseek-flash-latest",
            "b": "https://x.example//y", "c": "/* not a comment */"})

    def test_escaped_quote_does_not_end_string(self):
        self.assertEqual(self.parse(r'{"a": "x\" // y", "b": "\\"} // z'),
                         {"a": 'x" // y', "b": "\\"})

    def test_block_comments_and_trailing_commas(self):
        text = '{ /* one\n two */ "a": [1, 2, /* x */ ], "b": {"c": 1,}, }'
        self.assertEqual(self.parse(text), {"a": [1, 2], "b": {"c": 1}})

    def test_block_comment_keeps_line_numbers(self):
        stripped = party_models.strip_jsonc('/* a\nb\nc */ {"x": 1}')
        self.assertEqual(stripped.count("\n"), 2)

    def test_generated_documents_round_trip(self):
        # Invariant: commenting every line of a JSON document, with string
        # values full of comment-like text, never changes what it parses to.
        rng = random.Random(1106)
        alphabet = ['/', '/', '*', '"', '\\', '~', '#', ',', ']', '}', ' ', 'a', ':', '\n']

        def rand_str():
            return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))

        def rand_value(depth=0):
            kind = rng.randint(0, 5 if depth < 3 else 2)
            if kind == 0:
                return rand_str()
            if kind == 1:
                return rng.randint(-5, 5)
            if kind == 2:
                return rng.choice([True, False, None])
            if kind == 3:
                return [rand_value(depth + 1) for _ in range(rng.randint(0, 4))]
            return {rand_str(): rand_value(depth + 1) for _ in range(rng.randint(0, 4))}

        for _ in range(500):
            doc = {rand_str(): rand_value() for _ in range(rng.randint(1, 5))}
            lines = json.dumps(doc, indent=2).splitlines()
            commented = "\n".join(
                l + rng.choice(["", " // " + rand_str().replace("\n", ""),
                                " /* " + rand_str().replace("*", "") + " */"])
                for l in lines)
            self.assertEqual(self.parse(commented), doc, commented)


class ShippedFileTests(unittest.TestCase):

    def test_shipped_file_covers_every_role(self):
        models = party_models.load_jsonc(os.path.join(REPO, party_models.MASTER))
        self.assertEqual(sorted(models), sorted(party_models.ROLES))


if __name__ == "__main__":
    unittest.main()
