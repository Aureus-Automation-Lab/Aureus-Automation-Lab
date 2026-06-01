# Aureus Use Case Showcase V5 PDF Handoff

This repo includes public-safe local PDF generators for the English and Slovak showcase.

Preferred client-language generator:

```powershell
python scripts\generate-aureus-use-case-pdfs-v6-pro.py
```

This is the recommended version for client conversations. It uses the original v4 visual direction only as cropped conceptual panels, then rebuilds all text, cards, tables, scorecards, and CTAs on a clean grid with simpler buyer-facing language.

Legacy generator when the original v4 visual PDF is available:

```powershell
python scripts\generate-aureus-use-case-pdfs-v4-visuals.py
```

This keeps the original v4 visual direction and redraws the client-facing text, cards, labels, and Slovak/English copy as editable PDF text.

Fallback diagram generator:

```powershell
python scripts\generate-aureus-use-case-pdfs.py
```

The scripts create polished 16:9 PDF exports under `exports/` and copy the latest files to the desktop/OneDrive desktop folder when available. This handoff defines the source copy, layout rules, and safety checks that the PDF generator must preserve.

## Source Copy

Use:

- [AUREUS_USE_CASE_SHOWCASE_COPY_V5.md](AUREUS_USE_CASE_SHOWCASE_COPY_V5.md)
- [AUREUS_USE_CASE_SHOWCASE_COPY_V5_SK.md](AUREUS_USE_CASE_SHOWCASE_COPY_V5_SK.md)
- [AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V5.md](AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V5.md)
- [AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V6.md](AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V6.md)
- [AUREUS_USE_CASE_SHOWCASE_TOP_TIER_REFERENCE_NOTES.md](AUREUS_USE_CASE_SHOWCASE_TOP_TIER_REFERENCE_NOTES.md)

## Required Pages

1. Aureus Use Case Portfolio
2. How We Choose The Right AI Use Case
3. Automation Audit
4. n8n Workflow Review + Build
5. FinEcon Pocket / Bridge
6. Approval-Safe Sales Machine
7. Aureus OS / AOP
8. Public Proof Website + Automation
9. Client Use-Case Scorecard
10. 30-Day Client Pilot Path
11. How To Use This Showcase
12. Best First Step

## Layout Requirements

- Use 16:9 landscape for client presentation.
- Use enough text to explain each page, but avoid dense paragraphs.
- Add a visible "Client receives" block on every use-case page.
- Add proof status chips on every use-case page.
- Keep tables readable on screen and PDF.
- Avoid full blank pages.
- Avoid random bullet symbols or encoding artifacts.
- Use Slovak diacritics correctly in the SK version.

## Visual Requirements

- Visuals may be conceptual.
- Conceptual visuals must not be presented as real screenshots.
- Avoid tiny text inside generated images.
- Do not place text over high-detail image areas without a dark/light overlay.
- Every image must support the exact use case on that page.

## Safety Notes

Do not include:

- private implementation screenshots,
- raw workflow exports,
- credentials,
- private routes,
- private IDs,
- local paths,
- runtime logs,
- real invoices,
- real leads,
- customer-like data,
- unsupported claims.

## Export Settings

- PDF title: `Aureus Use Case Showcase V5`
- Author/brand: `Aureus Automation Lab`
- Language variants:
- English: `Aureus_Use_Case_Showcase_V5_EN.pdf`
- Slovak: `Aureus_Use_Case_Showcase_V5_SK.pdf`
- Preferred English: `Aureus_Use_Case_Showcase_Client_Language_V7_EN.pdf`
- Preferred Slovak: `Aureus_Use_Case_Showcase_Client_Language_V7_SK.pdf`
- Use high-quality image export.
- Keep final file size reasonable for email and LinkedIn follow-up.
