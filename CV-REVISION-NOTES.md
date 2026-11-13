# CV Revision Notes | November 2026

## Positioning

The shared portfolio position is:

`AI Platform & Reliability Engineer`

This preserves the strongest verified career signal, production platform engineering, while making direct Applied AI work easier to inspect.

Role-specific CV variants change emphasis without changing career facts:

- AI Platform & Reliability: agent platform delivery, governed runtime integration, observability, incident response, and production stabilization
- Platform/SRE: cloud runtime, delivery automation, observability, incident response, and security controls
- Applied AI: agent application delivery, LLM-assisted incident analysis, access control, model integration, rollout, and production operation

The public website lists only **English CV** (`CV-Eng.pdf`) and **Korean CV** (`CV-Kor.pdf`). Do not add role-specific variants to the navigation, hero, or download list. Existing variant files remain available at their historical URLs but are not advertised on the website.

## September changes

- Removed the decorative `Target Fit` block, skill chips, and arbitrary percentage bars.
- Moved to an ATS-readable two-page layout with a white background and restrained green, blue, and coral accents.
- Added the UNIST master's thesis: `Convergence Aware CNN Training`.
- Kept one-click Kubernetes provisioning as Bash-based work only.
- Removed Terraform, Ansible, standalone MLOps wording, and LLM Gateway design ownership.
- Replaced the public Enterprise AI Assistant reference with the user's LLM-assisted cluster monitoring project.
- Added stable public files for AI Platform & Reliability, Platform/SRE, Applied AI, and Korean CVs.
- Refreshed old tracked PDF URLs with the latest content so historical links no longer serve stale versions.

## Verified evidence

- About eight years of software, platform, and reliability engineering
- AWS EKS AX Agent Platform design and delivery
- Automatic domains and authorized-only access for self-service AX application deployment
- Authentication, authorization, security, and governance responsibility
- Client compatibility with an existing enterprise LLM Gateway API
- Microsoft collaboration for UK rollout readiness, initial operation, incident response, and stabilization of a B2C generative AI service
- Production delivery and reliability for a 30,000-employee AI chatbot
- Linux packet processing measured at up to 130,000 packets per second
- Distributed CNN research reporting up to 2.3x training speedup
- AI assistant inference, preprocessing, system integration, and asynchronous flows at TmaxOS
- Personal LLM-assisted monitoring system for internal clusters: error detection, LLM analysis, and email reports containing problems, analysis, and suggested remediation steps

## Personal project boundary | September 15

The user described a personal monitoring project for internal cluster operations. It detects errors, uses an LLM to analyze them, and emails the problem, analysis, and suggested solutions to the operator. Use this project in the website, both portfolio languages, and all current CV variants instead of Enterprise AI Assistant. Keep professional AX Agent Platform and production reliability work as the primary evidence.

Do not infer the model/provider, programming language, monitoring stack, scale, measured impact, or automatic remediation. Do not attach the old assistant's demo/source links to this project. The old reference code may remain in the repository but is no longer a featured CV or portfolio claim.

## Evaluation emphasis correction | September 15

The user clarified that their contribution to evaluation work was limited. Evaluation is not a primary strength or a headline project. Do not claim ownership of an evaluation pipeline, benchmark design, evaluation strategy, or measurable model-quality improvements.

- Remove evaluation from CV summaries, selected evidence, and core skills.
- Remove the standalone LLM evaluation case from featured website projects and detailed portfolio PDF cases.
- Retain only a short supporting statement in both portfolio languages: "Contributed to LLM evaluation work for machine translation" / "기계 번역을 위한 LLM 평가 작업에 참여했습니다."
- Keep AX Agent Platform, governed delivery, observability, release automation, and production reliability as the primary evidence.

## November additions | November 13

- Added **SK hynix AI Hackathon 2026 finalist** (본선 진출, Nov. 2026) under a new `Awards & Activities` / `수상 및 활동` section in every CV variant, both portfolio PDFs, and the website research list. Source: the user, and the official page `https://skhynix-hackathon.com/ai-2026` (Korean name `SK하이닉스 AI 해커톤 2026`; individual entry; two online qualifying rounds; offline finals on 2026-11-11 at COEX). The page gives no English name, so `SK hynix AI Hackathon 2026` is a translation. The user did not win a prize; do not call it an award win.
- Added **OfferNow (오퍼나우)** as a personal project in every CV variant, both portfolio PDFs, and the website. Source: the user's `career-copilot` repository as of 2026-11-09. Verified facts: CV (PDF/DOCX) to evidence-linked profile; official postings from 50+ Korean companies (51 connected of 78 registered on 2026-11-08) collected with robots.txt checks and no LLM; rule-based matching; provider-neutral LLM calls with per-user daily limits and cost logging; Expo/React Native, FastAPI, PostgreSQL with RLS, anonymous 24-hour sessions; Docker Compose, nginx, Let's Encrypt; deployed 2026-11-04 at heyoffernow.ai behind an operator-only gate ahead of a beta.
- Do not claim users, adoption, or recommendation-quality metrics for OfferNow until they are measured.
- Footer and dated filenames moved to November 2026. Older dated PDF URLs are refreshed with the latest content by the builders.

## Layout changes | November 13

- CV page 1 now holds all four experience entries; page 2 starts at `Selected Engineering Work`. The builder measures each page's free space and spreads it between sections, entries, and lines, so page 1 no longer ends with a large empty block.
- On the website the hackathon moved out of `Education & Research` into its own `Awards & Activities` section above the contact block.

## Website redesign | November 13

- The user asked for a less template-like site with visible interaction. Both pages now use a dark two-column layout: a fixed left rail (name, title, section navigation, CV links) and a scrolling right column (about, experience, projects, research, awards, contact).
- Interaction lives in `assets/js/script.js`: a spotlight that follows the cursor, drifting background points that link up near the cursor, rows that highlight while their siblings dim, project cards whose border glows at the cursor, a character-by-character name reveal, and sections that fade in on scroll. All of it is skipped under `prefers-reduced-motion`, and the cursor effects only run on devices with a mouse.
- Copy was carried over from the previous pages. The About paragraphs restate existing verified claims in first person; no new claims were added.
- Only the AX Agent Platform and OfferNow keep diagrams. Replace the OfferNow diagram with a real product screenshot when one is available.

## Claims to avoid

- Terraform or Ansible experience without a new source
- Ownership of LLM Gateway architecture or design
- Unmeasured availability, latency, cost, MTTR, adoption, or deployment-time metrics
- General claims of customer leadership that are not tied to a verified engagement
- Production-use claims for the public reference project
