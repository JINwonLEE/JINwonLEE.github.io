# Portfolio Update Guide

This repository publishes the bilingual portfolio at `jinwonlee.github.io`, generates role-specific CVs, and contains the public Enterprise AI Assistant reference implementation.

## Source of truth

- `index.html`: public English portfolio
- `index-ko.html`: public Korean portfolio
- `portfolio-config.json`: English project data used by the portfolio PDF builder
- `portfolio-config-ko.json`: Korean project data used by the portfolio PDF builder
- `tools/build_resume_pdfs.py`: content and layout for every CV variant
- `tools/build_portfolio_pdf.py`: content and layout for the downloadable portfolio PDFs

The website is intentionally static and does not fetch the JSON configs. When career facts change, update both HTML files, both config files, and the CV builder from the same verified evidence.

## Public positioning

Keep the shared website position broad enough for both role families:

`Production AI & Platform Engineer`

Use the role-specific CVs for application emphasis:

- `CV-Eng.pdf`: general/master CV
- `CV-Platform-SRE.pdf`: platform and reliability emphasis
- `CV-Applied-AI.pdf`: Applied AI and AI application emphasis
- `CV-Kor.pdf`: Korean master CV

Do not add a `Target Role` or `Target Fit` block to the CV. The professional title can change by variant, while the underlying career facts stay identical.

## Generate documents

```bash
python3 tools/build_resume_pdfs.py
python3 tools/build_portfolio_pdf.py
```

The builders write dated copies under `output/pdf/` and refresh the stable root filenames linked by the website.

Before publishing, render every PDF page and inspect it. At minimum, verify page count, text extraction, line wrapping, Korean glyphs, and working URLs.

## Evidence rules

Use only verified claims. The currently supported evidence includes:

- About eight years of software, platform, and reliability engineering experience
- AWS EKS-based AX Agent Platform delivery
- Self-service AX application deployment with automatic domains and authorized-only access
- Authentication, authorization, security, and governance responsibility
- Client integration with an existing enterprise LLM Gateway API
- UK rollout readiness, initial operation, incident response, and stabilization for a B2C generative AI service
- Production reliability for an enterprise AI chatbot used by 30,000 employees
- A Linux application measured at up to 130,000 packets per second
- Distributed CNN training research reporting up to 2.3x speedup
- Python/MLflow evaluation for LLM-based machine translation
- Bash-based one-click Kubernetes cluster provisioning

Do not introduce these claims without new source evidence:

- Terraform or Ansible experience
- Ownership of LLM Gateway design
- MLOps as a standalone responsibility label
- Availability, latency, MTTR, cost, adoption, or deployment-time metrics that have not been measured
- Production use of the public Enterprise AI Assistant reference implementation

## Add a project

1. Add a public description to both config files.
2. Add the matching case study to both HTML files when it should appear on the website.
3. Use a real project screenshot or an existing system diagram under `assets/images/`.
4. Separate `problem`, `role`, `engineering`, and `outcome` so ownership is clear.
5. Mark synthetic or personal work as a `public reference implementation`.

## Enterprise AI Assistant

The public reference implementation lives at:

```text
projects/enterprise-ai-assistant/
```

Run its tests:

```bash
cd projects/enterprise-ai-assistant
/usr/bin/python3 -m unittest discover -s tests -v
```

Run the API-backed UI:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8088
```

The GitHub Pages demo uses the deterministic browser implementation. The FastAPI version exposes the same access-control and evaluation workflow through API endpoints.

## Test the website

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Open:

- English: `http://127.0.0.1:4173/`
- Korean: `http://127.0.0.1:4173/index-ko.html`
- Public assistant: `http://127.0.0.1:4173/projects/enterprise-ai-assistant/web/`

Check desktop and mobile widths. Confirm there is no horizontal overflow, every image loads, the mobile navigation opens, and every CV/demo link returns successfully.

## Publish

Review the exact staged files before committing. Generated virtual environments, render outputs, caches, and `tmp/` are ignored.

```bash
git status --short
git diff --check
git add <reviewed files>
git commit -m "Refresh portfolio and career materials"
git push origin main
```

After GitHub Pages deploys, verify the live home page, Korean page, assistant demo, and each stable CV URL instead of relying on the local files alone.
