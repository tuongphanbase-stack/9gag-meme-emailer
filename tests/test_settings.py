"""Run: python -m unittest discover tests

Offline checks that run on every push (see .github/workflows/tests.yml).
"""
import importlib.util
import os
import re
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "9gag_top_meme_emailer.py")
sys.path.insert(0, ROOT)


def setting_names():
    """Every environment variable the script reads."""
    with open(SCRIPT, encoding="utf-8") as f:
        src = f.read()
    return set(re.findall(r'environ(?:\.get)?[(\[]\s*"([A-Z0-9_]+)"', src)) | set(
        re.findall(r'_env\(\s*"([A-Z0-9_]+)"', src))


def load(env=None, unset=()):
    """Import the script as a fresh module, from a scratch working directory."""
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, env or {}):
        for name in unset:
            os.environ.pop(name, None)
        os.chdir(tmp)
        try:
            spec = importlib.util.spec_from_file_location("emailer_under_test", SCRIPT)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        finally:
            os.chdir(cwd)


class Settings(unittest.TestCase):
    def test_loads_with_every_setting_empty(self):
        # The workflow passes an unset repository variable as an empty string;
        # float("") once crashed currency-rate-emailer on every run.
        names = setting_names()
        self.assertTrue(names)
        load({n: "" for n in names})

    def test_loads_with_no_settings(self):
        load(unset=setting_names())


class Dashboard(unittest.TestCase):
    def test_generate_updates_the_dashboard_status(self):
        m = load()
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(m, "get_top_memes_by_section", return_value={k: [] for k, _, _ in m.SECTIONS}):
            os.chdir(tmp)
            try:
                m.cmd_generate()
                with open(m.LATEST_FILE, encoding="utf-8") as f:
                    latest = f.read()
            finally:
                os.chdir(cwd)
        self.assertIn('"item_count": 0', latest)
        self.assertIn('"updated_at": "20', latest)
