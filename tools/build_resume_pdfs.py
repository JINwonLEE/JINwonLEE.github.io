from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from typing import Iterable, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT, "output", "pdf")
FONT_PATHS = (
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
)
FONT_PATH = next(path for path in FONT_PATHS if os.path.exists(path))
FONT = "ResumeSans"
pdfmetrics.registerFont(TTFont(FONT, FONT_PATH))


INK = colors.HexColor("#17211D")
MUTED = colors.HexColor("#5D6C64")
ACCENT = colors.HexColor("#176B4D")
CORAL = colors.HexColor("#D95F45")
BLUE = colors.HexColor("#2F5FA7")
LINE = colors.HexColor("#D9E1DC")
SOFT = colors.HexColor("#F3F7F5")


@dataclass(frozen=True)
class Experience:
    company: str
    role: str
    period: str
    location: str
    bullets: Sequence[str]


@dataclass(frozen=True)
class Project:
    title: str
    description: str
    link: str = ""


@dataclass(frozen=True)
class ResumeVariant:
    filename: str
    root_filename: str
    language: str
    professional_title: str
    summary: Sequence[str]
    evidence: Sequence[str]
    skills: Sequence[tuple[str, str]]
    experiences: Sequence[Experience]
    projects: Sequence[Project]


class ResumeDocument:
    def __init__(self, path: str, language: str, title: str):
        self.path = path
        self.language = language
        self.title = title
        self.canvas = canvas.Canvas(path, pagesize=A4)
        self.width, self.height = A4
        self.left = 16 * mm
        self.right = 16 * mm
        self.top = 14 * mm
        self.bottom = 13 * mm
        self.y = self.height - self.top
        self.page = 1

    @property
    def usable_width(self) -> float:
        return self.width - self.left - self.right

    def text_width(self, text: str, size: float) -> float:
        return pdfmetrics.stringWidth(text, FONT, size)

    def wrap(self, text: str, size: float, width: float) -> list[str]:
        words = text.split(" ")
        lines: list[str] = []
        current = ""
        for word in words:
            trial = word if not current else f"{current} {word}"
            if self.text_width(trial, size) <= width:
                current = trial
                continue
            if current:
                lines.append(current)
            current = word
        if current:
            lines.append(current)
        return lines

    def ensure(self, height: float) -> None:
        if self.y - height < self.bottom:
            self.new_page()

    def draw_rule(self, y: float, color=LINE, width: float = 0.6) -> None:
        self.canvas.setStrokeColor(color)
        self.canvas.setLineWidth(width)
        self.canvas.line(self.left, y, self.width - self.right, y)

    def footer(self) -> None:
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont(FONT, 6.8)
        updated = "Updated Sep. 2026" if self.language == "en" else "2026.09 업데이트"
        self.canvas.drawString(self.left, 7.2 * mm, updated)
        self.canvas.drawRightString(
            self.width - self.right,
            7.2 * mm,
            f"Jinwon Lee  |  {self.page}" if self.language == "en" else f"이진원  |  {self.page}",
        )

    def new_page(self) -> None:
        self.footer()
        self.canvas.showPage()
        self.page += 1
        self.y = self.height - self.top
        self.canvas.setFillColor(INK)
        self.canvas.setFont(FONT, 9.2)
        name = "JINWON LEE" if self.language == "en" else "이진원"
        self.canvas.drawString(self.left, self.y, name)
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont(FONT, 7.4)
        self.canvas.drawRightString(self.width - self.right, self.y, self.title)
        self.y -= 9
        self.draw_rule(self.y, ACCENT, 1.1)
        self.y -= 13

    def header(self) -> None:
        name = "Jinwon Lee" if self.language == "en" else "이진원"
        contact = (
            "Seoul, South Korea  |  +82 10-2422-1429  |  dlwlsdnjsehs1993@gmail.com"
            if self.language == "en"
            else "서울, 대한민국  |  +82 10-2422-1429  |  dlwlsdnjsehs1993@gmail.com"
        )
        links = "github.com/JINwonLEE  |  linkedin.com/in/jwl1993"

        self.canvas.setFillColor(ACCENT)
        self.canvas.rect(self.left, self.y - 38, 3.2, 40, fill=1, stroke=0)
        self.canvas.setFillColor(INK)
        self.canvas.setFont(FONT, 25)
        self.canvas.drawString(self.left + 10, self.y - 6, name)
        self.canvas.setFillColor(ACCENT)
        self.canvas.setFont(FONT, 10.4)
        self.canvas.drawString(self.left + 11, self.y - 23, self.title)
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont(FONT, 7.4)
        self.canvas.drawRightString(self.width - self.right, self.y - 7, contact)
        self.canvas.drawRightString(self.width - self.right, self.y - 20, links)
        self.y -= 49
        self.draw_rule(self.y, ACCENT, 1.2)
        self.y -= 9

    def section(self, title: str) -> None:
        self.ensure(22)
        self.y -= 4
        self.canvas.setFillColor(ACCENT)
        self.canvas.setFont(FONT, 8.6)
        label = title.upper() if self.language == "en" else title
        self.canvas.drawString(self.left, self.y, label)
        start = self.left + self.text_width(label, 8.6) + 8
        self.canvas.setStrokeColor(LINE)
        self.canvas.setLineWidth(0.6)
        self.canvas.line(start, self.y + 2, self.width - self.right, self.y + 2)
        self.y -= 12

    def paragraph(self, text: str, size: float = 8.45, leading: float = 12.0) -> None:
        lines = self.wrap(text, size, self.usable_width)
        self.ensure(len(lines) * leading + 2)
        self.canvas.setFillColor(INK)
        self.canvas.setFont(FONT, size)
        for line in lines:
            self.canvas.drawString(self.left, self.y, line)
            self.y -= leading
        self.y -= 2

    def bullets(
        self,
        items: Iterable[str],
        size: float = 8.0,
        leading: float = 11.0,
        x: float | None = None,
        width: float | None = None,
        gap: float = 1.5,
    ) -> None:
        x = self.left if x is None else x
        width = self.usable_width if width is None else width
        indent = 10
        for item in items:
            lines = self.wrap(item, size, width - indent)
            self.ensure(len(lines) * leading + gap)
            self.canvas.setFillColor(CORAL)
            self.canvas.setFont(FONT, size)
            self.canvas.drawString(x, self.y, "-")
            self.canvas.setFillColor(INK)
            for line in lines:
                self.canvas.drawString(x + indent, self.y, line)
                self.y -= leading
            self.y -= gap

    def evidence(self, items: Sequence[str]) -> None:
        gutter = 9
        column_width = (self.usable_width - gutter * 2) / 3
        wrapped = [self.wrap(item, 7.3, column_width - 12) for item in items]
        box_height = max(len(lines) for lines in wrapped) * 9.5 + 18
        self.ensure(box_height + 4)
        top = self.y
        for index, lines in enumerate(wrapped):
            x = self.left + index * (column_width + gutter)
            self.canvas.setFillColor(SOFT)
            self.canvas.rect(x, top - box_height, column_width, box_height, fill=1, stroke=0)
            self.canvas.setFillColor((ACCENT, BLUE, CORAL)[index])
            self.canvas.rect(x, top - 3, column_width, 3, fill=1, stroke=0)
            self.canvas.setFont(FONT, 7.3)
            self.canvas.setFillColor(INK)
            yy = top - 15
            for line in lines:
                self.canvas.drawString(x + 6, yy, line)
                yy -= 9.5
        self.y -= box_height + 5

    def skill_rows(self, rows: Sequence[tuple[str, str]]) -> None:
        label_width = 37 * mm
        for label, detail in rows:
            lines = self.wrap(detail, 7.75, self.usable_width - label_width - 8)
            height = max(12.5, len(lines) * 10.7)
            self.ensure(height + 2)
            self.canvas.setFillColor(ACCENT)
            self.canvas.setFont(FONT, 7.75)
            self.canvas.drawString(self.left, self.y, label)
            self.canvas.setFillColor(INK)
            yy = self.y
            for line in lines:
                self.canvas.drawString(self.left + label_width, yy, line)
                yy -= 10.7
            self.y -= height

    def experience(self, experience: Experience) -> None:
        bullet_lines = sum(
            len(self.wrap(bullet, 8.0, self.usable_width - 20))
            for bullet in experience.bullets
        )
        self.ensure(28 + bullet_lines * 11.0)
        self.canvas.setFillColor(INK)
        self.canvas.setFont(FONT, 9.1)
        self.canvas.drawString(self.left, self.y, experience.company)
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont(FONT, 7.2)
        self.canvas.drawRightString(self.width - self.right, self.y, experience.location)
        self.y -= 10.5
        self.canvas.setFillColor(ACCENT)
        self.canvas.setFont(FONT, 7.8)
        self.canvas.drawString(self.left, self.y, experience.role)
        self.canvas.setFillColor(MUTED)
        self.canvas.drawRightString(self.width - self.right, self.y, experience.period)
        self.y -= 11
        self.bullets(experience.bullets, x=self.left + 3, width=self.usable_width - 3)
        self.y -= 3

    def project(self, project: Project) -> None:
        title_size = 8.2
        description_lines = self.wrap(project.description, 7.8, self.usable_width - 8)
        self.ensure(13 + len(description_lines) * 10.8)
        self.canvas.setFillColor(INK)
        self.canvas.setFont(FONT, title_size)
        self.canvas.drawString(self.left, self.y, project.title)
        if project.link:
            self.canvas.setFillColor(BLUE)
            self.canvas.setFont(FONT, 6.8)
            self.canvas.drawRightString(self.width - self.right, self.y, project.link)
        self.y -= 10.5
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont(FONT, 7.8)
        for line in description_lines:
            self.canvas.drawString(self.left + 8, self.y, line)
            self.y -= 10.8
        self.y -= 4

    def compact_item(self, title: str, meta: str, detail: str = "") -> None:
        self.ensure(25)
        self.canvas.setFillColor(INK)
        self.canvas.setFont(FONT, 8.4)
        self.canvas.drawString(self.left, self.y, title)
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont(FONT, 7.0)
        self.canvas.drawRightString(self.width - self.right, self.y, meta)
        self.y -= 10
        if detail:
            self.canvas.setFillColor(MUTED)
            self.canvas.setFont(FONT, 7.55)
            for line in self.wrap(detail, 7.55, self.usable_width):
                self.canvas.drawString(self.left, self.y, line)
                self.y -= 10.2
        self.y -= 4

    def save(self) -> None:
        self.footer()
        self.canvas.save()


def english_experiences() -> tuple[Experience, ...]:
    return (
        Experience(
            "Samsung Electronics, AX Development Group",
            "SRE / AI Platform Engineer",
            "Jan. 2026 - Present",
            "Seoul, South Korea",
            (
                "Design and build an internal AX Agent Platform on AWS EKS, adapting the agent runtime and deployment path to enterprise platform standards.",
                "Implemented self-service AX application delivery with automatic domain issuance, authorized-only access, and platform controls for authentication, authorization, security, and governance.",
                "Enabled AX applications to call the existing enterprise LLM Gateway API through platform-side client compatibility and runtime integration.",
                "Supported a Microsoft-collaborative B2C generative AI service through UK rollout readiness, initial production operations, incident response, and stabilization from Jan. to Jun. 2026.",
            ),
        ),
        Experience(
            "Samsung Research",
            "SRE / AI Platform Engineer",
            "Jul. 2024 - Dec. 2025",
            "Seoul, South Korea",
            (
                "Led production delivery and application reliability for a company-wide AI chatbot serving 30,000 employees on internal Kubernetes clusters.",
                "Owned releases across development, staging, and production while integrating application delivery with security and operational requirements.",
                "Built container delivery pipelines with Docker, Kubernetes, GitHub Actions, ArgoCD, Helm, and Helmfile.",
                "Deployed Grafana, Prometheus, and OpenTelemetry observability and built a Python/MLflow evaluation workflow for LLM-based machine translation.",
            ),
        ),
        Experience(
            "Samsung Electronics, Network Division",
            "SRE & Software Engineer",
            "Jan. 2021 - Jun. 2024",
            "Seoul, South Korea",
            (
                "Designed and delivered containerized applications with Docker, Helm, Kubernetes Operators, and AWS services including EKS, ECS, Route 53, RDS, and IAM.",
                "Built and managed OpenShift, Kubernetes, and EKS environments for reliability, high availability, performance, and auto-scaling.",
                "Designed and developed a Bash-based one-click Kubernetes cluster provisioning system for cloud developers.",
                "Developed a Linux application that mirrors and forwards up to 130,000 packets per second under constrained system resources.",
            ),
        ),
        Experience(
            "TmaxOS & TmaxCloud",
            "Software & Platform Engineer",
            "Jan. 2019 - Dec. 2020",
            "Gyeonggi, South Korea",
            (
                "Built a Siri-like AI assistant on TmaxOS, covering model inference, data preprocessing, system integration, and asynchronous application flows.",
                "Designed and developed Kubernetes CI/CD and registry operators and deployed a private container image registry.",
            ),
        ),
    )


def korean_experiences() -> tuple[Experience, ...]:
    return (
        Experience(
            "삼성전자 AX Development Group",
            "SRE / AI 플랫폼 엔지니어",
            "2026.01 - 현재",
            "서울, 대한민국",
            (
                "AWS EKS 기반 사내 AX Agent Platform을 설계·구축하고, 에이전트 런타임과 배포 경로를 사내 플랫폼 표준에 맞게 조정했습니다.",
                "도메인 자동 발급과 인가된 사용자 전용 접근을 포함한 AX App 셀프서비스 배포 흐름을 구현하고 인증·인가·보안·거버넌스 통제를 담당했습니다.",
                "AX App이 기존 사내 LLM Gateway API를 호출할 수 있도록 플랫폼 측 클라이언트 호환성과 런타임 연동을 제공했습니다.",
                "2026.01~06 Microsoft와 협업한 B2C 생성형 AI 서비스의 UK 출시 준비, 초기 운영, 장애 대응 및 안정화를 수행했습니다.",
            ),
        ),
        Experience(
            "Samsung Research",
            "SRE / AI 플랫폼 엔지니어",
            "2024.07 - 2025.12",
            "서울, 대한민국",
            (
                "30,000명의 임직원이 사용하는 전사 AI 챗봇의 프로덕션 전달과 애플리케이션 신뢰성을 리딩했습니다.",
                "개발·스테이징·프로덕션 릴리스를 담당하며 애플리케이션 전달을 보안 및 운영 요구사항과 연결했습니다.",
                "Docker, Kubernetes, GitHub Actions, ArgoCD, Helm, Helmfile 기반 컨테이너 전달 파이프라인을 구축했습니다.",
                "Grafana, Prometheus, OpenTelemetry 관측 환경과 Python/MLflow 기반 기계 번역 LLM 평가 워크플로우를 구축했습니다.",
            ),
        ),
        Experience(
            "삼성전자 네트워크사업부",
            "SRE & 소프트웨어 엔지니어",
            "2021.01 - 2024.06",
            "서울, 대한민국",
            (
                "Docker, Helm, Kubernetes Operator와 AWS EKS, ECS, Route 53, RDS, IAM을 활용해 컨테이너 애플리케이션을 설계·전달했습니다.",
                "신뢰성·고가용성·성능·오토스케일링을 고려한 OpenShift, Kubernetes, EKS 환경을 구축·관리했습니다.",
                "Bash 기반 원클릭 Kubernetes 클러스터 프로비저닝 시스템을 설계·개발했습니다.",
                "제한된 시스템 리소스에서 초당 최대 130,000개 패킷을 미러링·전달하는 Linux 애플리케이션을 개발했습니다.",
            ),
        ),
        Experience(
            "TmaxOS & TmaxCloud",
            "소프트웨어 & 플랫폼 엔지니어",
            "2019.01 - 2020.12",
            "경기, 대한민국",
            (
                "TmaxOS 기반 Siri형 AI 어시스턴트의 모델 추론, 데이터 전처리, 시스템 연동 및 비동기 애플리케이션 흐름을 개발했습니다.",
                "Kubernetes CI/CD 및 레지스트리 Operator를 설계·개발하고 프라이빗 컨테이너 이미지 레지스트리를 배포했습니다.",
            ),
        ),
    )


PUBLIC_AI_PROJECT = Project(
    "Enterprise AI Assistant | Public reference implementation",
    "Built an access-aware Python assistant with SQLite FTS5 retrieval, pre-generation role filtering, grounded citations, audit events, evaluation cases, a FastAPI surface, and an optional OpenAI Responses API provider.",
    "jinwonlee.github.io/projects/enterprise-ai-assistant/web/",
)


def variants() -> tuple[ResumeVariant, ...]:
    experiences = english_experiences()
    common_skills = (
        ("Cloud & Platform", "AWS EKS, Azure, Kubernetes, OpenShift, Docker, Helm/Helmfile, ArgoCD, GitOps"),
        ("Software", "Python, Bash, Linux, Kubernetes Operators, API and runtime integration, asynchronous flows"),
        ("Reliability & Security", "Grafana, Prometheus, OpenTelemetry, incident response, authentication, authorization, security governance"),
        ("Applied AI Systems", "Agent application delivery, LLM evaluation with MLflow, existing LLM Gateway API integration, model inference"),
    )
    return (
        ResumeVariant(
            filename="Jinwon-Lee-CV-Master-2026-09.pdf",
            root_filename="CV-Eng.pdf",
            language="en",
            professional_title="Production AI & Platform Engineer",
            summary=(
                "Production AI and platform engineer with about eight years of experience delivering enterprise and user-facing systems across application software, cloud platforms, security, and operations.",
                "Carries work from architecture and implementation through integration, rollout, observability, incident response, and production stabilization.",
            ),
            evidence=(
                "AWS EKS platform for governed, self-service AX application delivery",
                "Production reliability for an enterprise AI service used by 30,000 employees",
                "Linux packet application measured at up to 130,000 packets per second",
            ),
            skills=common_skills,
            experiences=experiences,
            projects=(
                PUBLIC_AI_PROJECT,
                Project(
                    "LLM Performance Evaluation Pipeline",
                    "Built a Python and MLflow workflow for repeatable machine-translation model evaluation and result comparison on Kubernetes.",
                ),
                Project(
                    "Distributed CNN Training Research",
                    "Contributed to resource-aware layer placement for distributed TensorFlow training, reporting up to 2.3x training speedup in published research artifacts.",
                ),
                Project(
                    "High-throughput Packet Mirroring",
                    "Developed and tuned a Linux data-path application that mirrors and forwards up to 130,000 packets per second under constrained resources.",
                ),
            ),
        ),
        ResumeVariant(
            filename="Jinwon-Lee-CV-Platform-SRE-2026-09.pdf",
            root_filename="CV-Platform-SRE.pdf",
            language="en",
            professional_title="Platform & Site Reliability Engineer",
            summary=(
                "Platform and site reliability engineer with about eight years of experience building and operating cloud-native application platforms across AWS EKS, Azure, Kubernetes, and OpenShift.",
                "Combines platform software, release automation, observability, access control, and incident response to move services into reliable production operation.",
            ),
            evidence=(
                "AWS EKS agent platform with automated domains and authorized-only access",
                "Production delivery and reliability for a 30,000-employee AI service",
                "Kubernetes delivery, observability, and incident response across cloud environments",
            ),
            skills=(
                ("Platform", "AWS EKS, Kubernetes, OpenShift, Azure, Docker, Helm/Helmfile, Kubernetes Operators"),
                ("Delivery Automation", "ArgoCD, GitOps, GitHub Actions, Jenkins, CI/CD, Bash-based cluster provisioning"),
                ("Reliability", "Grafana, Prometheus, OpenTelemetry, high availability, auto-scaling, incident response"),
                ("Software & Security", "Python, Bash, Linux, API integration, authentication, authorization, security governance"),
            ),
            experiences=experiences,
            projects=(
                Project(
                    "Kubernetes Cluster Automation",
                    "Designed and developed a Bash-based one-click provisioning system for repeatable developer Kubernetes environments.",
                ),
                Project(
                    "Centralized Observability Stack",
                    "Deployed Grafana, Prometheus, and OpenTelemetry for shared service visibility, dashboards, and operational diagnosis.",
                ),
                Project(
                    "High-throughput Packet Mirroring",
                    "Developed a resource-aware Linux application measured at up to 130,000 packets per second.",
                ),
                Project(
                    "Internal AX Agent Platform",
                    "Built an AWS EKS application platform with automatic domains, authorized-only access, enterprise security controls, and compatibility with an existing LLM Gateway API.",
                ),
            ),
        ),
        ResumeVariant(
            filename="Jinwon-Lee-CV-Applied-AI-2026-09.pdf",
            root_filename="CV-Applied-AI.pdf",
            language="en",
            professional_title="Applied AI & Platform Engineer",
            summary=(
                "Applied AI and platform engineer with about eight years of experience turning enterprise requirements into production systems, including agent application delivery, LLM evaluation, model integration, access control, and reliability engineering.",
                "Builds hands-on across Python application logic, cloud-native runtime integration, evaluation, security controls, rollout, and production operations.",
            ),
            evidence=(
                "Governed AX application delivery with existing enterprise LLM Gateway integration",
                "Public assistant reference with retrieval, RBAC, citations, audit, and evals",
                "Python/MLflow LLM evaluation plus production operation of enterprise AI services",
            ),
            skills=(
                ("Applied AI", "Agent application delivery, retrieval, grounded citations, evaluation cases, model inference, LLM Gateway API integration"),
                ("Software", "Python, FastAPI, SQLite FTS5, Bash, Linux, API and runtime integration, asynchronous flows"),
                ("Cloud Platform", "AWS EKS, Azure, Kubernetes, OpenShift, Docker, Helm/Helmfile, ArgoCD"),
                ("Production Quality", "Authentication, authorization, governance, observability, incident response, rollout stabilization"),
            ),
            experiences=experiences,
            projects=(
                PUBLIC_AI_PROJECT,
                Project(
                    "LLM Performance Evaluation Pipeline",
                    "Built a Python and MLflow workflow for repeatable machine-translation LLM evaluation and result comparison on Kubernetes.",
                ),
                Project(
                    "TmaxOS AI Assistant",
                    "Built model inference, preprocessing, system integration, and asynchronous interaction flows for an OS-level AI assistant.",
                ),
                Project(
                    "Distributed CNN Training Research",
                    "Studied resource-aware placement for distributed TensorFlow training and contributed to research artifacts reporting up to 2.3x training speedup.",
                ),
            ),
        ),
        ResumeVariant(
            filename="Jinwon-Lee-CV-Kor-2026-09.pdf",
            root_filename="CV-Kor.pdf",
            language="ko",
            professional_title="프로덕션 AI & 플랫폼 엔지니어",
            summary=(
                "약 8년 동안 애플리케이션 소프트웨어, 클라우드 플랫폼, 보안 및 운영을 아우르며 엔터프라이즈·사용자 대상 시스템을 프로덕션까지 전달해 온 AI·플랫폼 엔지니어입니다.",
                "아키텍처와 구현부터 연동, 출시, 관측, 장애 대응 및 초기 안정화까지 직접 이어가는 것이 강점입니다.",
            ),
            evidence=(
                "AWS EKS 기반 거버넌스·셀프서비스 AX App 배포 플랫폼",
                "30,000명 임직원 대상 전사 AI 서비스 프로덕션 신뢰성",
                "초당 최대 130,000개 패킷 처리 Linux 애플리케이션",
            ),
            skills=(
                ("클라우드 & 플랫폼", "AWS EKS, Azure, Kubernetes, OpenShift, Docker, Helm/Helmfile, ArgoCD, GitOps"),
                ("소프트웨어", "Python, Bash, Linux, Kubernetes Operator, API·런타임 연동, 비동기 흐름"),
                ("신뢰성 & 보안", "Grafana, Prometheus, OpenTelemetry, 장애 대응, 인증·인가, 보안 거버넌스"),
                ("Applied AI", "Agent App 전달, MLflow 기반 LLM 평가, 기존 LLM Gateway API 연동, 모델 추론"),
            ),
            experiences=korean_experiences(),
            projects=(
                Project(
                    "Enterprise AI Assistant | 공개 레퍼런스 구현",
                    "SQLite FTS5 검색, 생성 전 역할 기반 권한 필터, 근거 인용, 감사 이벤트, 평가 케이스, FastAPI 및 선택적 OpenAI Responses API 연동을 구현했습니다.",
                    "jinwonlee.github.io/projects/enterprise-ai-assistant/web/",
                ),
                Project(
                    "LLM 성능 평가 파이프라인",
                    "Kubernetes에서 기계 번역 모델을 반복 평가·비교할 수 있도록 Python/MLflow 워크플로우를 구축했습니다.",
                ),
                Project(
                    "분산 CNN 학습 연구",
                    "분산 TensorFlow 학습의 리소스 인지 레이어 배치 연구에 참여해 발표 자료에서 최대 2.3배 학습 속도 향상을 보고했습니다.",
                ),
                Project(
                    "고처리량 패킷 미러링",
                    "제한된 리소스에서 초당 최대 130,000개 패킷을 미러링·전달하도록 Linux 데이터 경로 애플리케이션을 개발·튜닝했습니다.",
                ),
            ),
        ),
    )


def build_resume(variant: ResumeVariant) -> str:
    path = os.path.join(OUTPUT_DIR, variant.filename)
    doc = ResumeDocument(path, variant.language, variant.professional_title)
    doc.header()
    doc.section("Profile" if variant.language == "en" else "프로필")
    for paragraph in variant.summary:
        doc.paragraph(paragraph)
    doc.section("Selected Evidence" if variant.language == "en" else "핵심 근거")
    doc.evidence(variant.evidence)
    doc.section("Core Skills" if variant.language == "en" else "핵심 역량")
    doc.skill_rows(variant.skills)
    doc.section("Experience" if variant.language == "en" else "경력")
    for experience in variant.experiences[:3]:
        doc.experience(experience)

    doc.new_page()
    doc.section("Experience (continued)" if variant.language == "en" else "경력 (계속)")
    for experience in variant.experiences[3:]:
        doc.experience(experience)

    doc.section("Selected Engineering Work" if variant.language == "en" else "주요 엔지니어링 작업")
    for project in variant.projects:
        doc.project(project)

    doc.section("Education & Research" if variant.language == "en" else "학력 & 연구")
    if variant.language == "en":
        doc.compact_item(
            "UNIST | M.S. in Computer Science and Engineering",
            "Mar. 2017 - Feb. 2019",
            "Master's thesis: Convergence Aware CNN Training | Advisors: Jiwon Seo and Sam H. Noh",
        )
        doc.compact_item(
            "UNIST | B.S. in Computer Science and Engineering, Minor in Mathematics",
            "Mar. 2012 - Feb. 2017",
            "Undergraduate research: distributed systems for AI model training with TensorFlow",
        )
    else:
        doc.compact_item(
            "UNIST | 컴퓨터공학 석사",
            "2017.03 - 2019.02",
            "석사 논문: Convergence Aware CNN Training | 지도교수: 서지원, 노삼혁",
        )
        doc.compact_item(
            "UNIST | 컴퓨터공학 학사, 수학 부전공",
            "2012.03 - 2017.02",
            "학부 연구: TensorFlow 기반 AI 모델 학습을 위한 분산 시스템",
        )

    doc.section("Publications & Language" if variant.language == "en" else "논문 & 어학")
    publications = (
        "USENIX NSDI 2019 poster: Alleviating the Network Bottleneck for CNN Distributed Training through Automatic Resource-Aware Layer Placement.",
        "arXiv 2019: Accelerated Training for CNN Distributed Deep Learning through Automatic Resource-Aware Layer Placement.",
        "ACM EuroSys 2018 poster: Improving Performance of Distributed TensorFlow using CNN Characteristics Exploiting Model Parallelism.",
        "OPIc IH (Intermediate High), Dec. 2025.",
    ) if variant.language == "en" else (
        "USENIX NSDI 2019 poster: Alleviating the Network Bottleneck for CNN Distributed Training through Automatic Resource-Aware Layer Placement.",
        "arXiv 2019: Accelerated Training for CNN Distributed Deep Learning through Automatic Resource-Aware Layer Placement.",
        "ACM EuroSys 2018 poster: Improving Performance of Distributed TensorFlow using CNN Characteristics Exploiting Model Parallelism.",
        "OPIc IH (Intermediate High), 2025.12.",
    )
    doc.bullets(publications, size=7.45, leading=10.1, gap=1.5)
    doc.save()
    shutil.copyfile(path, os.path.join(ROOT, variant.root_filename))
    return path


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for variant in variants():
        build_resume(variant)


if __name__ == "__main__":
    main()
