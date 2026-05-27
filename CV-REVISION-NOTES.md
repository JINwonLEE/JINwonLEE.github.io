# CV Revision Notes for SK hynix Targeting

These notes summarize issues found by comparing `CV-Eng.pdf`, `CV-Kor.pdf`, `index.html`, `index-ko.html`, `portfolio-config.json`, and `portfolio-config-ko.json`.

## Must Fix in CV Source

- Align years of experience.
  - English CV: "8 years of experience"
  - Korean CV: "10년 차 개발자"
  - Portfolio site/config now uses "around 8 years" / "약 8년 차"
  - Recommended Korean CV text: `삼성전자에서 생성형 AI 서비스와 사내 LLM 플랫폼의 SRE/플랫폼 엔지니어링을 담당하고 있습니다. 약 8년 동안 Kubernetes 기반 서비스 운영, 클라우드 인프라 자동화, CI/CD, 관측 가능성, AI 평가/서빙 워크플로우를 다뤄왔습니다.`

- Fix Korean CV teaching assistant period.
  - Current extracted text: `2018.03 - 2018.01`
  - Likely inconsistent because the end date is earlier than the start date.
  - Verify against the original record before editing.

- Align the professional title.
  - Current PDFs: `SRE Engineer · Platform Engineer`
  - Portfolio site/config: `AI Platform · SRE Engineer` / `AI 플랫폼 · SRE 엔지니어`
  - Recommended direction: keep SRE visible, but move AI platform closer to the front for SK hynix AI/software/platform roles.

- Check address/privacy consistency.
  - English CV and Korean CV expose different address levels.
  - Website only shows Seoul, South Korea / 서울, 대한민국.
  - For public GitHub Pages PDFs, consider using city-level location only.

## Keep Because It Is Supported by the PDFs

- Company-wide AI chatbot platform serving 30,000 employees.
- Real-time packet mirroring up to 130,000 packets/sec.
- Distributed CNN training research reporting up to 2.3x speedup.
- Kubernetes, Azure, ArgoCD, Helm/Helmfile, GitHub Actions, Grafana, Prometheus, OpenTelemetry.
- Keycloak, OAuth, Langfuse for enterprise AI authentication and observability.

## Avoid Unless You Add Evidence

- Deployment-time reduction percentages.
- Unverified cost reduction, latency reduction, availability/SLA, or throughput numbers.
- Direct semiconductor/manufacturing claims unless a specific project or job description supports the connection.

## Suggested SK hynix-Oriented Summary

English:

```text
At Samsung Electronics, I work on SRE and platform engineering for generative AI services and internal LLM platforms. For about eight years, I have built and operated Kubernetes-based services, cloud infrastructure automation, CI/CD, observability, and AI evaluation/serving workflows. My strength is taking AI applications beyond "working code" and turning them into systems that real users can rely on.
```

Korean:

```text
삼성전자에서 생성형 AI 서비스와 사내 LLM 플랫폼의 SRE/플랫폼 엔지니어링을 담당하고 있습니다. 약 8년 동안 Kubernetes 기반 서비스 운영, 클라우드 인프라 자동화, CI/CD, 관측 가능성, AI 평가/서빙 워크플로우를 다뤄왔습니다. 제가 잘하는 일은 AI 애플리케이션을 "동작하는 코드"에서 실제 사용자가 안정적으로 쓸 수 있는 운영 구조로 옮기는 것입니다. 배포, 인증, 모니터링, 장애 대응, 리소스 제약을 함께 고려해 애플리케이션이 원활하게 동작할 수 있는 플랫폼을 만듭니다.
```

## SK hynix JD Target

Primary target:

- `선행 AI Software Solution - Platform Software`

Secondary target:

- `선행 AI Software Solution - System Software`

Supporting angle:

- MLOps, model serving operations, AI observability, and Kubernetes-based delivery.

Map the posting keywords to these evidence areas:

- AI/LLM/RAG: LLM evaluation, Document LLM platform, Langfuse observability, AI serving operations.
- Platform software: large-scale AI service operations, Kubernetes, Helm/Helmfile, ArgoCD, GitOps, cluster provisioning.
- MLOps / serving: LLM evaluation pipeline, MLflow metric tracking, AI serving efficiency work, Document LLM operations, Langfuse observability.
- System software: Linux, high-throughput packet mirroring, resource-constrained runtime behavior.
- Data/AI manufacturing fit: repeatable model evaluation, observability, data-sensitive enterprise AI operations, automation of reliable workflows.
- Reliability/operations: monitoring, alerting, multi-region readiness, security governance, DevSecOps checks.
