from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def marker(*parts: str) -> str:
    return "".join(parts)


REQUIRED_FILES = [
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/governance/public-profile-policy.json",
    ".github/governance/public-profile-policy.schema.json",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/public-profile-feedback.yml",
    ".github/pull_request_template.md",
    ".github/workflows/public-profile-validation.yml",
    "docs/portfolio/public-demo-flow.md",
    "docs/portfolio/synthetic-demo-case.md",
    "docs/portfolio/cv-usage.md",
    "docs/portfolio/offer-menu.md",
    "docs/portfolio/capabilities.md",
    "docs/portfolio/case-studies.md",
    "docs/portfolio/project-map.md",
    "docs/portfolio/naming-system.md",
    "docs/portfolio/credentials.md",
    "docs/portfolio/review-guide.md",
    "docs/portfolio/public-portfolio-scorecard.md",
    "docs/portfolio/github-portfolio-standard.md",
    "docs/profile/github-governance-approval-packet.md",
    "docs/profile/github-identity-transition.md",
    "docs/profile/quality-rubric.md",
    "docs/profile/readiness-check.md",
    "docs/profile/public-release-audit.md",
    "docs/proof/finecon-source-backed-status.md",
    "public-proof/portfolio-manifest.json",
    "public-proof/aureus-crm-operations/README.md",
    "public-proof/aureus-crm-operations/architecture.md",
    "public-proof/aureus-crm-operations/state-and-audit-model.md",
    "public-proof/aureus-crm-operations/validation-boundary.md",
    "public-proof/aureus-finecon/README.md",
    "public-proof/aureus-sales-workflow/README.md",
    "public-proof/aureus-trading-infrastructure/README.md",
    "public-proof/aureus-trading-infrastructure/risk-boundary.md",
    "scripts/audit-public-github-state.py",
    "scripts/test-audit-public-github-state.py",
    "scripts/validate-local-json-schema.py",
    "assets/aureus-profile-hero.gif",
    "assets/aureus-offer-menu.gif",
    "assets/aureus-sales-workflow.gif",
    "assets/aureus-finecon-flow.gif",
    "assets/aureus-os-model.gif",
    "assets/aureus-public-boundary.gif",
    "assets/aureus-capability-system.gif",
    "assets/aureus-collaboration-flow.gif",
    "assets/aureus-proof-pack.gif",
    "assets/aureus-readiness-check.gif",
    "assets/aureus-solution-architecture.gif",
]

FORBIDDEN_LEGACY_PATHS = [
    "public-proof/crm-platform",
    "public-proof/finecon",
    "public-proof/sales-machine",
    "public-proof/trading-infrastructure",
]

README_REQUIRED = [
    "Founder & AI Automation Solution Architect",
    "Controlled AI automation",
    "docs/portfolio/public-demo-flow.md",
    "docs/portfolio/synthetic-demo-case.md",
    "docs/portfolio/offer-menu.md",
    "docs/portfolio/cv-usage.md",
    "docs/portfolio/project-map.md",
    "docs/portfolio/naming-system.md",
    "docs/portfolio/credentials.md",
    "docs/portfolio/github-portfolio-standard.md",
    "public-proof/portfolio-manifest.json",
    "public-proof/aureus-crm-operations/README.md",
    "public-proof/aureus-trading-infrastructure/README.md",
]

FILE_REQUIRED = {
    "CODE_OF_CONDUCT.md": ["Our Standard", "Reporting And Enforcement"],
    "CONTRIBUTING.md": ["PR-first workflow", "validate-public-portfolio.py", "Review Boundary"],
    "SECURITY.md": ["Reporting A Vulnerability", "Do not open a public issue", "Sensitive Material"],
    "SUPPORT.md": ["public-profile feedback", "not a production support channel"],
    ".github/CODEOWNERS": ["@Aureus-Automation-Lab"],
    ".github/dependabot.yml": ["package-ecosystem: github-actions"],
    ".github/ISSUE_TEMPLATE/config.yml": ["blank_issues_enabled: false"],
    ".github/ISSUE_TEMPLATE/public-profile-feedback.yml": ["Public profile feedback", "Safety confirmation"],
    ".github/pull_request_template.md": ["Claim, Security, And Privacy Review", "Release And Rollback"],
    ".github/workflows/public-profile-validation.yml": [
        "permissions:",
        "contents: read",
        "persist-credentials: false",
        "concurrency:",
        "timeout-minutes:",
        "validate-public-portfolio.py",
        "validate-aureus-use-case-showcase.py",
        "test-audit-public-github-state.py",
    ],
    ".github/governance/public-profile-policy.json": [
        "aureus-public-profile-governance",
        "pre-reviewer-bootstrap",
        "APPROVAL_REQUIRED",
        "change_control",
        "sensitive_execution_contract",
        "aureus-main-governance",
    ],
    "scripts/audit-public-github-state.py": [
        "read-only drift audit",
        "BLOCKED_GITHUB_API_TIMEOUT",
        "validate_policy",
    ],
    "docs/portfolio/capabilities.md": [
        "Best-Fit Roles",
        "Aureus CRM Operations",
        "Aureus FinEcon",
        "Aureus Sales Workflow",
    ],
    "docs/portfolio/project-map.md": [
        "Aureus OS",
        "Aureus CRM Operations",
        "Aureus FinEcon",
        "Aureus Trading Infrastructure",
    ],
    "docs/portfolio/naming-system.md": [
        "Canonical Hierarchy",
        "Only Aureus OS is an operating system",
        "Legacy Alias Register",
        "Aureus CRM Operations",
        "Aureus FinEcon",
        "Aureus Sales Workflow",
        "Aureus Trading Infrastructure",
    ],
    "docs/portfolio/credentials.md": [
        "IBM AI Engineering Professional Certificate",
        "13 courses",
        "Professional, non-credit certificate",
    ],
    "docs/portfolio/case-studies.md": [
        "Engineering Proof Scenarios",
        "Automation Audit",
        "Aureus Sales Workflow",
        "Aureus FinEcon",
        "Git-Backed LinkedIn Content",
        "Monthly Automation Partner",
        "Aureus CRM Operations",
        "Aureus Trading Infrastructure",
    ],
    "docs/portfolio/review-guide.md": ["CV"],
    "docs/portfolio/offer-menu.md": ["Recommended first purchase"],
    "docs/portfolio/github-portfolio-standard.md": [
        "Identity Architecture",
        "Public Repository Contract",
        "Branch And Merge Baseline",
        "Security And Automation Baseline",
        "Objective Status Model",
        "Promotion Gate",
        "Policy As Code And Drift Detection",
    ],
    "docs/portfolio/public-portfolio-scorecard.md": [
        "Public Portfolio Readiness Matrix",
        "REPAIR_REQUIRED",
        "APPROVAL_REQUIRED",
        "APPROVAL_REQUIRED_LICENSE_DECISION",
        "BLOCKED_PENDING_CONTACT_PATH",
    ],
    "docs/profile/github-governance-approval-packet.md": [
        "Public Governance Baseline",
        "Desired-State Controls",
        "Recommended Rollout",
        "Approval Boundary",
        "Required Evidence",
        "Change-Control Boundary",
        "APPROVAL_REQUIRED",
        "sensitive execution contract remains private",
    ],
    "docs/profile/quality-rubric.md": ["Public GitHub Trust Standard", "Automatic No-Go"],
    "docs/proof/finecon-source-backed-status.md": [
        "Pocket document intake",
        "accountant validation",
        "does not claim",
    ],
    "public-proof/aureus-crm-operations/README.md": [
        "Aureus CRM Operations",
        "49 changed files",
        "21,472 added lines",
        "source-backed full-stack synthetic product proof",
    ],
    "public-proof/aureus-crm-operations/state-and-audit-model.md": [
        "ReservationsReleased",
        "Concrete Inventory Invariant",
    ],
    "public-proof/aureus-trading-infrastructure/README.md": [
        "paper-run",
        "isolated executor",
        "not financial advice",
    ],
    "public-proof/aureus-finecon/README.md": [
        "Aureus FinEcon Public Proof",
        "accounting review",
    ],
    "public-proof/aureus-sales-workflow/README.md": [
        "Aureus Sales Workflow Public Proof",
        "subordinate Aureus scenario",
    ],
}

PRIMARY_NAMING_SURFACES = [
    "README.md",
    "docs/portfolio/project-map.md",
    "public-proof/README.md",
    "docs/proof/proof-index.md",
]

CANONICAL_PUBLIC_NAMES = [
    "Aureus OS",
    "Aureus CRM Operations",
    "Aureus FinEcon",
    "Aureus Trading Infrastructure",
]

EXPECTED_PORTFOLIO = {
    "aureus-os-reference": {
        "canonical_name": "Aureus OS",
        "proof_package": "public-proof/aureus-os",
        "kind": "public-reference",
        "target_repository": "AureusAutomationLab/aureus-os-reference",
        "maturity": "source-backed-architecture",
        "publication_status": "sanitized-candidate",
        "founder_pin_order": 2,
        "organization_pin_order": 2,
    },
    "aureus-crm-operations": {
        "canonical_name": "Aureus CRM Operations",
        "proof_package": "public-proof/aureus-crm-operations",
        "kind": "public-product-proof",
        "target_repository": "AureusAutomationLab/aureus-crm-operations",
        "maturity": "source-backed-synthetic-demo",
        "publication_status": "sanitized-candidate",
        "founder_pin_order": 1,
        "organization_pin_order": 1,
    },
    "aureus-finecon-reference": {
        "canonical_name": "Aureus FinEcon",
        "proof_package": "public-proof/aureus-finecon",
        "kind": "public-reference",
        "target_repository": "AureusAutomationLab/aureus-finecon-reference",
        "maturity": "source-backed-workflow-reference",
        "publication_status": "sanitized-candidate",
        "founder_pin_order": 3,
        "organization_pin_order": 3,
    },
    "aureus-trading-infrastructure-reference": {
        "canonical_name": "Aureus Trading Infrastructure",
        "proof_package": "public-proof/aureus-trading-infrastructure",
        "kind": "public-reference",
        "target_repository": "AureusAutomationLab/aureus-trading-infrastructure-reference",
        "maturity": "paper-run-architecture",
        "publication_status": "sanitized-candidate",
        "founder_pin_order": 4,
        "organization_pin_order": 4,
    },
    "aureus-sales-workflow": {
        "canonical_name": "Aureus Sales Workflow",
        "proof_package": "public-proof/aureus-sales-workflow",
        "kind": "embedded-scenario",
        "target_repository": None,
        "maturity": "synthetic-workflow-scenario",
        "publication_status": "embedded-only",
        "founder_pin_order": None,
        "organization_pin_order": None,
    },
}

ALLOWED_PUBLICATION_STATUSES = {"sanitized-candidate", "embedded-only"}
ALLOWED_MATURITY = {
    "source-backed-architecture",
    "source-backed-synthetic-demo",
    "source-backed-workflow-reference",
    "paper-run-architecture",
    "synthetic-workflow-scenario",
}
ALLOWED_KINDS = {"public-reference", "public-product-proof", "embedded-scenario"}

LEGACY_ALIAS_ALLOWLIST = {
    "docs/portfolio/naming-system.md",
}

LEGACY_PRIMARY_NAMES = [
    marker("FinEcon Pocket", " / Bridge"),
    marker("Approval-Safe", " Aureus Sales Workflow"),
    marker("Sales", " Machine"),
]

FORBIDDEN_PHRASES = [
    marker("guar", "anteed", " ROI"),
    marker("proven", " revenue"),
    marker("world", "-class"),
    marker("best in", " the world"),
    marker("enterprise", "-grade"),
    marker("SOC 2", " certified"),
    marker("production", " proven"),
]

FORBIDDEN_PATTERNS = [
    re.compile(r"\bworld[ -]class\b", re.IGNORECASE),
    re.compile(r"\bbest\s+in\s+the\s+world\b", re.IGNORECASE),
    re.compile(r"\benterprise[ -]grade\b", re.IGNORECASE),
]

STALE_STATE_PHRASES = [
    marker("repository must remain ", "private until"),
    marker("switching the repository ", "to public"),
    marker("before switching the profile repository ", "from private to public"),
    marker("before making the profile ", "public"),
    marker("manual steps to make the profile repo ", "public"),
]

SECRET_MARKERS = [
    marker("OPENAI", "_API_KEY", "="),
    marker("GITHUB", "_TOKEN", "="),
    marker("N8N", "_API_KEY", "="),
    marker("password", "="),
    marker("secret", "="),
    marker("webhook", ".site"),
    marker("localhost", ":"),
    marker("127", ".0.0.1"),
]

MOJIBAKE_MARKERS = [
    "\u0102",
    "\u00e2\u20ac",
    "\ufffd",
]

SELF_RATING_PATTERN = re.compile(r"\b\d+(?:\.\d+)?/10(?:\+)?\b", re.IGNORECASE)
ACTION_REF_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
WINDOWS_ABSOLUTE_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")
HOST_SPECIFIC_ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"(?i)\b[A-Za-z]:[\\/]+Users[\\/]+"),
    re.compile(re.escape(marker("/", "Users", "/"))),
    re.compile(re.escape(marker("/", "home", "/"))),
)
SECRET_VALUE_PATTERNS = [
    re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|client[_-]?secret)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=:-]{16,}"
    ),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
]


def iter_text_files():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError("git ls-files failed while building the validation boundary")

    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        rel = raw_path.decode("utf-8", errors="strict")
        path = ROOT / rel
        if not path.is_file():
            continue
        if path.name in {
            "audit-public-github-state.py",
            "test-audit-public-github-state.py",
        }:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc", ".pdf"}:
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def host_specific_absolute_path_matches(content: str) -> list[str]:
    """Return public-host path prefixes that would leak workstation layout."""
    return [
        match.group(0)
        for pattern in HOST_SPECIFIC_ABSOLUTE_PATH_PATTERNS
        for match in pattern.finditer(content)
    ]


def validate_manifest(errors: list[str]) -> None:
    path = ROOT / "public-proof/portfolio-manifest.json"
    try:
        manifest = json.loads(read_text(path))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"Portfolio manifest is not valid JSON: {exc}")
        return

    if manifest.get("schema_version") != "1.0":
        errors.append("Portfolio manifest schema_version must be 1.0")

    verified_date = manifest.get("last_verified_date")
    try:
        verified = date.fromisoformat(verified_date)
    except (TypeError, ValueError):
        errors.append("Portfolio manifest last_verified_date must be an ISO date")
    else:
        age_days = (date.today() - verified).days
        if age_days < 0:
            errors.append("Portfolio manifest last_verified_date cannot be in the future")
        elif age_days > 90:
            errors.append("Portfolio manifest live assumptions are older than 90 days and must be refreshed")

    identity = manifest.get("canonical_identity", {})
    expected_identity = {
        "company": "Aureus Automation Lab",
        "company_organization": "AureusAutomationLab",
        "current_profile_account": "Aureus-Automation-Lab",
        "current_profile_repository": "Aureus-Automation-Lab/Aureus-Automation-Lab",
        "identity_state": "canonical-public-identity",
    }
    for key, expected in expected_identity.items():
        if identity.get(key) != expected:
            errors.append(f"Portfolio manifest canonical_identity.{key} must equal {expected!r}")

    governance_state = manifest.get("governance_state", {})
    if governance_state != {
        "rollout_phase": "pre-reviewer-bootstrap",
        "status": "APPROVAL_REQUIRED",
    }:
        errors.append(
            "Portfolio manifest governance_state must remain pre-reviewer-bootstrap and APPROVAL_REQUIRED"
        )

    company_profile = manifest.get("company_profile", {})
    if company_profile.get("target_repository") != "AureusAutomationLab/.github":
        errors.append("Portfolio manifest company profile target must be AureusAutomationLab/.github")
    if company_profile.get("publication_status") != "approval-required":
        errors.append("Portfolio manifest company profile must remain approval-required until published")

    items = manifest.get("portfolio_items")
    if not isinstance(items, list):
        errors.append("Portfolio manifest portfolio_items must be a list")
        return

    by_id: dict[str, dict] = {}
    target_repositories: set[str] = set()
    founder_pin_orders: set[int] = set()
    organization_pin_orders: set[int] = set()

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"Portfolio manifest item {index} must be an object")
            continue

        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"Portfolio manifest item {index} has no valid id")
            continue
        if item_id in by_id:
            errors.append(f"Portfolio manifest contains duplicate id: {item_id}")
        by_id[item_id] = item

        if item.get("publication_status") not in ALLOWED_PUBLICATION_STATUSES:
            errors.append(f"Portfolio manifest item {item_id} has invalid publication_status")
        if item.get("maturity") not in ALLOWED_MATURITY:
            errors.append(f"Portfolio manifest item {item_id} has invalid maturity")
        if item.get("kind") not in ALLOWED_KINDS:
            errors.append(f"Portfolio manifest item {item_id} has invalid kind")

        lineage = item.get("source_lineage")
        if not isinstance(lineage, dict):
            errors.append(f"Portfolio manifest item {item_id} must contain source_lineage")
        else:
            if not isinstance(lineage.get("evidence_id"), str) or not lineage.get("evidence_id"):
                errors.append(f"Portfolio manifest item {item_id} source_lineage.evidence_id is required")
            tree_hash = lineage.get("source_tree_hash")
            if tree_hash is not None and not re.fullmatch(r"[0-9a-f]{40}", str(tree_hash)):
                errors.append(f"Portfolio manifest item {item_id} source_tree_hash must be null or a Git SHA")
            publication_gate = lineage.get("publication_gate")
            if publication_gate not in {"PASS", "APPROVAL_REQUIRED"}:
                errors.append(
                    f"Portfolio manifest item {item_id} source_lineage.publication_gate is invalid"
                )
            if (
                item.get("publication_status") == "sanitized-candidate"
                and publication_gate != "APPROVAL_REQUIRED"
            ):
                errors.append(
                    f"Portfolio manifest item {item_id} sanitized candidates must remain APPROVAL_REQUIRED"
                )

        target_state = item.get("target_state")
        if not isinstance(target_state, dict):
            errors.append(f"Portfolio manifest item {item_id} must contain target_state")
        else:
            if type(target_state.get("exists")) is not bool:
                errors.append(f"Portfolio manifest item {item_id} target_state.exists must be boolean")
            if target_state.get("visibility") not in {None, "public", "private", "internal"}:
                errors.append(f"Portfolio manifest item {item_id} target_state.visibility is invalid")

        if item.get("gate_status") not in {"PASS", "REPAIR_REQUIRED", "APPROVAL_REQUIRED", "BLOCKED"}:
            errors.append(f"Portfolio manifest item {item_id} gate_status is invalid")

        proof_package = item.get("proof_package")
        if not isinstance(proof_package, str) or not proof_package.startswith("public-proof/"):
            errors.append(f"Portfolio manifest item {item_id} has invalid proof_package")
        else:
            proof_path = (ROOT / proof_package).resolve()
            try:
                proof_path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"Portfolio manifest item {item_id} proof_package escapes repository")
            if not proof_path.is_dir():
                errors.append(f"Portfolio manifest item {item_id} proof_package does not exist: {proof_package}")

        target_repository = item.get("target_repository")
        if target_repository is not None:
            if not isinstance(target_repository, str) or not target_repository.startswith("AureusAutomationLab/"):
                errors.append(f"Portfolio manifest item {item_id} target_repository is outside the company organization")
            elif target_repository in target_repositories:
                errors.append(f"Portfolio manifest contains duplicate target_repository: {target_repository}")
            else:
                target_repositories.add(target_repository)

        for surface, orders in (
            ("founder_pin_order", founder_pin_orders),
            ("organization_pin_order", organization_pin_orders),
        ):
            pin_order = item.get(surface)
            if pin_order is not None:
                if type(pin_order) is not int or not 1 <= pin_order <= 6:
                    errors.append(
                        f"Portfolio manifest item {item_id} {surface} must be an integer from 1 through 6"
                    )
                elif pin_order in orders:
                    errors.append(f"Portfolio manifest contains duplicate {surface}: {pin_order}")
                else:
                    orders.add(pin_order)

        if item.get("publication_status") == "embedded-only":
            if item.get("kind") != "embedded-scenario" or target_repository is not None:
                errors.append(
                    f"Portfolio manifest item {item_id} embedded-only entries must be embedded scenarios without a target repository"
                )
            if item.get("founder_pin_order") is not None or item.get("organization_pin_order") is not None:
                errors.append(f"Portfolio manifest item {item_id} embedded-only entries cannot be pinned")
        elif item.get("publication_status") == "sanitized-candidate" and target_repository is None:
            errors.append(f"Portfolio manifest item {item_id} sanitized candidates require a target repository")

    if set(by_id) != set(EXPECTED_PORTFOLIO):
        missing = sorted(set(EXPECTED_PORTFOLIO) - set(by_id))
        extra = sorted(set(by_id) - set(EXPECTED_PORTFOLIO))
        if missing:
            errors.append(f"Portfolio manifest missing canonical items: {', '.join(missing)}")
        if extra:
            errors.append(f"Portfolio manifest contains unreviewed top-level items: {', '.join(extra)}")

    for item_id, expected in EXPECTED_PORTFOLIO.items():
        item = by_id.get(item_id)
        if not item:
            continue
        for key, value in expected.items():
            if item.get(key) != value:
                errors.append(f"Portfolio manifest item {item_id} {key} must be {value!r}")


def governance_change_control_findings(policy: dict) -> list[str]:
    """Validate the public desired-state boundary without exposing execution topology."""
    change_control = policy.get("change_control")
    if not isinstance(change_control, dict):
        return ["Public GitHub governance policy change_control must be an object"]

    expected = {
        "mode": "review_required",
        "least_privilege": True,
        "fail_closed": True,
        "rollback_evidence_required": True,
        "post_change_attestation_required": True,
        "sensitive_execution_contract": "private",
    }
    findings: list[str] = []
    for key, value in expected.items():
        if change_control.get(key) != value:
            findings.append(
                f"Public GitHub governance policy change_control.{key} must be {value!r}"
            )

    if set(change_control) != set(expected):
        findings.append(
            "Public GitHub governance policy change_control must contain only the public contract fields"
        )
    return findings


def validate_governance_policy(errors: list[str]) -> None:
    path = ROOT / ".github/governance/public-profile-policy.json"
    try:
        policy = json.loads(read_text(path))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"Public GitHub governance policy is not valid JSON: {exc}")
        return

    exact_values = {
        ("schema_version",): "1.4",
        ("policy_id",): "aureus-public-profile-governance",
        ("rollout_phase",): "pre-reviewer-bootstrap",
        ("repository", "name_with_owner"): "Aureus-Automation-Lab/Aureus-Automation-Lab",
        ("repository", "visibility"): "public",
        ("repository", "default_branch"): "main",
        ("ruleset", "name"): "aureus-main-governance",
        ("ruleset", "include_refs"): ["refs/heads/main"],
        ("ruleset", "exclude_refs"): [],
        ("ruleset", "maximum_bypass_actors"): 0,
        ("ruleset", "required_status_checks", "contexts"): [
            {"context": "Validate public profile", "integration_id": 15368}
        ],
        ("review_governance", "minimum_distinct_human_reviewers"): 1,
        ("review_governance", "reviewer_access_mode"): "repository_scoped_direct_collaborator",
        ("review_governance", "required_repository_permission"): "push",
        ("review_governance", "organization_membership_for_review_forbidden"): True,
        ("review_governance", "current_status"): "APPROVAL_REQUIRED",
        ("legacy_branch_protection", "minimum_controls"): {
            "required_approving_review_count": 1,
            "required_conversation_resolution": True,
            "allow_force_pushes": False,
            "allow_deletions": False,
        },
        ("founder_profile", "account"): "Aureus-Automation-Lab",
        ("change_control", "mode"): "review_required",
        ("change_control", "least_privilege"): True,
        ("change_control", "fail_closed"): True,
        ("change_control", "rollback_evidence_required"): True,
        ("change_control", "post_change_attestation_required"): True,
        ("change_control", "sensitive_execution_contract"): "private",
        ("license_boundary", "status"): "APPROVAL_REQUIRED_LICENSE_DECISION",
        ("license_boundary", "no_license_grant"): True,
        ("license_boundary", "decision_scope"): [
            "code",
            "documentation",
            "assets",
            "trademarks",
        ],
        ("promotion_readiness", "status"): "BLOCKED_PENDING_CONTACT_PATH",
        ("promotion_readiness", "approved_contact_url"): None,
        ("promotion_readiness", "contact_path_requires_owner_approval"): True,
        ("promotion_readiness", "contact_path_requires_verification"): True,
        ("founder_profile", "minimum_pinned_repositories_current_phase"): 0,
        ("founder_profile", "minimum_pinned_repositories_target_phase"): 1,
        ("founder_profile", "maximum_pinned_repositories"): 6,
        ("company_profile", "public_profile_repository"): "AureusAutomationLab/.github",
        ("company_profile", "default_branch"): "main",
        ("company_profile", "initial_commit_contract"): {
            "branch": "main",
            "parent_sha": None,
            "exact_tree": True,
            "required_paths": [
                "profile/README.md",
                ".github/CODEOWNERS",
                "SECURITY.md",
                ".github/workflows/public-profile-validation.yml",
            ],
        },
        ("company_profile", "required_non_empty_fields"): [
            "name",
            "description",
            "location",
            "blog",
        ],
        ("organization_governance", "default_repository_permission"): "none",
        ("organization_governance", "two_factor_requirement_enabled"): True,
        ("organization_governance", "members_can_delete_repositories"): False,
        ("organization_governance", "members_can_change_repo_visibility"): False,
        ("organization_governance", "web_commit_signoff_required"): True,
    }

    for keys, expected in exact_values.items():
        value = policy
        try:
            for key in keys:
                value = value[key]
        except (KeyError, TypeError):
            errors.append(f"Public GitHub governance policy missing {'.'.join(keys)}")
            continue
        if type(value) is not type(expected) or value != expected:
            errors.append(
                f"Public GitHub governance policy {'.'.join(keys)} must be {expected!r}"
            )

    expected_topics = {
        "aureus-os",
        "applied-ai",
        "ai-automation",
        "solution-architecture",
        "full-stack",
        "n8n",
        "public-proof",
        "evidence-first",
    }
    topics = ((policy.get("repository") or {}).get("required_topics"))
    if not isinstance(topics, list) or set(topics) != expected_topics:
        errors.append("Public GitHub governance policy required_topics must match the approved About target")

    errors.extend(governance_change_control_findings(policy))

    manifest_path = ROOT / "public-proof/portfolio-manifest.json"
    try:
        manifest = json.loads(read_text(manifest_path))
    except (OSError, UnicodeError, json.JSONDecodeError):
        manifest = {}
    identity = manifest.get("canonical_identity") or {}
    if identity.get("current_profile_repository") != (policy.get("repository") or {}).get(
        "name_with_owner"
    ):
        errors.append(
            "Public governance repository identity must match portfolio manifest canonical identity"
        )
    if identity.get("current_profile_account") != (policy.get("founder_profile") or {}).get(
        "account"
    ):
        errors.append(
            "Public governance founder identity must match portfolio manifest canonical identity"
        )
    governance_state = manifest.get("governance_state") or {}
    if governance_state.get("rollout_phase") != policy.get("rollout_phase"):
        errors.append(
            "Public governance rollout phase must match portfolio manifest governance state"
        )
    if governance_state.get("status") != "APPROVAL_REQUIRED":
        errors.append(
            "Public governance manifest status must remain APPROVAL_REQUIRED"
        )

    schema_result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate-local-json-schema.py"),
            "--schema",
            str(ROOT / ".github/governance/public-profile-policy.schema.json"),
            "--instance",
            str(path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=20,
    )
    if schema_result.returncode != 0:
        details = " | ".join(
            line.strip()
            for line in (schema_result.stdout + schema_result.stderr).splitlines()
            if line.strip()
        )
        errors.append(f"Public GitHub governance JSON Schema validation failed: {details[:1000]}")

    rule_types = set(((policy.get("ruleset") or {}).get("required_rule_types")) or [])
    expected_rule_types = {
        "deletion",
        "non_fast_forward",
        "pull_request",
        "required_linear_history",
        "required_signatures",
        "required_status_checks",
    }
    if rule_types != expected_rule_types:
        errors.append("Public GitHub governance policy ruleset rule types are incomplete or unreviewed")
    allowed_merge_methods = (((policy.get("ruleset") or {}).get("pull_request") or {}).get(
        "allowed_merge_methods"
    ))
    if allowed_merge_methods != ["squash"]:
        errors.append("Public GitHub governance ruleset must allow squash merges only")

    expected_security_controls = {
        "vulnerability_alerts",
        "dependabot_security_updates",
        "private_vulnerability_reporting",
        "secret_scanning",
        "secret_scanning_push_protection",
        "secret_scanning_validity_checks",
        "secret_scanning_non_provider_patterns",
    }
    security_controls = policy.get("security_and_analysis") or {}
    if set(security_controls) != expected_security_controls or set(security_controls.values()) != {
        "enabled"
    }:
        errors.append("Public GitHub governance security baseline is incomplete or unreviewed")


def workflow_security_findings(content: str) -> list[str]:
    """Inspect workflow semantics conservatively across valid YAML spacing variants."""
    active_content = "\n".join(
        line for line in content.splitlines() if not line.lstrip().startswith("#")
    )
    findings: list[str] = []
    forbidden_patterns = (
        (
            re.compile(r"(?m)^\s*pull_request_target\s*:|^\s*on\s*:\s*\[[^\]]*\bpull_request_target\b"),
            "Public validation must not use pull_request_target",
        ),
        (re.compile(r"(?i)\bwrite-all\b"), "Public validation must not use write-all permissions"),
        (re.compile(r"(?i)\bcontents\s*:\s*write\b"), "Public validation must not use contents: write"),
        (re.compile(r"(?i)\bid-token\s*:\s*write\b"), "Public validation does not need an OIDC write token"),
        (
            re.compile(r"\$\{\{\s*secrets\s*(?:\.|\[)"),
            "Public pull-request validation must not consume repository secrets",
        ),
    )
    for pattern, message in forbidden_patterns:
        if pattern.search(active_content):
            findings.append(message)

    for match in re.finditer(
        r"^\s*(?:-\s*)?uses\s*:\s*['\"]?([^'\"\s#]+)",
        active_content,
        re.MULTILINE,
    ):
        action = match.group(1)
        if action.startswith("./"):
            continue
        if "@" not in action:
            findings.append(f"Workflow Action has no immutable reference: {action}")
            continue
        _, ref = action.rsplit("@", 1)
        if not ACTION_REF_PATTERN.fullmatch(ref):
            findings.append(f"Workflow Action is not pinned to a full commit SHA: {action}")
    return findings


def validate_workflow_security(errors: list[str]) -> None:
    workflow_paths = sorted((ROOT / ".github/workflows").glob("*.yml")) + sorted(
        (ROOT / ".github/workflows").glob("*.yaml")
    )
    if not workflow_paths:
        errors.append("No GitHub Actions workflow is available for validation")
        return

    for path in workflow_paths:
        try:
            content = read_text(path)
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read workflow {path.relative_to(ROOT).as_posix()}: {exc}")
            continue

        rel = path.relative_to(ROOT).as_posix()
        for finding in workflow_security_findings(content):
            errors.append(f"{rel}: {finding}")

    primary = read_text(ROOT / ".github/workflows/public-profile-validation.yml")
    if "runs-on: ubuntu-24.04" not in primary:
        errors.append("Public validation workflow must use the explicit ubuntu-24.04 runner image")


def validate_markdown_links(errors: list[str]) -> None:
    repository_root = ROOT.resolve()
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "exports" in path.parts:
            continue
        try:
            content = read_text(path)
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read Markdown file {path.relative_to(ROOT).as_posix()}: {exc}")
            continue

        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            rel = path.relative_to(ROOT).as_posix()
            if not clean:
                continue
            if (
                clean.lower().startswith("file:")
                or clean.startswith(("\\\\", "//"))
                or WINDOWS_ABSOLUTE_PATTERN.match(clean)
                or Path(clean).is_absolute()
            ):
                errors.append(f"Unsafe absolute Markdown link in {rel}: {target}")
                continue

            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(repository_root)
            except ValueError:
                errors.append(f"Markdown link escapes repository in {rel}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"Broken Markdown link in {rel}: {target}")


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    for rel in FORBIDDEN_LEGACY_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"Legacy discoverable public path must not exist: {rel}")

    license_paths = [ROOT / name for name in ("LICENSE", "LICENSE.md", "LICENSE.txt")]
    if any(path.exists() for path in license_paths):
        errors.append(
            "A license file must not be added until the owner approves the code, documentation, asset, and trademark boundary"
        )

    readme_path = ROOT / "README.md"
    readme = read_text(readme_path) if readme_path.exists() else ""
    for required in README_REQUIRED:
        if required not in readme:
            errors.append(f"README.md missing required text/link: {required}")

    if "Founder & AI Systems Architect" in readme:
        errors.append("README.md still contains old main hero phrase: Founder & AI Systems Architect")

    readme_lines = readme.splitlines()
    if len(readme_lines) > 120:
        errors.append(f"README.md is too long for a focused public front door: {len(readme_lines)} lines (max 120)")

    headings = [line.strip() for line in readme.splitlines() if line.startswith("#")]
    duplicate_headings = sorted({heading for heading in headings if headings.count(heading) > 1})
    for heading in duplicate_headings:
        errors.append(f"README.md contains duplicate heading: {heading}")

    for rel, required_values in FILE_REQUIRED.items():
        path = ROOT / rel
        content = read_text(path) if path.exists() else ""
        for required in required_values:
            if required not in content:
                errors.append(f"{rel} missing required text: {required}")

    for rel in PRIMARY_NAMING_SURFACES:
        path = ROOT / rel
        content = read_text(path) if path.exists() else ""
        for canonical_name in CANONICAL_PUBLIC_NAMES:
            if canonical_name not in content:
                errors.append(f"{rel} missing canonical public name: {canonical_name}")

    validate_markdown_links(errors)
    validate_manifest(errors)
    validate_governance_policy(errors)
    validate_workflow_security(errors)

    try:
        text_files = list(iter_text_files())
    except (RuntimeError, UnicodeError) as exc:
        errors.append(f"Cannot enumerate the Git validation boundary: {exc}")
        text_files = []

    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            content = read_text(path)
        except (OSError, UnicodeError) as exc:
            errors.append(f"Tracked text file is not strict UTF-8 or readable ({rel}): {exc}")
            continue

        host_paths = host_specific_absolute_path_matches(content)
        if host_paths:
            errors.append(
                f"Host-specific absolute path found in public tracked text ({rel}): "
                f"{host_paths[0]!r}"
            )

        wrong_finecon = marker("Fine", "Con")
        if wrong_finecon in content:
            errors.append(f"Incorrect FinEcon spelling remains in {rel}")

        if SELF_RATING_PATTERN.search(content):
            errors.append(f"Subjective numeric self-rating found in {rel}")

        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in content.lower():
                errors.append(f"Forbidden hype phrase '{phrase}' found in {rel}")

        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(content):
                errors.append(f"Forbidden hype pattern '{pattern.pattern}' found in {rel}")

        if rel not in LEGACY_ALIAS_ALLOWLIST:
            for legacy_name in LEGACY_PRIMARY_NAMES:
                if legacy_name in content:
                    errors.append(
                        f"Legacy public name '{legacy_name}' found outside the explicit alias register in {rel}"
                    )

        for phrase in STALE_STATE_PHRASES:
            if phrase.lower() in content.lower():
                errors.append(f"Stale pre-publication instruction found in {rel}: {phrase}")

        for secret_marker in SECRET_MARKERS:
            if secret_marker.lower() in content.lower():
                errors.append(f"Obvious secret/local marker '{secret_marker}' found in {rel}")

        for secret_pattern in SECRET_VALUE_PATTERNS:
            if secret_pattern.search(content):
                errors.append(f"Possible embedded secret value found in {rel}")

        for mojibake_marker in MOJIBAKE_MARKERS:
            if mojibake_marker in content:
                errors.append(f"Likely encoding corruption found in {rel}: {ascii(mojibake_marker)}")

    if errors:
        print("PUBLIC_PORTFOLIO_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PUBLIC_PORTFOLIO_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
