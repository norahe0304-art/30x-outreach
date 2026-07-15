"""
[INPUT]: 依赖 scripts/cold-outbound-sender.py CLI 与虚构 approved payload
[OUTPUT]: 验证默认 preview 无写入、live execution 缺少 manifest 或 audience proof 时失败
[POS]: tests/ 的最终外部写边界回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import copy
import os
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from thirtyx.approval import create_manifest, write_json


ROOT = Path(__file__).resolve().parents[1]
SENDER = ROOT / "scripts" / "cold-outbound-sender.py"
PAYLOAD = ROOT / "thirtyx" / "demo" / "approved-payload.json"
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("cold_outbound_sender", SENDER)
SENDER_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SENDER_MODULE)


class SenderSafetyTests(unittest.TestCase):
    def run_sender(self, *args):
        environment = {**os.environ, "PYTHONPATH": str(ROOT)}
        return subprocess.run(
            [sys.executable, str(SENDER), "--approved-file", str(PAYLOAD), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )

    def test_preview_is_default_and_does_not_write_history(self):
        with tempfile.TemporaryDirectory() as directory:
            history = Path(directory) / "history.json"
            result = self.run_sender("--history-file", str(history))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PREVIEW", result.stdout)
            self.assertFalse(history.exists())

    def test_execute_requires_manifest(self):
        result = self.run_sender("--execute")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--approval-manifest is required", result.stderr)

    def test_execute_requires_verified_signal_backed_audience(self):
        payload = SENDER_MODULE.load_json(PAYLOAD)
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "approval.json"
            write_json(manifest_path, create_manifest(payload, "ci", payload["campaign_id"]))
            result = self.run_sender("--execute", "--approval-manifest", str(manifest_path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--audience-batch is required", result.stderr)

    def test_audience_rejects_duplicate_approved_recipient(self):
        payload = SENDER_MODULE.load_json(PAYLOAD)
        payload["prospects"].append(copy.deepcopy(payload["prospects"][0]))
        audience = ROOT / "thirtyx" / "demo" / "audience.json"
        valid, errors = SENDER_MODULE.require_execution_audience(payload, audience)
        self.assertFalse(valid)
        self.assertIn("duplicate recipients", errors[0])

    def test_live_send_is_journaled_before_smtp(self):
        prospect = SENDER_MODULE.load_json(PAYLOAD)["prospects"][0]
        settings = {"sender_email": "sender@example.com", "sender_name": "", "host": "smtp.example.com", "port": 587, "user": "sender", "password": "secret"}
        with tempfile.TemporaryDirectory() as directory:
            history_path = Path(directory) / "history.json"
            def assert_pending(*_args):
                history = SENDER_MODULE.load_history(history_path)
                self.assertEqual(history[0]["status"], "pending")
            with patch.object(SENDER_MODULE, "send_smtp", side_effect=assert_pending):
                completed = SENDER_MODULE.process_batch([prospect], True, settings, [], 1, history_path)
            history = SENDER_MODULE.load_history(history_path)
        self.assertEqual(completed, 1)
        self.assertEqual(history[0]["status"], "sent")


if __name__ == "__main__":
    unittest.main()
