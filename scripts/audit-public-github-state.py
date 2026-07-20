from __future__ import annotations

"""Bounded read-only drift audit for the Aureus public GitHub governance baseline."""

import argparse
import base64
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / ".github/governance/public-profile-policy.json"
GH_API_TIMEOUT_SECONDS = 20
GH_API_HEADERS = [
    "-H",
    "Accept: application/vnd.github+json",
    "-H",
    "X-GitHub-Api-Version: 2022-11-28",
]
REPOSITORY_SECURITY_AND_ANALYSIS_KEYS = {
    "secret_scanning",
    "secret_scanning_push_protection",
    "secret_scanning_validity_checks",
    "secret_scanning_non_provider_patterns",
}
ORGANIZATION_LIVE_CONTROL_KEYS = {
    "default_repository_permission",
    "two_factor_requirement_enabled",
    "members_can_create_repositories",
    "members_can_create_public_repositories",
    "members_can_create_private_repositories",
    "members_can_create_internal_repositories",
    "members_can_delete_repositories",
    "members_can_change_repo_visibility",
    "web_commit_signoff_required",
}
CANONICAL_PUBLIC_REPOSITORY = "Aureus-Automation-Lab/Aureus-Automation-Lab"
CANONICAL_PROFILE_SUBJECT = "Aureus-Automation-Lab"
SUPPORTED_ROLLOUT_PHASES = {
    "pre-reviewer-bootstrap",
    "profile-hardening",
    "proof-publication",
    "target-operating-state",
}
SECRET_PATTERNS = (
    re.compile(r"(?i)(authorization\s*:\s*(?:bearer|basic)\s+)[^\s|,;]+"),
    re.compile(r"(?i)\b(?:gh[pousr]_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,})\b"),
    re.compile(
        r"(?i)([?&](?:access_token|api_key|client_secret|secret|token|key)=)[^&\s|]+"
    ),
)


class PolicyValidationError(ValueError):
    pass


def safe_error(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(
            lambda match: f"{match.group(1)}[REDACTED]"
            if match.lastindex
            else "[REDACTED]",
            redacted,
        )
    lines = [line.strip() for line in redacted.splitlines() if line.strip()]
    joined = " | ".join(lines[-3:])
    return joined[-600:]


def gh_json(arguments: list[str]) -> tuple[bool, Any, str | None]:
    try:
        process = subprocess.run(
            ["gh", "api", *GH_API_HEADERS, *arguments],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=GH_API_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        return False, None, "GitHub CLI is not installed or is not available on PATH"
    except subprocess.TimeoutExpired:
        return False, None, f"BLOCKED_GITHUB_API_TIMEOUT after {GH_API_TIMEOUT_SECONDS} seconds"

    if process.returncode != 0:
        return False, None, safe_error(process.stderr or process.stdout)

    output = process.stdout.strip()
    if not output:
        return True, {}, None

    try:
        return True, json.loads(output), None
    except json.JSONDecodeError as exc:
        return False, None, f"GitHub CLI returned invalid JSON: {exc}"


def add_finding(
    report: dict[str, Any],
    control: str,
    expected: Any,
    actual: Any,
    disposition: str = "APPROVAL_REQUIRED",
) -> None:
    report["findings"].append(
        {
            "control": control,
            "expected": expected,
            "actual": actual,
            "disposition": disposition,
        }
    )


def compare(
    report: dict[str, Any],
    control: str,
    expected: Any,
    actual: Any,
    disposition: str = "APPROVAL_REQUIRED",
) -> None:
    if actual != expected:
        add_finding(report, control, expected, actual, disposition)


def record_api_error(report: dict[str, Any], endpoint: str, error: str | None) -> None:
    report["api_errors"].append(
        {
            "endpoint": endpoint,
            "error": safe_error(error or "Unknown GitHub API error"),
        }
    )


def load_policy() -> dict[str, Any]:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    validate_policy(policy)
    return policy


def nested_value(policy: dict[str, Any], path: str) -> Any:
    value: Any = policy
    for key in path.split("."):
        if not isinstance(value, dict) or key not in value:
            raise PolicyValidationError(f"Missing required policy field: {path}")
        value = value[key]
    return value


def codeowner_rules(content: str) -> list[tuple[str, set[str]]]:
    """Return effective CODEOWNERS rules with exact owner tokens."""
    rules: list[tuple[str, set[str]]] = []
    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) < 2:
            continue
        rules.append((fields[0], set(fields[1:])))
    return rules


def validate_codeowners_reviewer(content: str, reviewer_login: str) -> None:
    rules = codeowner_rules(content)
    reviewer_token = f"@{reviewer_login}".casefold()
    if not any(pattern == "*" for pattern, _ in rules):
        raise PolicyValidationError("CODEOWNERS must contain an effective wildcard rule")
    missing = [
        pattern
        for pattern, owners in rules
        if reviewer_token not in {owner.casefold() for owner in owners}
    ]
    if missing:
        raise PolicyValidationError(
            "VERIFIED review governance requires the exact independent reviewer token on "
            f"every effective CODEOWNERS rule; missing: {', '.join(missing)}"
        )


def decode_github_content(payload: Any) -> str:
    """Decode a GitHub contents API payload without accepting ambiguous encodings."""
    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        raise PolicyValidationError("GitHub content payload must use base64 encoding")
    encoded = payload.get("content")
    if not isinstance(encoded, str):
        raise PolicyValidationError("GitHub content payload is missing content")
    try:
        compact = "".join(encoded.split())
        return base64.b64decode(compact, validate=True).decode("utf-8")
    except (ValueError, UnicodeError) as exc:
        raise PolicyValidationError("GitHub content payload is not valid base64 UTF-8") from exc


def reviewer_identity_problem(
    policy: dict[str, Any], reviewer_login: str, payload: Any
) -> str | None:
    """Return a fail-closed reason when the live reviewer is not a distinct human user."""
    if not isinstance(payload, dict):
        return "GitHub user payload is not an object"
    actual_login = payload.get("login")
    if not isinstance(actual_login, str) or actual_login.casefold() != reviewer_login.casefold():
        return "GitHub canonical login does not match the configured reviewer"
    if actual_login.casefold() == policy["founder_profile"]["account"].casefold():
        return "Reviewer resolves to the founder account"
    if payload.get("type") != "User":
        return "Reviewer must resolve to a human GitHub User"
    suspended_at = payload.get("suspended_at")
    if suspended_at is not None and suspended_at != "":
        return "Reviewer account is suspended"
    return None


def normalized_status_checks(checks: Any) -> list[dict[str, Any]]:
    """Normalize required checks while preserving the source application binding."""
    if not isinstance(checks, list):
        return []
    normalized: list[dict[str, Any]] = []
    for check in checks:
        if not isinstance(check, dict):
            normalized.append({"context": None, "integration_id": None})
            continue
        normalized.append(
            {
                "context": check.get("context"),
                "integration_id": check.get("integration_id"),
            }
        )
    return sorted(
        normalized,
        key=lambda item: (str(item.get("context")), str(item.get("integration_id"))),
    )


def validate_change_control(policy: dict[str, Any]) -> None:
    """Validate the public desired-state boundary without exposing private execution topology."""
    change_control = policy["change_control"]
    expected_static = {
        "mode": "review_required",
        "least_privilege": True,
        "fail_closed": True,
        "rollback_evidence_required": True,
        "post_change_attestation_required": True,
        "sensitive_execution_contract": "private",
    }
    for key, expected in expected_static.items():
        if change_control[key] != expected:
            raise PolicyValidationError(
                f"change_control.{key} does not match the reviewed public contract"
            )
    if set(change_control) != set(expected_static):
        raise PolicyValidationError(
            "change_control must contain only the reviewed public contract fields"
        )


def validate_policy(policy: Any) -> None:
    if not isinstance(policy, dict):
        raise PolicyValidationError("Policy root must be an object")

    required_types: dict[str, type | tuple[type, ...]] = {
        "schema_version": str,
        "policy_id": str,
        "rollout_phase": str,
        "repository.name_with_owner": str,
        "repository.visibility": str,
        "repository.default_branch": str,
        "repository.archived": bool,
        "repository.required_topics": list,
        "repository_features": dict,
        "merge_policy": dict,
        "review_governance.minimum_distinct_human_reviewers": int,
        "review_governance.codeowners_must_include_independent_reviewer": bool,
        "review_governance.reviewer_access_mode": str,
        "review_governance.required_repository_permission": str,
        "review_governance.organization_membership_for_review_forbidden": bool,
        "review_governance.require_effective_access_diff_before_after": bool,
        "review_governance.independent_reviewer_login": (str, type(None)),
        "review_governance.current_status": str,
        "ruleset.name": str,
        "ruleset.target": str,
        "ruleset.enforcement": str,
        "ruleset.include_refs": list,
        "ruleset.exclude_refs": list,
        "ruleset.maximum_bypass_actors": int,
        "ruleset.required_rule_types": list,
        "ruleset.pull_request": dict,
        "ruleset.pull_request.allowed_merge_methods": list,
        "ruleset.required_status_checks.strict_required_status_checks_policy": bool,
        "ruleset.required_status_checks.contexts": list,
        "legacy_branch_protection.required_in_rollout_phases": list,
        "legacy_branch_protection.forbidden_in_rollout_phases": list,
        "legacy_branch_protection.minimum_controls": dict,
        "security_and_analysis": dict,
        "community.minimum_health_percentage": int,
        "founder_profile.account": str,
        "founder_profile.required_non_empty_fields": list,
        "founder_profile.minimum_pinned_repositories_current_phase": int,
        "founder_profile.minimum_pinned_repositories_target_phase": int,
        "founder_profile.maximum_pinned_repositories": int,
        "company_profile.organization": str,
        "company_profile.public_profile_repository": str,
        "company_profile.default_branch": str,
        "company_profile.initial_commit_contract": dict,
        "company_profile.initial_commit_contract.branch": str,
        "company_profile.initial_commit_contract.parent_sha": type(None),
        "company_profile.initial_commit_contract.exact_tree": bool,
        "company_profile.initial_commit_contract.required_paths": list,
        "company_profile.required_non_empty_fields": list,
        "organization_governance.default_repository_permission": str,
        "organization_governance.two_factor_requirement_enabled": bool,
        "organization_governance.members_can_create_repositories": bool,
        "organization_governance.members_can_create_public_repositories": bool,
        "organization_governance.members_can_create_private_repositories": bool,
        "organization_governance.members_can_create_internal_repositories": bool,
        "organization_governance.members_can_delete_repositories": bool,
        "organization_governance.members_can_change_repo_visibility": bool,
        "organization_governance.web_commit_signoff_required": bool,
        "organization_governance.require_removal_impact_preflight": bool,
        "organization_governance.require_effective_access_diff_before_after": bool,
        "organization_governance.require_audit_log_evidence": bool,
        "change_control.mode": str,
        "change_control.least_privilege": bool,
        "change_control.fail_closed": bool,
        "change_control.rollback_evidence_required": bool,
        "change_control.post_change_attestation_required": bool,
        "change_control.sensitive_execution_contract": str,
        "license_boundary.status": str,
        "license_boundary.no_license_grant": bool,
        "license_boundary.decision_scope": list,
        "promotion_readiness.status": str,
        "promotion_readiness.approved_contact_url": (str, type(None)),
        "promotion_readiness.contact_path_requires_owner_approval": bool,
        "promotion_readiness.contact_path_requires_verification": bool,
    }
    for path, expected_type in required_types.items():
        value = nested_value(policy, path)
        expected_types = expected_type if isinstance(expected_type, tuple) else (expected_type,)
        if type(value) not in expected_types:
            expected_names = " or ".join(item.__name__ for item in expected_types)
            raise PolicyValidationError(
                f"Policy field {path} must be {expected_names}; got {type(value).__name__}"
            )

    if policy["schema_version"] != "1.4":
        raise PolicyValidationError("schema_version must be 1.4")
    if policy["policy_id"] != "aureus-public-profile-governance":
        raise PolicyValidationError("Unexpected policy_id")
    if policy["rollout_phase"] not in SUPPORTED_ROLLOUT_PHASES:
        raise PolicyValidationError("Unsupported rollout_phase")

    name_with_owner = policy["repository"]["name_with_owner"]
    if name_with_owner != CANONICAL_PUBLIC_REPOSITORY:
        raise PolicyValidationError(
            f"repository.name_with_owner must be {CANONICAL_PUBLIC_REPOSITORY}"
        )
    founder_account = policy["founder_profile"]["account"]
    if founder_account != CANONICAL_PROFILE_SUBJECT:
        raise PolicyValidationError(
            f"founder_profile.account must be {CANONICAL_PROFILE_SUBJECT}"
        )
    if not policy["repository"]["required_topics"]:
        raise PolicyValidationError("repository.required_topics cannot be empty")
    if len(set(policy["repository"]["required_topics"])) != len(policy["repository"]["required_topics"]):
        raise PolicyValidationError("repository.required_topics cannot contain duplicates")

    maximum_pins = policy["founder_profile"]["maximum_pinned_repositories"]
    current_minimum = policy["founder_profile"]["minimum_pinned_repositories_current_phase"]
    target_minimum = policy["founder_profile"]["minimum_pinned_repositories_target_phase"]
    if not (0 <= current_minimum <= target_minimum <= maximum_pins <= 6):
        raise PolicyValidationError("Founder pin thresholds must satisfy 0 <= current <= target <= max <= 6")

    company_profile = policy["company_profile"]
    expected_initial_commit_contract = {
        "branch": "main",
        "parent_sha": None,
        "exact_tree": True,
        "required_paths": [
            "profile/README.md",
            ".github/CODEOWNERS",
            "SECURITY.md",
            ".github/workflows/public-profile-validation.yml",
        ],
    }
    if company_profile["initial_commit_contract"] != expected_initial_commit_contract:
        raise PolicyValidationError(
            "Company profile initial commit must use the reviewed null-parent exact tree"
        )
    if company_profile["required_non_empty_fields"] != [
        "name",
        "description",
        "location",
        "blog",
    ]:
        raise PolicyValidationError(
            "Company profile metadata fields must match the reviewed exact set"
        )

    if policy["review_governance"]["minimum_distinct_human_reviewers"] < 1:
        raise PolicyValidationError("At least one distinct human reviewer is required")
    if policy["ruleset"]["pull_request"]["allowed_merge_methods"] != ["squash"]:
        raise PolicyValidationError("Ruleset pull requests must allow squash merges only")
    if policy["ruleset"]["include_refs"] != ["refs/heads/main"]:
        raise PolicyValidationError("Ruleset include refs must target main exactly")
    if policy["ruleset"]["exclude_refs"] != []:
        raise PolicyValidationError("Ruleset must not exclude any protected main ref")
    expected_rule_types = [
        "deletion",
        "non_fast_forward",
        "pull_request",
        "required_linear_history",
        "required_signatures",
        "required_status_checks",
    ]
    if sorted(policy["ruleset"]["required_rule_types"]) != expected_rule_types:
        raise PolicyValidationError("Ruleset rule types must match the reviewed exact set")
    expected_checks = [{"context": "Validate public profile", "integration_id": 15368}]
    if normalized_status_checks(policy["ruleset"]["required_status_checks"]["contexts"]) != expected_checks:
        raise PolicyValidationError(
            "Required status checks must be bound to the reviewed GitHub Actions application"
        )
    legacy_policy = policy["legacy_branch_protection"]
    if legacy_policy["required_in_rollout_phases"] != [
        "pre-reviewer-bootstrap",
        "profile-hardening",
    ]:
        raise PolicyValidationError("Legacy branch protection required phases are unreviewed")
    if legacy_policy["forbidden_in_rollout_phases"] != [
        "proof-publication",
        "target-operating-state",
    ]:
        raise PolicyValidationError("Legacy branch protection forbidden phases are unreviewed")
    expected_legacy_controls = {
        "required_approving_review_count": 1,
        "required_conversation_resolution": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }
    if legacy_policy["minimum_controls"] != expected_legacy_controls:
        raise PolicyValidationError("Legacy branch protection minimum controls are incomplete")
    if policy["review_governance"]["reviewer_access_mode"] != "repository_scoped_direct_collaborator":
        raise PolicyValidationError("Reviewer bootstrap must use repository-scoped direct access")
    if policy["review_governance"]["required_repository_permission"] != "push":
        raise PolicyValidationError("Reviewer repository permission must be exact push access")
    if not policy["review_governance"]["organization_membership_for_review_forbidden"]:
        raise PolicyValidationError("Organization membership cannot be used to bootstrap this reviewer")
    if not policy["review_governance"]["require_effective_access_diff_before_after"]:
        raise PolicyValidationError("Reviewer bootstrap requires a before/after effective-access diff")
    review_status = policy["review_governance"]["current_status"]
    reviewer_login = policy["review_governance"]["independent_reviewer_login"]
    if review_status not in {"APPROVAL_REQUIRED", "VERIFIED"}:
        raise PolicyValidationError(
            "review_governance.current_status must be APPROVAL_REQUIRED or VERIFIED"
        )
    if reviewer_login is not None:
        if not reviewer_login.strip():
            raise PolicyValidationError(
                "independent_reviewer_login must be null or a non-empty GitHub login"
            )
        if reviewer_login.casefold() == policy["founder_profile"]["account"].casefold():
            raise PolicyValidationError(
                "The founder account can never be configured as the independent reviewer"
            )
    if review_status == "VERIFIED":
        if not reviewer_login:
            raise PolicyValidationError(
                "VERIFIED review governance requires a distinct independent_reviewer_login"
            )
        codeowners = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
        validate_codeowners_reviewer(codeowners, reviewer_login)
    if set(policy["security_and_analysis"].values()) != {"enabled"}:
        raise PolicyValidationError("Every public repository security control must target enabled")
    organization_target = policy["organization_governance"]
    expected_organization_target = {
        "default_repository_permission": "none",
        "two_factor_requirement_enabled": True,
        "members_can_create_repositories": False,
        "members_can_create_public_repositories": False,
        "members_can_create_private_repositories": False,
        "members_can_create_internal_repositories": False,
        "members_can_delete_repositories": False,
        "members_can_change_repo_visibility": False,
        "web_commit_signoff_required": True,
        "require_removal_impact_preflight": True,
        "require_effective_access_diff_before_after": True,
        "require_audit_log_evidence": True,
    }
    if organization_target != expected_organization_target:
        raise PolicyValidationError("Organization governance target is incomplete or unreviewed")
    validate_change_control(policy)
    if policy["license_boundary"] != {
        "status": "APPROVAL_REQUIRED_LICENSE_DECISION",
        "no_license_grant": True,
        "decision_scope": ["code", "documentation", "assets", "trademarks"],
    }:
        raise PolicyValidationError("license_boundary must remain fail-closed pending owner decision")
    if policy["promotion_readiness"] != {
        "status": "BLOCKED_PENDING_CONTACT_PATH",
        "approved_contact_url": None,
        "contact_path_requires_owner_approval": True,
        "contact_path_requires_verification": True,
    }:
        raise PolicyValidationError(
            "promotion_readiness must remain blocked until an approved contact URL is verified"
        )


def audit_legacy_branch_protection(
    report: dict[str, Any], policy: dict[str, Any], protection: dict[str, Any] | None
) -> None:
    phase = policy["rollout_phase"]
    legacy_policy = policy["legacy_branch_protection"]
    if phase in legacy_policy["required_in_rollout_phases"] and protection is None:
        add_finding(
            report,
            "legacy_branch_protection.rollout_phase",
            f"present during {phase}",
            None,
            "REPAIR_REQUIRED_LEGACY_PROTECTION_MISSING",
        )
    elif phase in legacy_policy["required_in_rollout_phases"]:
        for key, expected in legacy_policy["minimum_controls"].items():
            compare(
                report,
                f"legacy_branch_protection.minimum_controls.{key}",
                expected,
                protection.get(key),
                "REPAIR_REQUIRED_LEGACY_PROTECTION_WEAK",
            )
    if phase in legacy_policy["forbidden_in_rollout_phases"] and protection is not None:
        add_finding(
            report,
            "legacy_branch_protection.rollout_phase",
            f"absent during {phase}",
            "present",
            "APPROVAL_REQUIRED_LEGACY_PROTECTION_REMOVAL",
        )


def audit_security_controls(
    report: dict[str, Any], policy: dict[str, Any], name_with_owner: str, repo: dict[str, Any]
) -> None:
    expected_controls = policy["security_and_analysis"]
    repo_security = repo.get("security_and_analysis") or {}
    observed: dict[str, str] = {}

    for key in sorted(REPOSITORY_SECURITY_AND_ANALYSIS_KEYS):
        actual = (repo_security.get(key) or {}).get("status", "unavailable")
        observed[key] = actual
        compare(report, f"security_and_analysis.{key}", expected_controls[key], actual)

    binary_endpoints = {
        "vulnerability_alerts": f"repos/{name_with_owner}/vulnerability-alerts",
        "dependabot_security_updates": f"repos/{name_with_owner}/automated-security-fixes",
    }
    for key, endpoint in binary_endpoints.items():
        ok, _, error = gh_json([endpoint])
        if ok:
            actual = "enabled"
        elif error and "404" in error:
            actual = "disabled"
        else:
            actual = "unavailable"
            record_api_error(report, endpoint, error)
        observed[key] = actual
        compare(report, f"security_and_analysis.{key}", expected_controls[key], actual)

    pvr_endpoint = f"repos/{name_with_owner}/private-vulnerability-reporting"
    ok, payload, error = gh_json([pvr_endpoint])
    if ok and isinstance(payload, dict) and isinstance(payload.get("enabled"), bool):
        actual = "enabled" if payload["enabled"] else "disabled"
    elif ok:
        actual = "unavailable"
        add_finding(
            report,
            "security_and_analysis.private_vulnerability_reporting",
            expected_controls["private_vulnerability_reporting"],
            actual,
            "BLOCKED_SECURITY_CONTROL_VISIBILITY",
        )
    else:
        actual = "unavailable"
        record_api_error(report, pvr_endpoint, error)
    observed["private_vulnerability_reporting"] = actual
    if actual != "unavailable":
        compare(
            report,
            "security_and_analysis.private_vulnerability_reporting",
            expected_controls["private_vulnerability_reporting"],
            actual,
        )

    report["observed"]["security_and_analysis"] = observed


def audit_live_codeowners(
    report: dict[str, Any],
    policy: dict[str, Any],
    name_with_owner: str,
    default_branch: str,
    reviewer_login: str,
) -> None:
    endpoint = (
        f"repos/{name_with_owner}/contents/.github/CODEOWNERS?ref={default_branch}"
    )
    ok, payload, error = gh_json([endpoint])
    if not ok:
        record_api_error(
            report,
            endpoint,
            f"BLOCKED_LIVE_CODEOWNERS_UNVERIFIED: {error or 'GitHub API read failed'}",
        )
        add_finding(
            report,
            "review_governance.live_default_branch_codeowners",
            f"every effective rule assigns @{reviewer_login}",
            "unavailable",
            "BLOCKED_LIVE_CODEOWNERS_UNVERIFIED",
        )
        return

    try:
        content = decode_github_content(payload)
        validate_codeowners_reviewer(content, reviewer_login)
    except PolicyValidationError as exc:
        add_finding(
            report,
            "review_governance.live_default_branch_codeowners",
            f"every effective rule assigns @{reviewer_login}",
            str(exc),
            "BLOCKED_LIVE_CODEOWNERS_UNVERIFIED",
        )
        return

    report["observed"]["live_default_branch_codeowners"] = {
        "path": payload.get("path"),
        "sha": payload.get("sha"),
        "ref": default_branch,
        "reviewer_verified": True,
    }


def audit_live_reviewer(
    report: dict[str, Any],
    policy: dict[str, Any],
    name_with_owner: str,
    default_branch: str,
    reviewer_login: str,
) -> None:
    observed: dict[str, Any] = {"configured_login": reviewer_login}
    identity_endpoint = f"users/{reviewer_login}"
    ok, identity, identity_error = gh_json([identity_endpoint])
    if not ok:
        record_api_error(
            report,
            identity_endpoint,
            f"BLOCKED_REVIEWER_IDENTITY_UNVERIFIED: {identity_error or 'GitHub API read failed'}",
        )
        add_finding(
            report,
            "review_governance.independent_reviewer_identity",
            "distinct active human GitHub user",
            "unavailable",
            "BLOCKED_REVIEWER_IDENTITY_UNVERIFIED",
        )
    else:
        identity_payload = identity if isinstance(identity, dict) else {}
        observed.update(
            {
                "canonical_login": identity_payload.get("login"),
                "account_type": identity_payload.get("type"),
                "suspended": identity_payload.get("suspended_at") is not None
                and identity_payload.get("suspended_at") != "",
            }
        )
        identity_problem = reviewer_identity_problem(policy, reviewer_login, identity)
        if identity_problem:
            add_finding(
                report,
                "review_governance.independent_reviewer_identity",
                "distinct active human GitHub user",
                identity_problem,
                "BLOCKED_REVIEWER_IDENTITY_UNVERIFIED",
            )

    permission_endpoint = f"repos/{name_with_owner}/collaborators/{reviewer_login}/permission"
    ok, permission_payload, permission_error = gh_json([permission_endpoint])
    if not ok:
        record_api_error(
            report,
            permission_endpoint,
            f"BLOCKED_REVIEWER_PERMISSION_UNVERIFIED: {permission_error or 'GitHub API read failed'}",
        )
    else:
        permission = (
            permission_payload.get("permission")
            if isinstance(permission_payload, dict)
            else None
        )
        expected_permission = policy["review_governance"]["required_repository_permission"]
        observed["permission"] = permission
        if permission != expected_permission:
            add_finding(
                report,
                "review_governance.independent_reviewer_permission",
                expected_permission,
                permission,
                "BLOCKED_REVIEWER_ACCESS_BLAST_RADIUS",
            )

    membership_endpoint = (
        f"orgs/{policy['company_profile']['organization']}/memberships/{reviewer_login}"
    )
    membership_ok, membership, membership_error = gh_json([membership_endpoint])
    if membership_ok:
        observed["organization_membership"] = (membership or {}).get("state", "member")
        add_finding(
            report,
            "review_governance.organization_membership_for_review_forbidden",
            "reviewer is not an organization member",
            observed["organization_membership"],
            "BLOCKED_REVIEWER_ACCESS_BLAST_RADIUS",
        )
    elif membership_error and "404" in membership_error:
        observed["organization_membership"] = "absent"
    else:
        record_api_error(report, membership_endpoint, membership_error)

    report["observed"]["independent_reviewer"] = observed
    audit_live_codeowners(
        report,
        policy,
        name_with_owner,
        default_branch,
        reviewer_login,
    )


def audit_repository(report: dict[str, Any], policy: dict[str, Any]) -> None:
    repository_policy = policy["repository"]
    name_with_owner = repository_policy["name_with_owner"]
    owner, repository = name_with_owner.split("/", 1)

    ok, viewer, error = gh_json(["user"])
    if not ok:
        record_api_error(report, "user", error)
    else:
        authenticated_login = viewer.get("login") if isinstance(viewer, dict) else None
        expected_login = policy["founder_profile"]["account"]
        actor_matches = authenticated_login == expected_login
        report["observed"]["authenticated_login"] = authenticated_login
        report["observed"]["audit_actor_matches_profile_subject"] = actor_matches
        if not actor_matches:
            add_finding(
                report,
                "identity.audit_actor_matches_profile_subject",
                expected_login,
                authenticated_login,
                "BLOCKED_AUDIT_ACTOR_PROFILE_SUBJECT_MISMATCH",
            )

    ok, repo, error = gh_json([f"repos/{name_with_owner}"])
    if not ok:
        record_api_error(report, f"repos/{name_with_owner}", error)
        return

    report["observed"]["repository"] = {
        "name_with_owner": repo.get("full_name"),
        "visibility": repo.get("visibility"),
        "default_branch": repo.get("default_branch"),
        "archived": repo.get("archived"),
        "topics": sorted(repo.get("topics") or []),
    }

    compare(report, "repository.name_with_owner", name_with_owner, repo.get("full_name"))
    compare(report, "repository.visibility", repository_policy["visibility"], repo.get("visibility"))
    compare(report, "repository.default_branch", repository_policy["default_branch"], repo.get("default_branch"))
    compare(report, "repository.archived", repository_policy["archived"], repo.get("archived"))

    actual_topics = set(repo.get("topics") or [])
    missing_topics = sorted(set(repository_policy["required_topics"]) - actual_topics)
    if missing_topics:
        add_finding(report, "repository.required_topics", [], missing_topics)

    for key, expected in policy["repository_features"].items():
        compare(report, f"repository_features.{key}", expected, repo.get(key))

    for key, expected in policy["merge_policy"].items():
        compare(report, f"merge_policy.{key}", expected, repo.get(key))

    reviewer = policy["review_governance"].get("independent_reviewer_login")
    if policy["review_governance"]["current_status"] == "VERIFIED" and reviewer:
        audit_live_reviewer(
            report,
            policy,
            name_with_owner,
            repository_policy["default_branch"],
            reviewer,
        )

    audit_security_controls(report, policy, name_with_owner, repo)

    default_branch = repository_policy["default_branch"]
    ok, protection, protection_error = gh_json(
        [f"repos/{name_with_owner}/branches/{default_branch}/protection"]
    )
    if ok:
        pull_request = protection.get("required_pull_request_reviews") or {}
        status_checks = protection.get("required_status_checks") or {}
        observed_protection = {
            "required_approving_review_count": pull_request.get("required_approving_review_count"),
            "dismiss_stale_reviews": pull_request.get("dismiss_stale_reviews"),
            "require_code_owner_reviews": pull_request.get("require_code_owner_reviews"),
            "require_last_push_approval": pull_request.get("require_last_push_approval"),
            "required_status_contexts": sorted(status_checks.get("contexts") or []),
            "enforce_admins": (protection.get("enforce_admins") or {}).get("enabled"),
            "required_conversation_resolution": (
                protection.get("required_conversation_resolution") or {}
            ).get("enabled"),
            "required_linear_history": (protection.get("required_linear_history") or {}).get("enabled"),
            "allow_force_pushes": (protection.get("allow_force_pushes") or {}).get("enabled"),
            "allow_deletions": (protection.get("allow_deletions") or {}).get("enabled"),
        }
        report["observed"]["legacy_branch_protection"] = observed_protection
        audit_legacy_branch_protection(report, policy, observed_protection)
    elif protection_error and "404" not in protection_error:
        record_api_error(
            report,
            f"repos/{name_with_owner}/branches/{default_branch}/protection",
            protection_error,
        )
    else:
        report["observed"]["legacy_branch_protection"] = None
        audit_legacy_branch_protection(report, policy, None)

    audit_ruleset(report, policy, owner, repository)

    ok, community, error = gh_json([f"repos/{name_with_owner}/community/profile"])
    if not ok:
        record_api_error(report, f"repos/{name_with_owner}/community/profile", error)
    else:
        actual_health = community.get("health_percentage")
        report["observed"]["community_health_percentage"] = actual_health
        minimum_health = policy["community"]["minimum_health_percentage"]
        if not isinstance(actual_health, int) or actual_health < minimum_health:
            add_finding(
                report,
                "community.minimum_health_percentage",
                f">={minimum_health}",
                actual_health,
            )


def audit_ruleset(
    report: dict[str, Any], policy: dict[str, Any], owner: str, repository: str
) -> None:
    ruleset_policy = policy["ruleset"]
    endpoint = f"repos/{owner}/{repository}/rulesets"
    ok, rulesets, error = gh_json([endpoint])
    if not ok:
        record_api_error(report, endpoint, error)
        return

    named = next(
        (item for item in rulesets if item.get("name") == ruleset_policy["name"]),
        None,
    )
    if not named:
        report["observed"]["ruleset"] = None
        add_finding(report, "ruleset.name", ruleset_policy["name"], None)
        return

    ruleset_id = named.get("id")
    ok, ruleset, error = gh_json([f"{endpoint}/{ruleset_id}"])
    if not ok:
        record_api_error(report, f"{endpoint}/{ruleset_id}", error)
        return

    rule_types = sorted(rule.get("type") for rule in ruleset.get("rules") or [])
    included_refs = sorted(
        ((ruleset.get("conditions") or {}).get("ref_name") or {}).get("include") or []
    )
    excluded_refs = sorted(
        ((ruleset.get("conditions") or {}).get("ref_name") or {}).get("exclude") or []
    )
    bypass_visible = "bypass_actors" in ruleset
    bypass_count = len(ruleset["bypass_actors"] or []) if bypass_visible else None
    if not bypass_visible:
        record_api_error(
            report,
            f"{endpoint}/{ruleset_id}",
            "BLOCKED_RULESET_BYPASS_VISIBILITY: GitHub omitted bypass_actors; zero bypass cannot be proven",
        )
    report["observed"]["ruleset"] = {
        "id": ruleset_id,
        "name": ruleset.get("name"),
        "target": ruleset.get("target"),
        "enforcement": ruleset.get("enforcement"),
        "include_refs": included_refs,
        "exclude_refs": excluded_refs,
        "bypass_actor_count": bypass_count,
        "rule_types": rule_types,
    }

    compare(report, "ruleset.target", ruleset_policy["target"], ruleset.get("target"))
    compare(report, "ruleset.enforcement", ruleset_policy["enforcement"], ruleset.get("enforcement"))
    compare(report, "ruleset.include_refs", sorted(ruleset_policy["include_refs"]), included_refs)
    compare(report, "ruleset.exclude_refs", sorted(ruleset_policy["exclude_refs"]), excluded_refs)
    if bypass_count is not None and bypass_count > ruleset_policy["maximum_bypass_actors"]:
        add_finding(
            report,
            "ruleset.maximum_bypass_actors",
            ruleset_policy["maximum_bypass_actors"],
            bypass_count,
        )

    compare(
        report,
        "ruleset.required_rule_types",
        sorted(ruleset_policy["required_rule_types"]),
        rule_types,
    )

    rules_by_type = {rule.get("type"): rule for rule in ruleset.get("rules") or []}
    pull_request_rule = rules_by_type.get("pull_request") or {}
    pull_request_parameters = pull_request_rule.get("parameters") or {}
    for key, expected in ruleset_policy["pull_request"].items():
        compare(
            report,
            f"ruleset.pull_request.{key}",
            expected,
            pull_request_parameters.get(key),
        )

    checks_rule = rules_by_type.get("required_status_checks") or {}
    checks_parameters = checks_rule.get("parameters") or {}
    expected_checks = ruleset_policy["required_status_checks"]
    compare(
        report,
        "ruleset.required_status_checks.strict_required_status_checks_policy",
        expected_checks["strict_required_status_checks_policy"],
        checks_parameters.get("strict_required_status_checks_policy"),
    )
    actual_contexts = normalized_status_checks(
        checks_parameters.get("required_status_checks")
    )
    expected_contexts = normalized_status_checks(expected_checks["contexts"])
    compare(
        report,
        "ruleset.required_status_checks.contexts",
        expected_contexts,
        actual_contexts,
    )
    report["observed"]["ruleset"]["required_status_checks"] = actual_contexts


def minimum_pins_for_phase(policy: dict[str, Any]) -> int:
    if policy["rollout_phase"] in {"proof-publication", "target-operating-state"}:
        return policy["founder_profile"]["minimum_pinned_repositories_target_phase"]
    return policy["founder_profile"]["minimum_pinned_repositories_current_phase"]


def audit_profiles(report: dict[str, Any], policy: dict[str, Any]) -> None:
    founder = policy["founder_profile"]
    account = founder["account"]
    ok, profile, error = gh_json([f"users/{account}"])
    if not ok:
        record_api_error(report, f"users/{account}", error)
    else:
        completeness = {
            field: bool(profile.get(field))
            for field in founder["required_non_empty_fields"]
        }
        report["observed"]["founder_profile_fields_present"] = completeness
        for field, present in completeness.items():
            if not present:
                add_finding(report, f"founder_profile.{field}", "non-empty", None)

    query = (
        "query($login:String!){user(login:$login){pinnedItems(first:6,types:[REPOSITORY])"
        "{totalCount nodes{... on Repository{nameWithOwner}}}}}"
    )
    ok, pins_payload, error = gh_json(
        ["graphql", "-f", f"query={query}", "-F", f"login={account}"]
    )
    if not ok:
        record_api_error(report, "graphql:user.pinnedItems", error)
    else:
        pinned = ((pins_payload.get("data") or {}).get("user") or {}).get("pinnedItems") or {}
        count = pinned.get("totalCount")
        names = sorted(
            node.get("nameWithOwner")
            for node in pinned.get("nodes") or []
            if node.get("nameWithOwner")
        )
        report["observed"]["pinned_repositories"] = names
        minimum = minimum_pins_for_phase(policy)
        maximum = founder["maximum_pinned_repositories"]
        if not isinstance(count, int) or count < minimum or count > maximum:
            add_finding(report, "founder_profile.pinned_repository_count", f"{minimum}..{maximum}", count)

    company = policy["company_profile"]
    organization = company["organization"]
    ok, organization_payload, error = gh_json([f"orgs/{organization}"])
    if not ok:
        record_api_error(report, f"orgs/{organization}", error)
    else:
        completeness = {
            field: bool(organization_payload.get(field))
            for field in company["required_non_empty_fields"]
        }
        report["observed"]["company_profile_fields_present"] = completeness
        for field, present in completeness.items():
            if not present:
                add_finding(report, f"company_profile.{field}", "non-empty", None)
        organization_target = policy["organization_governance"]
        observed_controls: dict[str, Any] = {}
        for key in sorted(ORGANIZATION_LIVE_CONTROL_KEYS):
            if key not in organization_payload:
                observed_controls[key] = "unavailable"
                add_finding(
                    report,
                    f"organization_governance.{key}",
                    organization_target[key],
                    "unavailable",
                    "BLOCKED_ORGANIZATION_CONTROL_VISIBILITY",
                )
                continue
            actual = organization_payload[key]
            observed_controls[key] = actual
            compare(report, f"organization_governance.{key}", organization_target[key], actual)
        report["observed"]["organization_governance"] = observed_controls

    profile_repository = company["public_profile_repository"]
    ok, profile_repo, error = gh_json([f"repos/{profile_repository}"])
    if not ok:
        if error and "404" in error:
            report["observed"]["company_profile_repository"] = None
            add_finding(report, "company_profile.public_profile_repository", profile_repository, None)
        else:
            record_api_error(report, f"repos/{profile_repository}", error)
    else:
        actual = profile_repo.get("full_name")
        report["observed"]["company_profile_repository"] = actual
        compare(report, "company_profile.public_profile_repository", profile_repository, actual)
        compare(report, "company_profile.repository_visibility", "public", profile_repo.get("visibility"))
        compare(
            report,
            "company_profile.default_branch",
            company["default_branch"],
            profile_repo.get("default_branch"),
        )

        default_branch = company["default_branch"]
        readme_endpoint = f"repos/{profile_repository}/contents/profile/README.md?ref={default_branch}"
        ok, readme_payload, readme_error = gh_json([readme_endpoint])
        if not ok:
            if readme_error and "404" in readme_error:
                report["observed"]["company_profile_readme"] = None
                add_finding(
                    report,
                    "company_profile.profile_readme",
                    "profile/README.md",
                    None,
                    "REPAIR_REQUIRED",
                )
            else:
                record_api_error(report, readme_endpoint, readme_error)
        else:
            report["observed"]["company_profile_readme"] = readme_payload.get("path")
            encoded_content = readme_payload.get("content")
            decoded_content = ""
            if readme_payload.get("encoding") == "base64" and isinstance(encoded_content, str):
                try:
                    decoded_content = base64.b64decode(encoded_content).decode("utf-8")
                except (ValueError, UnicodeError):
                    decoded_content = ""
            if not decoded_content.strip() or "Aureus Automation Lab" not in decoded_content:
                add_finding(
                    report,
                    "company_profile.profile_readme_identity",
                    "non-empty profile/README.md containing Aureus Automation Lab",
                    "missing or invalid",
                    "REPAIR_REQUIRED",
                )


def finalize_status(report: dict[str, Any]) -> int:
    if report["api_errors"]:
        known_api_blockers = (
            "BLOCKED_GITHUB_API_TIMEOUT",
            "BLOCKED_RULESET_BYPASS_VISIBILITY",
            "BLOCKED_LIVE_CODEOWNERS_UNVERIFIED",
            "BLOCKED_REVIEWER_IDENTITY_UNVERIFIED",
            "BLOCKED_REVIEWER_PERMISSION_UNVERIFIED",
        )
        report["status"] = next(
            (
                blocker
                for blocker in known_api_blockers
                if any(blocker in item.get("error", "") for item in report["api_errors"])
            ),
            "BLOCKED_GITHUB_READ_ONLY_AUDIT",
        )
        return 3
    if report["findings"]:
        dispositions = {finding["disposition"] for finding in report["findings"]}
        blockers = sorted(value for value in dispositions if value.startswith("BLOCKED"))
        if blockers:
            report["blockers"] = blockers
            report["status"] = (
                blockers[0] if len(blockers) == 1 else "BLOCKED_MULTIPLE_PREREQUISITES"
            )
            return 3
        has_repair = any(value.startswith("REPAIR_REQUIRED") for value in dispositions)
        has_approval = any(value.startswith("APPROVAL_REQUIRED") for value in dispositions)
        if has_repair and has_approval:
            report["status"] = "REPAIR_REQUIRED_AND_APPROVAL_REQUIRED"
        elif has_repair:
            report["status"] = "REPAIR_REQUIRED"
        else:
            report["status"] = "APPROVAL_REQUIRED"
        return 2
    report["status"] = "PASS"
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only drift audit for the Aureus public GitHub governance baseline."
    )
    parser.add_argument("--json", action="store_true", help="Print the complete JSON report")
    args = parser.parse_args()

    try:
        policy = load_policy()
    except (OSError, UnicodeError, json.JSONDecodeError, PolicyValidationError) as exc:
        report = {
            "schema_version": "1.0",
            "status": "BLOCKED_INVALID_LOCAL_POLICY",
            "error": str(exc),
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 3

    report: dict[str, Any] = {
        "schema_version": "1.0",
        "audit_type": "read-only",
        "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "policy_id": policy["policy_id"],
        "repository": policy["repository"]["name_with_owner"],
        "status": "PENDING",
        "observed": {},
        "findings": [],
        "api_errors": [],
        "next_action": (
            "Use the approval packet for any selected live repair; this audit never mutates GitHub."
        ),
    }

    review_status = policy["review_governance"]["current_status"]
    if review_status != "VERIFIED":
        add_finding(
            report,
            "review_governance.current_status",
            "VERIFIED",
            review_status,
            "APPROVAL_REQUIRED",
        )

    audit_repository(report, policy)
    audit_profiles(report, policy)
    exit_code = finalize_status(report)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"PUBLIC_GITHUB_STATE_AUDIT: {report['status']}")
        print(f"Findings: {len(report['findings'])}")
        print(f"API errors: {len(report['api_errors'])}")
        for finding in report["findings"]:
            print(
                f"- {finding['control']}: expected={finding['expected']!r}; "
                f"actual={finding['actual']!r}; {finding['disposition']}"
            )
        for api_error in report["api_errors"]:
            print(f"- {api_error['endpoint']}: {api_error['error']}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
