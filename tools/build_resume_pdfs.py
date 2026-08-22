from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT, "output", "pdf")
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

FONT = "ArialUnicode"
pdfmetrics.registerFont(TTFont(FONT, FONT_PATH))


def load_motto(lang: str) -> str:
    filename = "portfolio-config-ko.json" if lang == "ko" else "portfolio-config.json"
    with open(os.path.join(ROOT, filename), encoding="utf-8") as f:
        return json.load(f)["personal"]["motto"]


@dataclass
class Experience:
    company: str
    role: str
    period: str
    location: str
    bullets: Sequence[str]


@dataclass
class Education:
    school: str
    degree: str
    period: str
    details: Sequence[str]


class ResumeCanvas:
    def __init__(self, filename: str, lang: str):
        self.filename = filename
        self.lang = lang
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.w, self.h = A4
        self.left = 21 * mm
        self.right = 21 * mm
        self.top = 19 * mm
        self.bottom = 17 * mm
        self.y = self.h - self.top
        self.page = 1
        self.accent = colors.HexColor("#B88A2E")
        self.text = colors.HexColor("#242424")
        self.muted = colors.HexColor("#5A5A5A")
        self.light = colors.HexColor("#E8E0D2")

    @property
    def usable(self) -> float:
        return self.w - self.left - self.right

    def save(self):
        self.footer()
        self.c.save()

    def footer(self):
        self.c.setFont(FONT, 7)
        self.c.setFillColor(self.muted)
        label = "Updated Aug 2026"
        self.c.drawString(self.left, 10 * mm, label)
        self.c.drawRightString(self.w - self.right, 10 * mm, f"{self.page}")

    def new_page(self):
        self.footer()
        self.c.showPage()
        self.page += 1
        self.y = self.h - self.top

    def ensure(self, needed: float):
        if self.y - needed < self.bottom:
            self.new_page()

    def draw_line(self, x1: float, y: float, x2: float, color=colors.HexColor("#D9D9D9")):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(0.5)
        self.c.line(x1, y, x2, y)

    def fill_rect(self, x: float, y: float, w: float, h: float, color):
        self.c.setFillColor(color)
        self.c.rect(x, y, w, h, stroke=0, fill=1)

    def text_width(self, s: str, size: float) -> float:
        return pdfmetrics.stringWidth(s, FONT, size)

    def wrap(self, text: str, size: float, width: float) -> List[str]:
        words = text.split(" ")
        lines: List[str] = []
        cur = ""
        for word in words:
            trial = word if not cur else f"{cur} {word}"
            if self.text_width(trial, size) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                if self.text_width(word, size) <= width:
                    cur = word
                else:
                    chunk = ""
                    for ch in word:
                        trial_chunk = chunk + ch
                        if self.text_width(trial_chunk, size) <= width:
                            chunk = trial_chunk
                        else:
                            if chunk:
                                lines.append(chunk)
                            chunk = ch
                    cur = chunk
        if cur:
            lines.append(cur)
        return lines

    def paragraph(self, text: str, size=8.8, leading=12.6, color=None, width=None, x=None):
        width = self.usable if width is None else width
        x = self.left if x is None else x
        color = self.text if color is None else color
        lines = self.wrap(text, size, width)
        self.ensure(len(lines) * leading + 2)
        self.c.setFont(FONT, size)
        self.c.setFillColor(color)
        for line in lines:
            self.c.drawString(x, self.y, line)
            self.y -= leading
        self.y -= 3

    def heading(self, title: str):
        self.ensure(22)
        self.y -= 7
        self.c.setFont(FONT, 10.4)
        self.c.setFillColor(self.accent)
        self.c.drawString(self.left, self.y, title.upper())
        self.draw_line(self.left + self.text_width(title.upper(), 10.4) + 6, self.y + 2, self.w - self.right)
        self.y -= 15

    def bullet_list(self, bullets: Iterable[str], size=8.15, leading=11.7, indent=4.6 * mm, x=None, width=None):
        x = self.left if x is None else x
        width = self.usable if width is None else width
        for bullet in bullets:
            lines = self.wrap(bullet, size, width - indent)
            self.ensure(len(lines) * leading + 2)
            self.c.setFillColor(self.accent)
            self.c.setFont(FONT, size)
            self.c.drawString(x, self.y, "•")
            self.c.setFillColor(self.text)
            for i, line in enumerate(lines):
                self.c.drawString(x + indent, self.y, line)
                self.y -= leading
            self.y -= 2

    def header(self, name: str, title: str, contact: str, motto: str, focus: Sequence[str]):
        box_w = 54 * mm
        gap = 9 * mm
        box_x = self.w - self.right - box_w
        left_w = self.usable - box_w - gap
        header_top = self.y

        self.c.setFillColor(colors.HexColor("#111111"))
        self.c.setFont(FONT, 24)
        self.c.drawString(self.left, self.y, name)
        self.y -= 18
        self.c.setFillColor(self.accent)
        self.c.setFont(FONT, 10.3)
        self.c.drawString(self.left, self.y, title)
        self.y -= 13
        self.c.setFillColor(self.muted)
        self.c.setFont(FONT, 7.8)
        for line in self.wrap(contact, 7.8, left_w):
            self.c.drawString(self.left, self.y, line)
            self.y -= 10
        self.y -= 2
        self.c.setFillColor(colors.HexColor("#404040"))
        self.c.setFont(FONT, 8.6)
        self.c.drawString(self.left, self.y, f'"{motto}"')
        self.y -= 16

        box_h = header_top - self.y - 2
        self.c.setFillColor(colors.HexColor("#FAF7F0"))
        self.c.roundRect(box_x, self.y + 7, box_w, box_h, 4, fill=1, stroke=0)
        self.c.setFillColor(self.accent)
        self.c.setFont(FONT, 7.4)
        label = "TARGET FIT" if self.lang == "en" else "지원 포지션 적합도"
        self.c.drawString(box_x + 5 * mm, header_top - 9, label)
        yy = header_top - 22
        self.c.setFont(FONT, 7.7)
        self.c.setFillColor(self.text)
        for item in focus:
            self.c.setFillColor(self.accent)
            self.c.drawString(box_x + 5 * mm, yy, "•")
            self.c.setFillColor(self.text)
            for i, line in enumerate(self.wrap(item, 7.7, box_w - 13 * mm)):
                self.c.drawString(box_x + 8 * mm, yy, line)
                yy -= 9.4
            yy -= 1

        self.draw_line(self.left, self.y, self.w - self.right, self.accent)
        self.y -= 13

    def summary_panel(self, paragraphs: Sequence[str]):
        size = 8.7
        leading = 12.4
        pad_x = 5 * mm
        pad_y = 4 * mm
        lines_by_para = [self.wrap(text, size, self.usable - 2 * pad_x) for text in paragraphs]
        needed = 2 * pad_y + sum(len(lines) * leading for lines in lines_by_para) + (len(paragraphs) - 1) * 4
        self.ensure(needed + 3)
        top = self.y
        self.fill_rect(self.left, top - needed + 2, self.usable, needed, colors.HexColor("#FAF8F3"))
        self.fill_rect(self.left, top - needed + 2, 2.1 * mm, needed, self.accent)
        self.c.setFont(FONT, size)
        self.c.setFillColor(self.text)
        yy = top - pad_y
        for lines in lines_by_para:
            for line in lines:
                self.c.drawString(self.left + pad_x, yy, line)
                yy -= leading
            yy -= 4
        self.y = top - needed - 18

    def chips(self, items: Sequence[str]):
        x = self.left
        box_h = 13.5
        self.ensure(32)
        for item in items:
            box_w = self.text_width(item, 7.5) + 12
            if x + box_w > self.w - self.right:
                x = self.left
                self.y -= box_h + 6
            self.c.setFillColor(colors.HexColor("#F8F4EC"))
            self.c.roundRect(x, self.y - 3, box_w, box_h, 3, fill=1, stroke=0)
            self.c.setFillColor(colors.HexColor("#7A5B18"))
            self.c.setFont(FONT, 7.5)
            self.c.drawString(x + 6, self.y, item)
            x += box_w + 6
        self.y -= box_h + 11

    def skill_block(self, rows: Sequence[tuple[str, str]]):
        label_w = 39 * mm
        for label, text in rows:
            lines = self.wrap(text, 8.0, self.usable - label_w - 6)
            self.ensure(max(14, len(lines) * 11.5) + 3)
            self.draw_line(self.left, self.y + 4, self.w - self.right, colors.HexColor("#EFE7DA"))
            self.c.setFont(FONT, 8.0)
            self.c.setFillColor(self.accent)
            self.c.drawString(self.left, self.y, label)
            self.c.setFillColor(self.text)
            yy = self.y
            for line in lines:
                self.c.drawString(self.left + label_w, yy, line)
                yy -= 11.5
            self.y = yy - 2

    def experience(self, exp: Experience):
        est = 34 + len(exp.bullets) * 23
        self.ensure(min(est, 105))
        start_y = self.y + 2
        rail_x = self.left + 1.8 * mm
        content_x = self.left + 7.5 * mm
        content_w = self.w - self.right - content_x
        self.c.setStrokeColor(colors.HexColor("#E7D8BF"))
        self.c.setLineWidth(0.7)
        self.c.line(rail_x, start_y - 6, rail_x, start_y - min(est, 105) + 14)
        self.c.setFillColor(self.accent)
        self.c.circle(rail_x, start_y - 2, 1.55 * mm, stroke=0, fill=1)
        self.c.setFillColor(colors.HexColor("#111111"))
        self.c.setFont(FONT, 10.0)
        self.c.drawString(content_x, self.y, exp.company)
        self.c.setFillColor(self.muted)
        self.c.setFont(FONT, 7.9)
        self.c.drawRightString(self.w - self.right, self.y, exp.location)
        self.y -= 11
        self.c.setFillColor(self.accent)
        self.c.setFont(FONT, 8.6)
        self.c.drawString(content_x, self.y, exp.role)
        self.c.setFillColor(self.muted)
        self.c.drawRightString(self.w - self.right, self.y, exp.period)
        self.y -= 12
        self.bullet_list(exp.bullets, x=content_x, width=content_w)
        self.y -= 5

    def education(self, edu: Education):
        self.ensure(44)
        self.c.setFont(FONT, 9.2)
        self.c.setFillColor(colors.HexColor("#111111"))
        self.c.drawString(self.left, self.y, edu.school)
        self.c.setFillColor(self.muted)
        self.c.setFont(FONT, 7.9)
        self.c.drawRightString(self.w - self.right, self.y, edu.period)
        self.y -= 11
        self.paragraph(edu.degree, size=8.1, leading=11.5)
        self.bullet_list(edu.details, size=7.8, leading=11.0)


def build_english():
    r = ResumeCanvas(os.path.join(OUTPUT_DIR, "Jinwon-Lee-CV-Eng-2026-08.pdf"), "en")
    r.header(
        "Jinwon Lee",
        "AI Platform Software & SRE Engineer",
        "Seoul, South Korea | +82 10-2422-1429 | dlwlsdnjsehs1993@gmail.com | github.com/JINwonLEE | linkedin.com/in/jwl1993",
        load_motto("en"),
        ["AI Platform Software", "MLOps / Model Serving", "Kubernetes Infrastructure", "System Software"],
    )
    r.heading("Summary")
    r.summary_panel(
        [
            "At Samsung Electronics, I design and build an internal AX Agent Platform while working on SRE and platform engineering for generative AI services. "
            "For about eight years, I have built and operated Kubernetes-based services, cloud infrastructure automation, CI/CD, observability, and AI evaluation/serving workflows.",
            'My strength is taking AI applications beyond "working code" and turning them into systems that real users can rely on. '
            "I consider deployment, authentication, monitoring, incident response, and resource constraints together to build platforms where applications can run smoothly and reliably.",
        ]
    )
    r.chips(["AI Platform Software", "MLOps & Model Serving", "System Software & Performance", "Cloud/Kubernetes Infrastructure"])

    r.heading("Core Skills")
    r.skill_block(
        [
            ("AI/MLOps", "LLM evaluation pipeline, MLflow metric tracking, AI serving operations, Document LLM platform, Langfuse observability"),
            ("Platform", "Kubernetes, AWS EKS, Azure, OpenShift, Docker, Helm/Helmfile, ArgoCD, GitOps, Terraform, Ansible"),
            ("System", "Linux runtime behavior, Python automation, high-throughput packet mirroring, distributed systems, resource-aware optimization"),
            ("Reliability", "Authentication/authorization, security governance, domain provisioning, Grafana, Prometheus, OpenTelemetry, incident response"),
        ]
    )

    r.heading("Experience")
    experiences = [
        Experience(
            "Samsung Electronics (AX Development Group)",
            "SRE / AI Platform Engineer",
            "Jan. 2026 - Present",
            "Seoul, South Korea",
            [
                "Global B2C Generative AI Service (Jan. 2026 - Jun. 2026): Supported the UK expansion, initial production operations, and incident response for a Microsoft Azure-based service in collaboration with Microsoft.",
                "AX Agent Platform (Jul. 2026 - Present): Designed and built an internal platform on AWS EKS, adapting the agent runtime and deployment environment to internal platform standards.",
                "Owned authentication, authorization, security, and internal governance while building self-service deployment with automatic domain provisioning and authorized-only access.",
                "Enabled deployed AX applications to consume the existing enterprise LLM Gateway API through platform-side client compatibility and integration, without owning the Gateway design.",
            ],
        ),
        Experience(
            "Samsung Research",
            "SRE / AI Platform Engineer",
            "Jul. 2024 - Dec. 2025",
            "Seoul, South Korea",
            [
                "Operated a company-wide AI chatbot service on internal Kubernetes clusters, owning platform and application reliability for production use.",
                "Led infrastructure, platform, and application operations for a company-wide AI chatbot platform serving 30,000 employees on Kubernetes.",
                "Provisioned and operated development, staging, and production Kubernetes clusters using Helm and Helmfile.",
                "Built automated CI/CD pipelines for containerized applications with Docker, Kubernetes, GitHub Actions, and ArgoCD.",
                "Deployed centralized monitoring with Grafana, Prometheus, and OpenTelemetry, and built an automated LLM evaluation pipeline for Machine Translation tasks.",
            ],
        ),
        Experience(
            "Samsung Electronics (Network Dept.)",
            "SRE & Software Engineer",
            "Jan. 2021 - Jun. 2024",
            "Seoul, South Korea",
            [
                "Deployed containerized applications using Docker, Helm, Kubernetes Operator, and AWS services including EKS, ECS, Route 53, RDS, and IAM.",
                "Built and managed OpenShift, Kubernetes, and EKS environments with focus on performance, reliability, high availability, and auto-scaling.",
                "Developed an automated one-click Kubernetes cluster provisioning system for cloud developers.",
                "Developed an application that mirrors up to 130,000 packets per second in real time under constrained system resources.",
            ],
        ),
        Experience(
            "TmaxOS & TmaxCloud",
            "Software & Platform Engineer",
            "Jan. 2019 - Dec. 2020",
            "Gyeonggi, South Korea",
            [
                "Developed CI/CD and registry operators in Kubernetes and deployed a private container image registry.",
                "Built a Siri-like AI assistant on TmaxOS with system-level integration, AI model inference, preprocessing, and asynchronous architecture.",
            ],
        ),
    ]
    for index, exp in enumerate(experiences):
        if index == 2:
            r.new_page()
            r.heading("Experience (continued)")
        r.experience(exp)

    r.heading("Education")
    for edu in [
        Education(
            "UNIST (Ulsan National Institute of Science and Technology)",
            "M.S. in Computer Science and Engineering",
            "Mar. 2017 - Feb. 2019",
            ["Master Thesis: Convergence Aware CNN Training", "Advisors: Jiwon Seo (Hanyang University), Sam H. Noh (UNIST)"],
        ),
        Education(
            "UNIST (Ulsan National Institute of Science and Technology)",
            "B.S. in Computer Science and Engineering; Minor in Mathematics",
            "Mar. 2012 - Feb. 2017",
            ["Undergraduate research: distributed systems for AI model training with TensorFlow"],
        ),
    ]:
        r.education(edu)

    r.heading("Certifications & Language")
    r.bullet_list(["OPIc IH (Intermediate High), Dec. 2025"], size=7.4, leading=9.8)

    r.heading("Publications")
    r.bullet_list(
        [
            "Alleviating the Network Bottleneck for CNN Distributed Training through Automatic Resource-Aware Layer Placement, USENIX NSDI 2019 poster.",
            "Accelerated Training for CNN Distributed Deep Learning through Automatic Resource-Aware Layer Placement, arXiv 2019.",
            "Improving Performance of Distributed TensorFlow using CNN Characteristics Exploiting Model Parallelism, ACM EuroSys 2018 poster.",
        ],
        size=7.4,
        leading=9.8,
    )
    r.save()


def build_korean():
    r = ResumeCanvas(os.path.join(OUTPUT_DIR, "Jinwon-Lee-CV-Kor-2026-08.pdf"), "ko")
    r.header(
        "이진원",
        "AI 플랫폼 소프트웨어 & SRE 엔지니어",
        "서울, 대한민국 | +82 10-2422-1429 | dlwlsdnjsehs1993@gmail.com | github.com/JINwonLEE | linkedin.com/in/jwl1993",
        load_motto("ko"),
        ["AI 플랫폼 소프트웨어", "MLOps / 모델 서빙", "Kubernetes 인프라", "시스템 소프트웨어"],
    )
    r.heading("요약")
    r.summary_panel(
        [
            "삼성전자에서 사내 AX Agent Platform을 설계·구축하며 생성형 AI 서비스의 SRE/플랫폼 엔지니어링을 담당하고 있습니다. "
            "약 8년 동안 Kubernetes 기반 서비스 운영, 클라우드 인프라 자동화, CI/CD, 관측 가능성, AI 평가/서빙 워크플로우를 다뤄왔습니다.",
            '제가 잘하는 일은 AI 애플리케이션을 "동작하는 코드"에서 실제 사용자가 안정적으로 쓸 수 있는 운영 구조로 옮기는 것입니다. '
            "배포, 인증, 모니터링, 장애 대응, 리소스 제약을 함께 고려해 애플리케이션이 원활하게 동작할 수 있는 플랫폼을 만듭니다.",
        ]
    )
    r.chips(["AI 플랫폼 소프트웨어", "MLOps & 모델 서빙", "시스템 소프트웨어 & 성능", "클라우드/Kubernetes 인프라"])

    r.heading("핵심 역량")
    r.skill_block(
        [
            ("AI/MLOps", "LLM 평가 파이프라인, MLflow 메트릭 추적, AI 서빙 운영, Document LLM 플랫폼, Langfuse 관측 가능성"),
            ("플랫폼", "Kubernetes, AWS EKS, Azure, OpenShift, Docker, Helm/Helmfile, ArgoCD, GitOps, Terraform, Ansible"),
            ("시스템", "Linux 런타임 동작, Python 자동화, 고성능 패킷 미러링, 분산 시스템, 리소스 인식 최적화"),
            ("신뢰성", "인증·인가, 보안 거버넌스, 도메인 자동 발급, Grafana, Prometheus, OpenTelemetry, 장애 대응"),
        ]
    )

    r.heading("경력")
    experiences = [
        Experience(
            "삼성전자 (AX Development Group)",
            "SRE / AI 플랫폼 엔지니어",
            "2026.01 - 현재",
            "서울, 대한민국",
            [
                "글로벌 B2C 생성형 AI 서비스 (2026.01 - 2026.06): Microsoft와 협업하여 Azure 기반 서비스의 UK 확장, 초기 프로덕션 운영 및 장애 대응을 수행했습니다.",
                "AX Agent Platform (2026.07 - 현재): AWS EKS 기반 사내 플랫폼을 설계·구축하고, AX Agent의 실행·배포 환경을 사내 플랫폼 규격에 맞게 조정했습니다.",
                "인증·인가·보안 및 사내 거버넌스를 담당하고, AX App 배포 시 도메인을 자동 발급하여 인가된 사용자만 접근할 수 있는 셀프서비스 구조를 구축했습니다.",
                "배포된 AX App이 기존 사내 LLM Gateway API를 사용할 수 있도록 플랫폼 측 클라이언트 호환성과 연동을 제공했으며, Gateway 자체 설계는 담당하지 않았습니다.",
            ],
        ),
        Experience(
            "삼성리서치 (Samsung Research)",
            "SRE / AI 플랫폼 엔지니어",
            "2024.07 - 2025.12",
            "서울, 대한민국",
            [
                "사내 Kubernetes 클러스터 기반 전사 AI 챗봇 서비스를 운영하며 프로덕션 사용을 위한 플랫폼 및 애플리케이션 신뢰성을 담당했습니다.",
                "약 30,000명의 임직원이 사용하는 전사 AI 챗봇 플랫폼의 Kubernetes 기반 인프라, 플랫폼, 애플리케이션 운영을 담당했습니다.",
                "Helm/Helmfile을 활용하여 개발, 스테이징, 프로덕션 Kubernetes 클러스터를 프로비저닝하고 운영했습니다.",
                "Docker, Kubernetes, GitHub Actions, ArgoCD를 활용해 컨테이너화된 애플리케이션의 CI/CD 파이프라인을 구축했습니다.",
                "Grafana, Prometheus, OpenTelemetry 기반 중앙 모니터링을 배포하고, 기계 번역 태스크용 LLM 평가 자동화 파이프라인을 구축했습니다.",
            ],
        ),
        Experience(
            "삼성전자 (Network Dept.)",
            "SRE & 소프트웨어 엔지니어",
            "2021.01 - 2024.06",
            "서울, 대한민국",
            [
                "Docker, Helm, Kubernetes Operator 및 AWS(EKS, ECS, Route 53, RDS, IAM 등)를 활용해 컨테이너화된 애플리케이션을 배포했습니다.",
                "OpenShift, Kubernetes, EKS 환경을 구축/관리하며 성능, 안정성, 고가용성, 오토스케일링을 고려한 운영을 수행했습니다.",
                "클라우드 개발자를 위한 Kubernetes 클러스터 원클릭 프로비저닝 시스템을 개발했습니다.",
                "제한된 시스템 리소스에서 초당 최대 130,000개의 패킷을 실시간으로 미러링해 타겟 서버로 전달하는 애플리케이션을 개발했습니다.",
            ],
        ),
        Experience(
            "티맥스OS & 티맥스클라우드",
            "소프트웨어 & 플랫폼 엔지니어",
            "2019.01 - 2020.12",
            "경기, 대한민국",
            [
                "Kubernetes 환경에서 CI/CD 및 레지스트리 오퍼레이터를 개발하고 프라이빗 컨테이너 이미지 레지스트리를 배포했습니다.",
                "TmaxOS 기반 Siri형 AI 어시스턴트를 개발하며 시스템 수준 통합, AI 모델 추론, 데이터 전처리, 비동기 아키텍처를 담당했습니다.",
            ],
        ),
    ]
    for index, exp in enumerate(experiences):
        if index == 2:
            r.new_page()
            r.heading("경력 (계속)")
        r.experience(exp)

    r.heading("학력")
    for edu in [
        Education(
            "UNIST (울산과학기술원)",
            "M.S. 컴퓨터 공학과",
            "2017.03 - 2019.02",
            ["석사 졸업 논문: Convergence Aware CNN Training", "지도교수: 서지원 (한양대학교), 노삼혁 (UNIST)"],
        ),
        Education(
            "UNIST (울산과학기술원)",
            "B.S. 컴퓨터 공학과; 부전공 수학",
            "2012.03 - 2017.02",
            ["학부 연구: TensorFlow 기반 AI 모델 학습을 위한 분산 시스템"],
        ),
    ]:
        r.education(edu)

    r.heading("자격/어학")
    r.bullet_list(["OPIc IH (Intermediate High), 2025.12 취득"], size=7.4, leading=9.8)

    r.heading("논문/발표")
    r.bullet_list(
        [
            "Alleviating the Network Bottleneck for CNN Distributed Training through Automatic Resource-Aware Layer Placement, USENIX NSDI 2019 poster.",
            "Accelerated Training for CNN Distributed Deep Learning through Automatic Resource-Aware Layer Placement, arXiv 2019.",
            "Improving Performance of Distributed TensorFlow using CNN Characteristics Exploiting Model Parallelism, ACM EuroSys 2018 poster.",
        ],
        size=7.4,
        leading=9.8,
    )
    r.save()


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_english()
    build_korean()
