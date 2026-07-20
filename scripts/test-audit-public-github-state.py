from __future__ import annotations

"""Dependency-free regression tests for the public GitHub drift audit."""

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/audit-public-github-state.py"
SCHEMA_MODULE_PATH = ROOT / "scripts/validate-local-json-schema.py"
PORTFOLIO_MODULE_PATH = ROOT / "scripts/validate-public-portfolio.py"
POLICY_PATH = ROOT / ".github/governance/public-profile-policy.json"
SCHEMA_PATH = ROOT / ".github/governance/public-profile-policy.schema.json"
MANIFEST_PATH = ROOT / "public-proof/portfolio-manifest.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_module("audit_public_github_state", MODULE_PATH)
SCHEMA_VALIDATOR = load_module("validate_local_json_schema", SCHEMA_MODULE_PATH)
PORTFOLIO = load_module("validate_public_portfolio", PORTFOLIO_MODULE_PATH)


def load_policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def assert_raises(expected_exception, function, *args) -> None:
    try:
        function(*args)
    except expected_exception:
        return
    raise AssertionError(f"Expected {expected_exception.__name__}")


def assert_policy_rejected(policy: dict) -> None:
    assert_raises(AUDIT.PolicyValidationError, AUDIT.validate_policy, policy)
    assert SCHEMA_VALIDATOR.validate_instance(policy, load_schema(), load_schema())


def empty_report() -> dict:
    return {"status": "PENDING", "observed": {}, "findings": [], "api_errors": []}


def matching_ruleset(policy: dict, *, include_bypass_actors: bool = True) -> dict:
    rules = [
        {"type": rule_type}
        for rule_type in policy["ruleset"]["required_rule_types"]
        if rule_type not in {"pull_request", "required_status_checks"}
    ]
    rules.extend(
        [
            {
                "type": "pull_request",
                "parameters": copy.deepcopy(policy["ruleset"]["pull_request"]),
            },
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": True,
                    "required_status_checks": copy.deepcopy(
                        policy["ruleset"]["required_status_checks"]["contexts"]
                    ),
                },
            },
        ]
    )
    payload = {
        "id": 77,
        "name": policy["ruleset"]["name"],
        "target": policy["ruleset"]["target"],
        "enforcement": policy["ruleset"]["enforcement"],
        "conditions": {
            "ref_name": {
                "include": policy["ruleset"]["include_refs"],
                "exclude": policy["ruleset"]["exclude_refs"],
            }
        },
        "rules": rules,
    }
    if include_bypass_actors:
        payload["bypass_actors"] = []
    return payload


def fake_governance_reads(policy: dict, manifest: dict):
    def reader(path: Path) -> str:
        resolved = Path(path).resolve()
        if resolved == POLICY_PATH.resolve():
            return json.dumps(policy)
        if resolved == MANIFEST_PATH.resolve():
            return json.dumps(manifest)
        return Path(path).read_text(encoding="utf-8")

    return reader


def test_valid_policy_and_schema() -> None:
    policy = load_policy()
    AUDIT.validate_policy(policy)
    assert SCHEMA_VALIDATOR.validate_instance(policy, load_schema(), load_schema()) == []


def test_exact_repository_identity_is_fail_closed() -> None:
    policy = load_policy()
    policy["repository"]["name_with_owner"] = "AureusAutomationLab/Aureus-Automation-Lab"
    assert_policy_rejected(policy)


def test_exact_founder_identity_is_fail_closed() -> None:
    for mutated in ("aureus-automation-lab", "AureusAutomationLab"):
        policy = load_policy()
        policy["founder_profile"]["account"] = mutated
        assert_policy_rejected(policy)


def test_rollout_phase_and_cross_file_identity_mismatches_block() -> None:
    unsupported = load_policy()
    unsupported["rollout_phase"] = "unreviewed-phase"
    assert_policy_rejected(unsupported)

    supported_but_mismatched = load_policy()
    supported_but_mismatched["rollout_phase"] = "profile-hardening"
    errors: list[str] = []
    with mock.patch.object(
        PORTFOLIO,
        "read_text",
        side_effect=fake_governance_reads(supported_but_mismatched, load_manifest()),
    ):
        PORTFOLIO.validate_governance_policy(errors)
    assert any("rollout phase" in error.lower() for error in errors)

    manifest = load_manifest()
    manifest["canonical_identity"]["current_profile_account"] = "Different-Subject"
    manifest["canonical_identity"]["current_profile_repository"] = "Different/Repository"
    errors = []
    with mock.patch.object(
        PORTFOLIO,
        "read_text",
        side_effect=fake_governance_reads(load_policy(), manifest),
    ):
        PORTFOLIO.validate_governance_policy(errors)
    assert any("repository identity" in error.lower() for error in errors)
    assert any("founder identity" in error.lower() for error in errors)


def test_manifest_governance_phase_is_fail_closed() -> None:
    manifest = load_manifest()
    manifest["governance_state"]["rollout_phase"] = "target-operating-state"
    errors: list[str] = []
    with mock.patch.object(PORTFOLIO, "read_text", return_value=json.dumps(manifest)):
        PORTFOLIO.validate_manifest(errors)
    assert any("governance_state" in error for error in errors)


def test_change_control_is_exact_minimal_public_contract() -> None:
    expected = {
        "mode": "review_required",
        "least_privilege": True,
        "fail_closed": True,
        "rollback_evidence_required": True,
        "post_change_attestation_required": True,
        "sensitive_execution_contract": "private",
    }
    policy = load_policy()
    assert policy["change_control"] == expected
    assert PORTFOLIO.governance_change_control_findings(policy) == []

    for key in expected:
        mutated = load_policy()
        mutated["change_control"][key] = False if isinstance(expected[key], bool) else "mutated"
        assert_policy_rejected(mutated)

    extra = load_policy()
    extra["change_control"]["status"] = "VERIFIED"
    assert_policy_rejected(extra)
    assert PORTFOLIO.governance_change_control_findings(extra)


def test_private_scope_compiler_is_absent_from_public_contract() -> None:
    public_contract = "\n".join(
        [
            POLICY_PATH.read_text(encoding="utf-8"),
            SCHEMA_PATH.read_text(encoding="utf-8"),
            (ROOT / "docs/portfolio/github-portfolio-standard.md").read_text(
                encoding="utf-8"
            ),
        ]
    )
    assert "live_scope_compiler" not in public_contract
    assert "GIT-ORG-" not in public_contract


def test_reviewer_status_accepts_only_approval_required_or_verified() -> None:
    for invalid_status in ("PASS", "BLOCKED", "REPAIR_REQUIRED", ""):
        policy = load_policy()
        policy["review_governance"]["current_status"] = invalid_status
        assert_policy_rejected(policy)


def test_founder_can_never_be_independent_reviewer() -> None:
    founder = load_policy()["founder_profile"]["account"]
    for status in ("APPROVAL_REQUIRED", "VERIFIED"):
        for reviewer in (founder, founder.lower(), founder.upper()):
            policy = load_policy()
            policy["review_governance"]["current_status"] = status
            policy["review_governance"]["independent_reviewer_login"] = reviewer
            assert_raises(AUDIT.PolicyValidationError, AUDIT.validate_policy, policy)


def test_bot_reviewer_identity_is_blocked() -> None:
    policy = load_policy()
    problem = AUDIT.reviewer_identity_problem(
        policy,
        "trusted-reviewer",
        {"login": "trusted-reviewer", "type": "Bot", "suspended_at": None},
    )
    assert problem == "Reviewer must resolve to a human GitHub User"


def test_codeowners_requires_exact_reviewer_on_every_rule() -> None:
    invalid = "* @trusted-reviewer\n/docs/ @someone-else\n"
    assert_raises(
        AUDIT.PolicyValidationError,
        AUDIT.validate_codeowners_reviewer,
        invalid,
        "trusted-reviewer",
    )
    valid = "* @trusted-reviewer\n/docs/ @trusted-reviewer @someone-else\n"
    AUDIT.validate_codeowners_reviewer(valid, "trusted-reviewer")


def test_safe_error_redacts_all_supported_secret_shapes_before_truncation() -> None:
    sentinel = "SENTINEL_ULTRA_SECRET_1234"
    samples = [
        f"Authorization: Bearer {sentinel}",
        f"Authorization: Basic {sentinel}",
        f"request failed for ghp_{sentinel}",
        f"request failed for github_pat_{sentinel}",
        f"https://example.invalid/a?token={sentinel}&page=1",
        f"https://example.invalid/a?client_secret={sentinel}",
        ("padding " * 200) + f"Authorization: Bearer {sentinel}",
    ]
    for sample in samples:
        redacted = AUDIT.safe_error(sample)
        assert sentinel not in redacted
        assert "[REDACTED]" in redacted

        report = empty_report()
        AUDIT.record_api_error(report, "fixture", sample)
        serialized = json.dumps(report, ensure_ascii=False)
        assert sentinel not in serialized
        assert "[REDACTED]" in serialized


def test_github_timeout_is_bounded() -> None:
    with mock.patch.object(
        AUDIT.subprocess,
        "run",
        side_effect=subprocess.TimeoutExpired(cmd=["gh", "api"], timeout=20),
    ):
        ok, payload, error = AUDIT.gh_json(["user"])
    assert ok is False
    assert payload is None
    assert error == "BLOCKED_GITHUB_API_TIMEOUT after 20 seconds"


def test_audit_actor_profile_subject_mismatch_is_blocking_and_redacted() -> None:
    policy = load_policy()
    sentinel = "SENTINEL_ACTOR_SECRET_9876"
    report = empty_report()
    with mock.patch.object(
        AUDIT,
        "gh_json",
        side_effect=[
            (True, {"login": "different-actor"}, None),
            (False, None, f"HTTP 403?access_token={sentinel}"),
        ],
    ):
        AUDIT.audit_repository(report, policy)
    finding = next(
        item
        for item in report["findings"]
        if item["control"] == "identity.audit_actor_matches_profile_subject"
    )
    assert finding["disposition"] == "BLOCKED_AUDIT_ACTOR_PROFILE_SUBJECT_MISMATCH"
    assert sentinel not in json.dumps(report, ensure_ascii=False)


def test_status_precedence_preserves_identity_blockers() -> None:
    report = empty_report()
    AUDIT.add_finding(
        report,
        "identity.audit_actor_matches_profile_subject",
        "Aureus-Automation-Lab",
        "different-actor",
        "BLOCKED_AUDIT_ACTOR_PROFILE_SUBJECT_MISMATCH",
    )
    assert AUDIT.finalize_status(report) == 3
    assert report["status"] == "BLOCKED_AUDIT_ACTOR_PROFILE_SUBJECT_MISMATCH"

    mixed = empty_report()
    AUDIT.add_finding(mixed, "repair", True, False, "REPAIR_REQUIRED")
    AUDIT.add_finding(mixed, "approval", True, False, "APPROVAL_REQUIRED")
    assert AUDIT.finalize_status(mixed) == 2
    assert mixed["status"] == "REPAIR_REQUIRED_AND_APPROVAL_REQUIRED"


def test_missing_ruleset_bypass_visibility_fails_closed() -> None:
    policy = load_policy()
    ruleset = matching_ruleset(policy, include_bypass_actors=False)
    report = empty_report()
    with mock.patch.object(
        AUDIT,
        "gh_json",
        side_effect=[
            (True, [{"id": 77, "name": policy["ruleset"]["name"]}], None),
            (True, ruleset, None),
        ],
    ):
        AUDIT.audit_ruleset(report, policy, "owner", "repository")
    assert any(
        "BLOCKED_RULESET_BYPASS_VISIBILITY" in item["error"]
        for item in report["api_errors"]
    )


def test_ruleset_requires_exact_rules_and_bound_check_source() -> None:
    policy = load_policy()
    ruleset = matching_ruleset(policy)
    ruleset["rules"].append({"type": "creation"})
    checks = next(
        rule for rule in ruleset["rules"] if rule["type"] == "required_status_checks"
    )
    checks["parameters"]["required_status_checks"][0]["integration_id"] = 999
    report = empty_report()
    with mock.patch.object(
        AUDIT,
        "gh_json",
        side_effect=[
            (True, [{"id": 77, "name": policy["ruleset"]["name"]}], None),
            (True, ruleset, None),
        ],
    ):
        AUDIT.audit_ruleset(report, policy, "owner", "repository")
    controls = {item["control"] for item in report["findings"]}
    assert "ruleset.required_rule_types" in controls
    assert "ruleset.required_status_checks.contexts" in controls


def test_legacy_branch_protection_is_phase_aware() -> None:
    policy = load_policy()
    required_report = empty_report()
    AUDIT.audit_legacy_branch_protection(required_report, policy, None)
    assert required_report["findings"][0]["disposition"] == (
        "REPAIR_REQUIRED_LEGACY_PROTECTION_MISSING"
    )

    policy["rollout_phase"] = "target-operating-state"
    forbidden_report = empty_report()
    AUDIT.audit_legacy_branch_protection(forbidden_report, policy, {"url": "present"})
    assert forbidden_report["findings"][0]["disposition"] == (
        "APPROVAL_REQUIRED_LEGACY_PROTECTION_REMOVAL"
    )


def test_live_codeowners_must_match_default_branch() -> None:
    policy = load_policy()
    reviewer = "trusted-reviewer"
    live_content = "* @trusted-reviewer\n/docs/ @someone-else\n"
    payload = {
        "path": ".github/CODEOWNERS",
        "sha": "abc123",
        "encoding": "base64",
        "content": AUDIT.base64.b64encode(live_content.encode("utf-8")).decode("ascii"),
    }
    report = empty_report()
    with mock.patch.object(AUDIT, "gh_json", return_value=(True, payload, None)):
        AUDIT.audit_live_codeowners(report, policy, "owner/repository", "main", reviewer)
    assert report["findings"][0]["disposition"] == "BLOCKED_LIVE_CODEOWNERS_UNVERIFIED"


def test_reviewer_permission_is_exact_least_privilege() -> None:
    policy = load_policy()
    reviewer = "trusted-reviewer"
    codeowners = "* @trusted-reviewer\n"
    codeowners_payload = {
        "path": ".github/CODEOWNERS",
        "sha": "abc123",
        "encoding": "base64",
        "content": AUDIT.base64.b64encode(codeowners.encode("utf-8")).decode("ascii"),
    }
    report = empty_report()
    with mock.patch.object(
        AUDIT,
        "gh_json",
        side_effect=[
            (True, {"login": reviewer, "type": "User", "suspended_at": None}, None),
            (True, {"permission": "admin"}, None),
            (False, None, "HTTP 404: Not Found"),
            (True, codeowners_payload, None),
        ],
    ):
        AUDIT.audit_live_reviewer(report, policy, "owner/repository", "main", reviewer)
    finding = next(
        item
        for item in report["findings"]
        if item["control"] == "review_governance.independent_reviewer_permission"
    )
    assert finding["expected"] == "push"
    assert finding["actual"] == "admin"
    assert finding["disposition"] == "BLOCKED_REVIEWER_ACCESS_BLAST_RADIUS"


def test_license_and_contact_boundaries_fail_closed() -> None:
    policy = load_policy()
    assert policy["license_boundary"]["status"] == "APPROVAL_REQUIRED_LICENSE_DECISION"
    assert policy["promotion_readiness"]["status"] == "BLOCKED_PENDING_CONTACT_PATH"
    assert policy["promotion_readiness"]["approved_contact_url"] is None
    assert not any((ROOT / name).exists() for name in ("LICENSE", "LICENSE.md", "LICENSE.txt"))

    license_drift = load_policy()
    license_drift["license_boundary"]["no_license_grant"] = False
    assert_policy_rejected(license_drift)

    contact_drift = load_policy()
    contact_drift["promotion_readiness"]["approved_contact_url"] = (
        "https://example.invalid/contact"
    )
    assert_policy_rejected(contact_drift)


def test_manifest_uses_public_approval_gates_not_private_scope_ids() -> None:
    manifest = load_manifest()
    serialized = json.dumps(manifest)
    assert "dependency_scope_ids" not in serialized
    for item in manifest["portfolio_items"]:
        gate = item["source_lineage"]["publication_gate"]
        if item["publication_status"] == "sanitized-candidate":
            assert gate == "APPROVAL_REQUIRED"
        else:
            assert gate == "PASS"


def test_workflow_security_handles_yaml_spacing_and_secret_variants() -> None:
    fixture = """
on:
  pull_request_target :
permissions:
  contents : write
  id-token : write
jobs:
  audit:
    steps:
      - uses : actions/checkout@main
      - run: echo "${{ secrets['TOKEN'] }}"
"""
    findings = PORTFOLIO.workflow_security_findings(fixture)
    assert len(findings) == 5
    assert any("pull_request_target" in item for item in findings)
    assert any("contents: write" in item for item in findings)
    assert any("OIDC" in item for item in findings)
    assert any("repository secrets" in item for item in findings)
    assert any("not pinned" in item for item in findings)


def test_security_controls_cover_full_baseline() -> None:
    policy = load_policy()
    repo = {
        "security_and_analysis": {
            key: {"status": "enabled"}
            for key in AUDIT.REPOSITORY_SECURITY_AND_ANALYSIS_KEYS
        }
    }
    report = empty_report()
    with mock.patch.object(
        AUDIT,
        "gh_json",
        side_effect=[
            (True, {}, None),
            (True, {}, None),
            (True, {"enabled": True}, None),
        ],
    ):
        AUDIT.audit_security_controls(report, policy, "owner/repository", repo)
    assert report["findings"] == []
    assert report["api_errors"] == []
    assert set(report["observed"]["security_and_analysis"]) == set(
        policy["security_and_analysis"]
    )


def main() -> int:
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as exc:  # noqa: BLE001 - dependency-free test harness
            failures.append(f"{test.__name__}: {type(exc).__name__}: {exc}")

    if failures:
        print("PUBLIC_GITHUB_AUDIT_TESTS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PUBLIC_GITHUB_AUDIT_TESTS: PASS ({len(tests)} tests)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
