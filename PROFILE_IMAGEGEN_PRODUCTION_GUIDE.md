# Profile ImageGen Production Guide

This guide defines how public profile images should be generated for Robert Kolesár / KimiAoki and Aureus Automation Lab.

The goal is not to generate beautiful random images. The goal is to create public-safe visuals that explain the portfolio faster than text can.

## Official Guidance Applied

This workflow follows the OpenAI image generation guidance used through the OpenAI Developers docs:

- use `gpt-image-2` for generation when using the Image API route,
- include the intended use of the image in the prompt,
- structure prompts in a stable order: scene/background, subject, key details, constraints,
- use short labeled sections for complex prompts,
- specify composition, viewpoint, lighting, materials, and layout when they matter,
- state exclusions and invariants explicitly,
- avoid relying on precise in-image text unless necessary,
- iterate with targeted changes instead of overloading a single prompt.

Reference pages:

- OpenAI Image Generation Guide: https://developers.openai.com/api/docs/guides/image-generation
- OpenAI GPT Image Prompting Guide: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- OpenAI Images 2.0 announcement: https://openai.com/sk-SK/index/introducing-chatgpt-images-2-0/

## API Route Decision

| Need | Use | Why |
| --- | --- | --- |
| One new final asset from one prompt | Image API with `gpt-image-2` | Direct generation path for a single image |
| Iterative creative direction | Responses API with image generation tool | Supports multi-turn refinement through conversation state |
| High-fidelity edits from a previous image | Responses API or Image API edits | Use when the base image is good and only one part needs to change |
| Reference-image composition | Image API edits or Responses API with image inputs | Use when style, structure, or source objects must be preserved |
| Transparent background | Not native in `gpt-image-2` | Use opaque output or a controlled chroma-key/removal flow instead |

For this GitHub profile, the default production pattern is:

1. Generate a strong base concept with the Image API style prompt structure.
2. Review it against the slot-specific acceptance gate.
3. If only one thing is wrong, run a targeted iteration instead of rewriting the whole prompt.
4. Save only accepted assets into `assets/image2/`.

## Recommended Settings For GitHub Profile Assets

| Stage | Recommended setting | Notes |
| --- | --- | --- |
| First draft | `quality: low` or built-in fast draft | Use only to test composition and meaning |
| Review candidate | `quality: medium` | Good balance for visual QA |
| Final public asset | `quality: high` when using direct API | Use for hero and major profile visuals |
| README landscape | `1536x1024` or `2048x1152` | Landscape assets fit GitHub profile sections best |
| Output format | PNG | Best default for crisp GitHub concept visuals |
| In-image text | Avoid | Use Markdown/SVG text instead; generated text can drift |

## OpenAI Images 2.0 Lessons Applied

Images 2.0 is useful for more than decorative scenes. For this profile, use it for:

| Capability | Profile use |
| --- | --- |
| Complex visual systems | AOP architecture maps, governance flows, proof loops |
| Editorial layouts | GitHub README hero and visual review sections |
| Diagram-like imagery | Public/private boundary and validation flows |
| Multi-turn refinement | Fix one defect at a time: remove text, simplify composition, adjust hierarchy |
| Visual consistency | Reuse the same palette, icons, grid, lighting, and slot vocabulary |

Do not use it to create fake evidence. Generated media is concept visualization only.

## Production Rule

Every image must have a slot and a job.

| Slot | Review job | Good image outcome |
| --- | --- | --- |
| README hero | Explain the full public profile in one scene | Manual process becomes AOP architecture, validation, evidence, and handoff |
| Workflow governance | Explain why workflow automation is controlled | Source, review gates, approval, credential separation, evidence, handoff |
| Public/private boundary | Explain why raw private work is not public | Public proof artifacts are separated from sealed private implementation |
| Supervisor validation | Explain model supervision without fake certification | Worker output passes contract, review, repair, scorecard, and evidence |
| FineCon / Invoice | Explain document-heavy workflow boundaries | Intake, extraction, review, POHODA boundary, evidence |
| Web Studio | Explain visual production discipline | Brief, design system, build, browser QA, proof pack |

If an image cannot name its slot and review job, it should not be generated.

## Prompt Structure

Use this shape for every production prompt:

```text
Use case: productivity-visual / infographic-diagram
Asset type: <where this image will appear>

PRIMARY GOAL
<What the reviewer should understand in five seconds.>

VISUAL FORMAT
<The kind of image: technical poster, editorial architecture map, product-system diagram, visual proof board.>

COMPOSITION
<Layout, reading direction, macro zones, hierarchy, negative space, GitHub README size.>

SYSTEM ANATOMY
<The exact visible objects and what each one means.>

STYLE
<Color, material language, lighting, polish level, typography behavior if any.>

LAYOUT RULES
<What to include, what not to include, how to prevent clutter.>

SAFETY CONSTRAINTS
<No secrets, no fake claims, no private implementation, no real screenshots.>

SUCCESS CRITERIA
<How we decide if the image is accepted or rejected.>
```

## Visual Language

Use this shared visual system:

| Element | Meaning |
| --- | --- |
| Dark graphite grid | serious technical review surface |
| Cyan rails | workflow and system routing |
| Muted Aureus gold | owner approval, action gates, handoff |
| Green validation states | tests, evidence, reviewed output |
| Ivory paper fragments | business documents and manual process |
| Frosted gates | review, validation, egress, human approval |
| Sealed lower lane | private credentials, endpoints, workflow exports, production settings |

## What To Avoid

- Random dark AI command-center images.
- Generic glowing dashboards.
- Fake metrics, charts, customer proof, revenue, badges, certificates, or dashboards.
- Humanoid robots, office stock scenes, handshake imagery, trophies, coins, or provider logos.
- Tiny illegible UI labels.
- Real-looking code snippets, URLs, endpoints, webhook paths, credentials, workflow IDs, POHODA internals, private payloads, or private screenshots.
- Images that look impressive but do not explain the exact Markdown section.

## Current Asset Decisions

| Asset | Decision | Why |
| --- | --- | --- |
| `assets/image2/profile-public-architecture-hero.png` | Accepted | It now reads as a five-zone architecture map with manual inputs, process mapping, AOP core, validation, evidence/handoff, and private boundary |
| `assets/image2/n8n-workflow-governance.png` | Accepted | It reads as workflow source moving through review gates, approval, evidence/handoff, and separated credentials |
| `assets/image2/public-private-boundary.png` | Accepted | It shows public-safe artifacts, a controlled review window, and sealed private implementation without text |
| `assets/image2/supervisor-validation-capability.png` | Accepted | It shows contract check, supervisor review, repair loop, owner approval, and evidence/handoff without provider or certification claims |

## Acceptance Gate

Accept an image only when all are true:

- The image explains its section without needing fake text.
- It is visually readable at GitHub README width.
- The composition is intentional and not random.
- The public/private boundary is safe.
- It does not imply production proof, certification, revenue, customer outcome, accounting correctness, or trading performance.
- It has no private-looking details.
- It improves comprehension compared with Markdown alone.

If any point fails, keep the prompt but reject the image.
