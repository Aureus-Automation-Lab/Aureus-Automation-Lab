from __future__ import annotations

"""Validate a JSON document against the dependency-free schema subset used here."""

import argparse
import json
import re
from pathlib import Path
from typing import Any


class SchemaValidationError(ValueError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def resolve_reference(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise SchemaValidationError(f"Only local JSON Pointer references are supported: {reference}")
    value: Any = root_schema
    for raw_token in reference[2:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise SchemaValidationError(f"Unresolvable schema reference: {reference}")
        value = value[token]
    if not isinstance(value, dict):
        raise SchemaValidationError(f"Schema reference does not resolve to an object: {reference}")
    return value


def matches_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return type(value) is bool
    if expected == "integer":
        return type(value) is int
    if expected == "number":
        return type(value) in {int, float}
    if expected == "string":
        return type(value) is str
    if expected == "array":
        return type(value) is list
    if expected == "object":
        return type(value) is dict
    raise SchemaValidationError(f"Unsupported schema type: {expected}")


def validate_instance(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    errors: list[str] = []

    if "$ref" in schema:
        errors.extend(validate_instance(value, resolve_reference(root_schema, schema["$ref"]), root_schema, path))

    for subschema in schema.get("allOf", []):
        errors.extend(validate_instance(value, subschema, root_schema, path))

    expected_type = schema.get("type")
    if expected_type is not None:
        expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(matches_type(value, item) for item in expected_types):
            errors.append(f"{path}: expected type {' or '.join(expected_types)}, got {type(value).__name__}")
            return errors

    if "const" in schema and canonical(value) != canonical(schema["const"]):
        errors.append(f"{path}: value does not match const {schema['const']!r}")
    if "enum" in schema and all(canonical(value) != canonical(item) for item in schema["enum"]):
        errors.append(f"{path}: value is not in the allowed enum")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key!r}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_instance(value[key], child_schema, root_schema, f"{path}.{key}"))
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errors.append(f"{path}: expected at least {schema['minProperties']} properties")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: expected at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            items = [canonical(item) for item in value]
            if len(items) != len(set(items)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, item_schema, root_schema, f"{path}[{index}]"))
        contains_schema = schema.get("contains")
        if isinstance(contains_schema, dict):
            matches = [
                not validate_instance(item, contains_schema, root_schema, f"{path}[{index}]")
                for index, item in enumerate(value)
            ]
            if not any(matches):
                errors.append(f"{path}: array does not contain an item matching the required schema")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: string is shorter than {schema['minLength']}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")

    if type(value) in {int, float}:
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: number is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: number is above maximum {schema['maximum']}")

    return errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local JSON policy against its checked-in schema")
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--instance", required=True, type=Path)
    args = parser.parse_args()

    try:
        schema = load_json(args.schema)
        instance = load_json(args.instance)
        if not isinstance(schema, dict):
            raise SchemaValidationError("Schema root must be an object")
        errors = validate_instance(instance, schema, schema)
    except (OSError, UnicodeError, json.JSONDecodeError, SchemaValidationError) as exc:
        print("LOCAL_JSON_SCHEMA_VALIDATION: BLOCKED")
        print(f"- {exc}")
        return 2

    if errors:
        print("LOCAL_JSON_SCHEMA_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LOCAL_JSON_SCHEMA_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
