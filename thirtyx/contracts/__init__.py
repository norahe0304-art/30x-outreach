"""
[INPUT]: 依赖 wheel 内置 JSON Schema 与 jsonschema Draft 2020-12
[OUTPUT]: 对外提供 load_schema()、validate_instance() 与 SCHEMA_NAMES
[POS]: thirtyx 的运行时数据边界；源码和安装后 CLI 共用同一契约
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import json
from importlib import resources

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


SCHEMA_NAMES = (
    "campaign-spec.schema.json",
    "audience-batch.schema.json",
    "experiment-observation.schema.json",
    "decision-record.schema.json",
    "approval-manifest.schema.json",
    "learning-record.schema.json",
)


def load_schema(name):
    if name not in SCHEMA_NAMES:
        raise ValueError(f"unknown schema: {name}")
    text = resources.files(__name__).joinpath(name).read_text(encoding="utf-8")
    return json.loads(text)


def validate_instance(instance, name):
    validator = Draft202012Validator(load_schema(name), format_checker=FormatChecker())
    try:
        validator.validate(instance)
    except ValidationError as error:
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        raise ValueError(f"{name} validation failed at {location}: {error.message}") from error
    return instance
