<!--
[INPUT]: 依赖项目的凭据、PII、approval、execution 与 dependency 风险模型
[OUTPUT]: 对外提供支持版本和私密漏洞报告流程
[POS]: .github 的安全响应契约；禁止在公开 issue 披露可利用细节
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
# Security policy

## Supported versions

The newest tagged `0.x` release receives security fixes. The default branch may contain unreleased changes and is not a stability promise.

## Report privately

Do not open a public issue for a vulnerability involving credential exposure, approval bypass, unintended external writes, recipient PII, injection, or dependency compromise.

Use [GitHub private vulnerability reporting](https://github.com/norahe0304-art/30x-outreach/security/advisories/new). Include the affected version, reproduction, impact, and a minimal redacted proof. Never attach real credentials or contact data.

## Response

Maintainers will acknowledge a complete report, validate the boundary, prepare a fix and regression test, and coordinate disclosure. No response-time SLA is promised while the project is maintained independently.

## Operator responsibility

30x provides technical safeguards, not legal clearance. Operators remain responsible for consent, suppression lists, platform terms, sending reputation, and applicable laws.
