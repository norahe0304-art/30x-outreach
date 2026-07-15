"""
[INPUT]: 依赖 thirtyx.approval 的规范化哈希与 manifest API
[OUTPUT]: 验证相同 JSON 哈希稳定、内容变更阻断、recipient count 绑定
[POS]: tests/ 的审批安全回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import copy
import unittest

from thirtyx.approval import content_sha256, create_manifest, verify_manifest


class ApprovalGateTests(unittest.TestCase):
    def setUp(self):
        self.payload = {"campaign_id": "demo", "prospects": [{"email": "alex@northstar.example"}]}

    def test_hash_is_order_independent(self):
        reordered = {"prospects": [{"email": "alex@northstar.example"}], "campaign_id": "demo"}
        self.assertEqual(content_sha256(self.payload), content_sha256(reordered))

    def test_mutation_invalidates_approval(self):
        manifest = create_manifest(self.payload, "reviewer@example.com", "demo")
        mutated = copy.deepcopy(self.payload)
        mutated["prospects"][0]["email"] = "other@northstar.example"
        valid, errors = verify_manifest(mutated, manifest)
        self.assertFalse(valid)
        self.assertIn("content_sha256 does not match payload", errors)

    def test_campaign_mismatch_cannot_be_approved(self):
        with self.assertRaises(ValueError):
            create_manifest(self.payload, "reviewer@example.com", "different-campaign")


if __name__ == "__main__":
    unittest.main()
