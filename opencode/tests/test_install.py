"""Tests for install.sh — run: python3 -m unittest discover tests

Each test installs a temp copy of the repo into a temp OPENCODE_CONFIG_DIR,
with PARTY_MODEL_CATALOG pointing at a fake catalog, so nothing touches the
real ~/.config/opencode or asks a running OpenCode.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

from test_party_models import REPO, SHIPPED, catalog_json, frontmatter_model

import party_models

COPY = ["install.sh", "AGENTS.fragment.md", party_models.MASTER, "tools", "agents",
        "commands", "skills"]


class InstallTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="party-install-test-")
        self.addCleanup(shutil.rmtree, self.tmp)
        self.root = os.path.join(self.tmp, "repo")
        os.makedirs(self.root)
        for name in COPY:
            src = os.path.join(REPO, name)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(self.root, name),
                                ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(src, self.root)
        self.dest = os.path.join(self.tmp, "config")
        self.catalog = os.path.join(self.tmp, "catalog.json")
        with open(self.catalog, "w", encoding="utf-8") as f:
            f.write(catalog_json())

    def install(self, *args):
        env = dict(os.environ, OPENCODE_CONFIG_DIR=self.dest,
                   **{party_models.CATALOG_ENV: self.catalog})
        p = subprocess.run(["sh", os.path.join(self.root, "install.sh")] + list(args),
                           env=env, cwd=self.tmp, capture_output=True, text=True)
        return p.returncode, p.stdout, p.stderr

    def write_local(self, text):
        with open(os.path.join(self.root, party_models.LOCAL), "w", encoding="utf-8") as f:
            f.write(text)

    def assert_dest_untouched(self):
        self.assertFalse(os.path.exists(self.dest),
                         "install.sh must stop before creating anything in the config dir")

    def test_links_generated_files_with_shipped_models(self):
        code, out, err = self.install()
        self.assertEqual(code, 0, err)
        for rel, value in SHIPPED.items():
            link = os.path.join(self.dest, rel)
            self.assertTrue(os.path.islink(link), rel)
            self.assertEqual(os.readlink(link),
                             os.path.join(self.root, party_models.OUT_DIR, rel),
                             "%s must link the rendered copy, not the source" % rel)
            self.assertEqual(frontmatter_model(link), ["model: " + value], rel)
        for skill in ("party-run", "session-zero"):
            self.assertEqual(os.readlink(os.path.join(self.dest, "skills", skill)),
                             os.path.join(self.root, "skills", skill))
        with open(os.path.join(self.dest, "AGENTS.md"), encoding="utf-8") as f:
            self.assertIn("BEGIN adventure-party", f.read())

    def test_local_override_reaches_the_installed_file(self):
        self.write_local('{ "fighter": { "model": "local/qwen-flash-next", "effort": "deep" } }')
        code, out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertEqual(frontmatter_model(os.path.join(self.dest, "agents/fighter.md")),
                         ["model: local/qwen-flash-next#deep"])

    def test_bad_model_aborts_before_installing(self):
        self.write_local('{ "fighter": { "model": "openrouter/qwen/qwen3.8-flash", "effort": "deep" } }')
        code, out, err = self.install()
        self.assertEqual(code, 1, out + err)
        self.assertIn("fighter: model openrouter/qwen/qwen3.8-flash has no effort 'deep'", err)
        self.assertIn("nothing was installed", err)
        self.assert_dest_untouched()

    def test_bad_model_keeps_an_existing_install(self):
        code, _, err = self.install()
        self.assertEqual(code, 0, err)
        self.write_local('{ "cleric": { "model": "nope/nope" } }')
        code, out, err = self.install()
        self.assertEqual(code, 1, out + err)
        self.assertEqual(frontmatter_model(os.path.join(self.dest, "agents/cleric.md")),
                         ["model: " + SHIPPED["agents/cleric.md"]])

    def test_no_check_is_passed_to_the_renderer(self):
        self.write_local('{ "cleric": { "model": "nope/nope", "effort": "whatever" } }')
        code, out, err = self.install("--no-check")
        self.assertEqual(code, 0, err)
        self.assertEqual(frontmatter_model(os.path.join(self.dest, "agents/cleric.md")),
                         ["model: nope/nope#whatever"])

    def test_unknown_argument_installs_nothing(self):
        code, out, err = self.install("--nocheck")
        self.assertEqual(code, 2, out + err)
        self.assertIn("usage:", err)
        self.assert_dest_untouched()
        self.assertFalse(os.path.exists(os.path.join(self.root, party_models.OUT_DIR)))

    def test_reinstall_repoints_links_from_the_sources(self):
        # Installs before the models file linked agents/*.md and commands/*.md
        # straight from the repo; a re-run must move them to .generated/.
        for rel in SHIPPED:
            os.makedirs(os.path.join(self.dest, os.path.dirname(rel)), exist_ok=True)
            os.symlink(os.path.join(self.root, rel), os.path.join(self.dest, rel))
        code, _, err = self.install()
        self.assertEqual(code, 0, err)
        for rel in SHIPPED:
            self.assertEqual(os.readlink(os.path.join(self.dest, rel)),
                             os.path.join(self.root, party_models.OUT_DIR, rel), rel)

    def test_stale_generated_file_is_not_linked(self):
        stale = os.path.join(self.root, party_models.OUT_DIR, "agents")
        os.makedirs(stale)
        with open(os.path.join(stale, "retired.md"), "w") as f:
            f.write("---\nmodel: x\n---\n")
        code, _, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertFalse(os.path.lexists(os.path.join(self.dest, "agents", "retired.md")),
                         "install.sh must link only rendered copies of current sources")

    def test_uninstall_removes_the_links(self):
        code, _, err = self.install()
        self.assertEqual(code, 0, err)
        code, out, err = self.install("--uninstall")
        self.assertEqual(code, 0, err)
        for rel in SHIPPED:
            self.assertFalse(os.path.lexists(os.path.join(self.dest, rel)), rel)
        for skill in ("party-run", "session-zero"):
            self.assertFalse(os.path.lexists(os.path.join(self.dest, "skills", skill)))
        with open(os.path.join(self.dest, "AGENTS.md"), encoding="utf-8") as f:
            self.assertNotIn("adventure-party", f.read())


class SourcePlaceholderTests(unittest.TestCase):

    def test_sources_carry_the_role_placeholder(self):
        # The sources must not name a model: install.sh stamps the real one in
        # from party-models.jsonc. A model written here would be overwritten
        # on every install, and a personal one would leak into the repo.
        for role, rel in party_models.ROLES.items():
            self.assertEqual(frontmatter_model(os.path.join(REPO, rel)),
                             ["model: party-models:" + role], rel)


if __name__ == "__main__":
    unittest.main()
