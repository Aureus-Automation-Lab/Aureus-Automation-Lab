# Profile ImageGen Production Guide

This guide defines how public profile images should be generated for Róbert Kolesár / robertkolesar and Aureus Automation Lab.

The goal is not to generate beautiful random images. The goal is to create public-safe visuals that explain the portfolio faster than text can.

## Official Guidance Applied

This workflow uses Codex built-in `image_gen` as the primary production path for this repository. OpenAI Image Generation / Images 2.0 guidance is used for prompt structure, review discipline, and future direct API runs if the owner explicitly configures that path.

- generate through Codex built-in `image_gen` for normal profile assets,
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
- OpenAI Images 2.0 announcement: https://openai.com/index/introducing-chatgpt-images-2-0/

## Codex ImageGen Route Decision

| Need | Use | Why |
| --- | --- | --- |
| Normal profile visual | Codex built-in `image_gen` | Fastest available path in Codex; no API key setup required |
| Iterative creative direction | Codex built-in `image_gen` with one targeted follow-up at a time | Keeps the image direction controlled and avoids random drift |
| Project-bound asset | Generate in Codex, inspect, then copy accepted output into `assets/` | The repository must not reference temporary generated-image paths |
| Future direct API run | Image API / Responses API only if explicitly configured | Useful when the owner wants exact API control over size, quality, format, or streaming |
| Transparent background | Avoid for this profile unless needed | GitHub profile images should be opaque 16:9 visuals; transparency needs a separate removal workflow |

For this GitHub profile, the default production pattern is:

1. Generate a strong base concept with Codex built-in `image_gen`.
2. Review it against the slot-specific acceptance gate.
3. If only one thing is wrong, run a targeted iteration instead of rewriting the whole prompt.
4. Inspect the generated still or GIF frame.
5. Copy only accepted assets into `assets/`.
6. Document the prompt, visual job, and acceptance decision.

## Recommended Settings And Constraints

Codex built-in `image_gen` does not require this public repo to store or manage an OpenAI API key environment variable or write a custom API runner. The controllable variables are the prompt, iteration discipline, asset selection, and QA gate.

If a future direct API run is explicitly configured, use these settings as the default:

| Stage | Recommended setting | Notes |
| --- | --- | --- |
| First draft | low or medium quality | Use only to test composition and meaning |
| Final public asset | high quality | Use for hero and major profile visuals |
| README landscape | `1536x1024` or `2048x1152` | Landscape assets fit GitHub profile sections best |
| Output format | GIF or static image | Use GIF only when motion helps explain a process |
| In-image text | Keep short and deliberate | Text must remain readable at GitHub width |

## OpenAI Images 2.0 Lessons Applied

Images 2.0 is useful for more than decorative scenes. For this profile, use it for:

| Capability | Profile use |
| --- | --- |
| Complex visual systems | Aureus OS architecture maps, governance flows, proof loops |
| Editorial layouts | GitHub README hero and visual review sections |
| Diagram-like imagery | Public/private boundary and validation flows |
| Multi-turn refinement | Fix one defect at a time: remove text, simplify composition, adjust hierarchy |
| Visual consistency | Reuse the same palette, icons, grid, lighting, and slot vocabulary |

Do not use it to create fake evidence. Generated media is concept visualization only.

## Production Rule

Every image must have a slot and a job.

| Slot | Review job | Good image outcome |
| --- | --- | --- |
| README hero | Explain the full public profile in one scene | Manual process becomes Aureus OS architecture, validation, evidence, and handoff |
| Workflow governance | Explain why workflow automation is controlled | Source, review gates, approval, credential separation, evidence, handoff |
| Public/private boundary | Explain why raw private work is not public | Public proof artifacts are separated from sealed private implementation |
| Supervisor validation | Explain model supervision without fake certification | Worker output passes contract, review, repair, scorecard, and evidence |
| FinEcon / Invoice | Explain document-heavy workflow boundaries | Intake, extraction, review, POHODA boundary, evidence |
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
| `assets/aureus-profile-hero.gif` | Accepted | It now reads as a five-zone architecture map with manual inputs, process mapping, Aureus OS core, validation, evidence/handoff, and private boundary |
| `assets/aureus-offer-menu.gif` | Accepted | It shows the six concrete commercial starting points without turning the README into a sales document |
| `assets/aureus-sales-workflow.gif` | Accepted | It shows lead handling, qualification, manual approval, reply classification, next step, report, and evidence |
| `assets/aureus-finecon-flow.gif` | Accepted | It shows document/invoice intake, extraction, validation, exceptions, owner review, and finance handoff |
| `assets/aureus-os-model.gif` | Accepted | It shows task, limits, AI draft, validation, approval, and evidence as one operating model |
| `assets/aureus-public-boundary.gif` | Accepted | It shows public proof separated from private implementation |
| `assets/aureus-capability-system.gif` | Accepted | It shows each capability as its own lane instead of reusing an offer visual |
| `assets/aureus-collaboration-flow.gif` | Accepted | It shows the delivery relationship from context to handoff |
| `assets/aureus-proof-pack.gif` | Accepted | It shows what can be made public and what remains private |
| `assets/aureus-readiness-check.gif` | Accepted | It shows the final public release gates |
| `assets/aureus-solution-architecture.gif` | Accepted | It shows the technical flow from signal to evidence |

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
