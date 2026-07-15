"""
[INPUT]: 依赖 scripts/lead-pipeline.py 的 preview upload 与 evidence-backed personalization
[OUTPUT]: 验证默认不产生 Instantly 写入、无已验证来源时不生成文案
[POS]: tests/ 的 lead staging 安全回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("lead_pipeline", ROOT / "scripts" / "lead-pipeline.py")
LEAD_PIPELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LEAD_PIPELINE)


class LeadPipelineSafetyTests(unittest.TestCase):
    def test_upload_is_preview_by_default(self):
        leads = [{"email": "alex@northstar.example"}]
        with patch.object(LEAD_PIPELINE, "request_with_retry") as request:
            result = LEAD_PIPELINE.upload_to_instantly("unused", leads, "demo")
        request.assert_not_called()
        self.assertFalse(result["executed"])
        self.assertEqual(result["planned"], 1)

    def test_personalization_requires_verified_source(self):
        self.assertEqual(LEAD_PIPELINE.generate_personalization({"title": "VP Growth"}), "")
        signal = {"verified": True, "source": "https://northstar.example", "observation": "Hiring a lifecycle lead."}
        self.assertEqual(LEAD_PIPELINE.generate_personalization({"personalization_signal": signal}), signal["observation"])


if __name__ == "__main__":
    unittest.main()
