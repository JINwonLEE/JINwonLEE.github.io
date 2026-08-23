from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT, "output", "pdf")
OUTPUTS = {
    "ko": os.path.join(OUTPUT_DIR, "Jinwon-Lee-Portfolio-Kor-2026-08-v3.pdf"),
    "en": os.path.join(OUTPUT_DIR, "Jinwon-Lee-Portfolio-Eng-2026-08-v3.pdf"),
}
CONFIGS = {
    "ko": os.path.join(ROOT, "portfolio-config-ko.json"),
    "en": os.path.join(ROOT, "portfolio-config.json"),
}
PORTFOLIO_URL = "https://jinwonlee.github.io/"

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

FONT = "ArialUnicode"
pdfmetrics.registerFont(TTFont(FONT, FONT_PATH))


@dataclass
class Project:
    title: str
    description: str
    problem: str
    role: str
    engineering: str
    outcome: str
    relevance: str
    technologies: Sequence[str]


class PortfolioPDF:
    def __init__(self, filename: str, lang: str):
        self.filename = filename
        self.lang = lang
        self.c = canvas.Canvas(filename, pagesize=landscape(A4))
        self.w, self.h = landscape(A4)
        self.left = 20 * mm
        self.right = 20 * mm
        self.top = 17 * mm
        self.bottom = 15 * mm
        self.page = 1
        self.bg = colors.HexColor("#151516")
        self.panel = colors.HexColor("#202124")
        self.panel2 = colors.HexColor("#24262B")
        self.text = colors.HexColor("#F7F3EA")
        self.body = colors.HexColor("#D9D3C8")
        self.muted = colors.HexColor("#A9A196")
        self.accent = colors.HexColor("#D5A642")
        self.blue = colors.HexColor("#67C7E8")
        self.green = colors.HexColor("#70D79E")
        self.purple = colors.HexColor("#B89DFF")
        self.line = colors.HexColor("#514A3D")

    @property
    def usable(self) -> float:
        return self.w - self.left - self.right

    def save(self):
        self.c.save()

    def page_bg(self, eyebrow: str | None = None):
        self.c.setFillColor(self.bg)
        self.c.rect(0, 0, self.w, self.h, stroke=0, fill=1)
        self.c.setFillColor(colors.HexColor("#223033"))
        self.c.circle(self.w - 42 * mm, self.h - 20 * mm, 42 * mm, stroke=0, fill=1)
        self.c.setFillColor(colors.HexColor("#242424"))
        self.c.circle(24 * mm, 8 * mm, 58 * mm, stroke=0, fill=1)
        if eyebrow:
            self.text_at(self.left, self.h - self.top, eyebrow, 10, self.accent, 700)
        self.footer()

    def footer(self):
        y = 10 * mm
        self.c.setStrokeColor(colors.HexColor("#2F2D2A"))
        self.c.setLineWidth(0.5)
        self.c.line(self.left, y + 8, self.w - self.right, y + 8)
        self.text_at(self.left, y, PORTFOLIO_URL, 7.5, self.muted)
        self.c.linkURL(PORTFOLIO_URL, (self.left, y - 2, self.left + 42 * mm, y + 8), relative=0)
        self.text_right(self.w - self.right, y, str(self.page), 7.5, self.muted)

    def new_page(self, eyebrow: str | None = None):
        self.c.showPage()
        self.page += 1
        self.page_bg(eyebrow)

    def text_width(self, value: str, size: float) -> float:
        return pdfmetrics.stringWidth(value, FONT, size)

    def wrap(self, value: str, size: float, width: float) -> List[str]:
        words = value.split(" ")
        lines: List[str] = []
        current = ""
        for word in words:
            trial = word if not current else f"{current} {word}"
            if self.text_width(trial, size) <= width:
                current = trial
                continue
            if current:
                lines.append(current)
            if self.text_width(word, size) <= width:
                current = word
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
                current = chunk
        if current:
            lines.append(current)
        return lines

    def text_at(self, x: float, y: float, value: str, size: float, color=None, weight: int = 400):
        self.c.setFont(FONT, size)
        self.c.setFillColor(color or self.text)
        self.c.drawString(x, y, value)

    def text_right(self, x: float, y: float, value: str, size: float, color=None):
        self.c.setFont(FONT, size)
        self.c.setFillColor(color or self.text)
        self.c.drawRightString(x, y, value)

    def paragraph(self, x: float, y: float, value: str, width: float, size: float = 9, leading: float = 13, color=None) -> float:
        self.c.setFont(FONT, size)
        self.c.setFillColor(color or self.body)
        for line in self.wrap(value, size, width):
            self.c.drawString(x, y, line)
            y -= leading
        return y

    def section_title(self, x: float, y: float, title: str, subtitle: str | None = None) -> float:
        self.text_at(x, y, title, 22, self.text, 800)
        y -= 12
        if subtitle:
            self.text_at(x, y, subtitle, 9.5, self.muted)
            y -= 10
        self.c.setStrokeColor(self.accent)
        self.c.setLineWidth(1.2)
        self.c.line(x, y, x + 44 * mm, y)
        return y - 12

    def rounded_rect(self, x: float, y: float, w: float, h: float, fill, stroke=None, radius: float = 4 * mm):
        self.c.setFillColor(fill)
        self.c.setStrokeColor(stroke or fill)
        self.c.roundRect(x, y, w, h, radius, stroke=1 if stroke else 0, fill=1)

    def chip(self, x: float, y: float, value: str, fill=None, color=None) -> float:
        size = 8.2
        pad_x = 4.2 * mm
        w = self.text_width(value, size) + pad_x * 2
        self.rounded_rect(x, y - 5, w, 8 * mm, fill or colors.HexColor("#2B281F"), None, 3 * mm)
        self.text_at(x + pad_x, y + 1.2, value, size, color or self.accent, 650)
        return x + w + 4

    def bullet(self, x: float, y: float, value: str, width: float, size: float = 8.4, leading: float = 11.5) -> float:
        self.text_at(x, y, "•", size, self.accent)
        return self.paragraph(x + 5 * mm, y, value, width - 5 * mm, size, leading, self.body) - 1

    def capability_card(self, x: float, y: float, w: float, h: float, title: str, body: str, accent) -> None:
        self.rounded_rect(x, y - h, w, h, colors.HexColor("#202124"), colors.HexColor("#3A362D"), 4 * mm)
        self.c.setFillColor(accent)
        self.c.circle(x + 8 * mm, y - 8 * mm, 3 * mm, stroke=0, fill=1)
        self.text_at(x + 15 * mm, y - 9.5 * mm, title, 11, self.text, 750)
        self.paragraph(x + 7 * mm, y - 18 * mm, body, w - 14 * mm, 8.0, 10.0, self.body)

    def simple_diagram(self, x: float, y: float, w: float, h: float, project: Project, accent) -> None:
        self.rounded_rect(x, y - h, w, h, colors.HexColor("#1B1C1F"), colors.HexColor("#34302A"), 5 * mm)
        box_w = (w - 30 * mm) / 3
        box_h = 21 * mm
        y_box = y - h / 2 + box_h / 2
        labels = self.diagram_labels(project)
        xs = [x + 7 * mm, x + 15 * mm + box_w, x + 23 * mm + box_w * 2]
        for i, label_value in enumerate(labels):
            self.rounded_rect(xs[i], y_box - box_h, box_w, box_h, colors.HexColor("#22252A"), accent, 3 * mm)
            parts = label_value.split("\n")
            self.text_at(xs[i] + 5 * mm, y_box - 8 * mm, parts[0], 8.2, self.accent, 700)
            if len(parts) > 1:
                self.text_at(xs[i] + 5 * mm, y_box - 15 * mm, parts[1], 7.6, self.body)
        self.c.setStrokeColor(accent)
        self.c.setLineWidth(2)
        self.c.line(xs[0] + box_w, y_box - box_h / 2, xs[1], y_box - box_h / 2)
        self.c.line(xs[1] + box_w, y_box - box_h / 2, xs[2], y_box - box_h / 2)

    def diagram_labels(self, project: Project) -> Sequence[str]:
        title = project.title
        if "AX Agent" in title:
            return ["AX Apps\nDeploy", "EKS\nPlatform", "Domain/Auth\nLLM Gateway"]
        if "생성형 AI" in title or "Generative AI" in title:
            return ["Azure\nGlobal AI", "K8s\nServing", "Users\nB2C Traffic"]
        if "챗봇" in title or "Chatbot" in title:
            return ["30K\nEmployees", "Enterprise\nAI Platform", "Policy\nAuth/Data"]
        if "인프라 운영" in title or "AI Services" in title:
            return ["Keycloak\nOAuth", "AI Apps\nSRE", "Langfuse\nTraces"]
        if "클러스터" in title or "Cluster" in title:
            return ["Input\nOne click", "IaC\nProvision", "Dev/Stage\nProd"]
        if "평가" in title or "Evaluation" in title:
            return ["Dataset\nMT tasks", "Evaluate\nLLM", "MLflow\nMetrics"]
        if "GitOps" in title:
            return ["Git\nSource", "ArgoCD\nSync", "K8s\nDeploy"]
        if "모니터링" in title or "Monitoring" in title:
            return ["Metrics\nRuntime", "Grafana\nDashboard", "Alerts\nIncident"]
        if "패킷" in title or "Packet" in title:
            return ["NIC\nPackets", "Mirror\n130K pps", "Target\nServer"]
        if "CNN" in title:
            return ["CNN\nLayers", "GPU\nPlacement", "Training\nSpeedup"]
        return ["OS\nRuntime", "AI\nAssistant", "User\nInteraction"]

    def capability_point(self, project: Project) -> str:
        title = project.title
        if self.lang == "en":
            if "AX Agent" in title:
                return "Experience building a governed self-service agent platform with runtime compatibility, access control, and enterprise LLM integration."
            if "Generative AI" in title:
                return "Experience delivering UK rollout readiness, production stabilization, and incident response for a consumer generative AI service."
            if "Chatbot" in title:
                return "Experience leading application delivery and reliability for tens of thousands of internal users."
            if "AI Services" in title:
                return "Experience connecting LLM application operations with authentication, observability, and runtime reliability."
            if "Cluster" in title:
                return "Experience standardizing infrastructure and automating repeatable development and test environments."
            if "Evaluation" in title:
                return "Experience automating model quality comparison and making evaluation results traceable and repeatable."
            if "GitOps" in title:
                return "Experience connecting deployment consistency, security checks, and operations automation for containerized services."
            if "Monitoring" in title:
                return "Experience using metrics, logs, and traces for incident detection and runtime analysis."
            if "Packet" in title:
                return "Experience optimizing Linux runtime behavior and high-throughput data movement under resource constraints."
            if "CNN" in title:
                return "Research experience on network bottlenecks, resource placement, and performance improvement for distributed training workloads."
            return "Experience integrating AI functionality with OS-level behavior, asynchronous processing, and user interaction."

        if "AX Agent" in title:
            return "런타임 호환성, 셀프서비스 배포, 접근 제어, 사내 LLM 연동을 하나의 거버넌스 플랫폼으로 구현한 경험입니다."
        if "생성형 AI" in title:
            return "소비자 대상 생성형 AI 서비스의 UK 출시 준비, 초기 안정화, 장애 대응을 수행한 경험입니다."
        if "챗봇" in title:
            return "수만 명 규모의 내부 사용자를 위한 애플리케이션 전달과 신뢰성을 리딩한 경험입니다."
        if "인프라 운영" in title:
            return "LLM 애플리케이션 운영을 인증, 관측 가능성, 런타임 안정성과 연결한 경험입니다."
        if "클러스터" in title:
            return "반복 가능한 개발/테스트 환경을 만들기 위한 플랫폼 자동화와 인프라 표준화 경험입니다."
        if "평가" in title:
            return "모델 품질 비교를 자동화하고 평가 결과를 추적 가능하고 반복 가능한 흐름으로 만든 경험입니다."
        if "GitOps" in title:
            return "컨테이너 기반 서비스의 배포 일관성, 보안 검증, 운영 자동화를 연결한 경험입니다."
        if "모니터링" in title:
            return "시스템 메트릭, 로그, 트레이스를 모아 장애 탐지와 런타임 분석에 활용한 경험입니다."
        if "패킷" in title:
            return "Linux 런타임, 고성능 데이터 이동, 제한된 리소스에서의 성능 최적화를 다룬 경험입니다."
        if "CNN" in title:
            return "분산 학습 워크로드의 네트워크 병목, 리소스 배치, 성능 개선을 연구한 경험입니다."
        return "AI 기능을 OS 수준 동작, 비동기 처리, 사용자 상호작용과 연결해 구현한 경험입니다."

    def project_card(self, x: float, y: float, w: float, h: float, project: Project, index: int, accent) -> None:
        self.rounded_rect(x, y - h, w, h, self.panel, colors.HexColor("#39352E"), 5 * mm)
        self.simple_diagram(x + 6 * mm, y - 8 * mm, w - 12 * mm, 37 * mm, project, accent)
        top = y - 53 * mm
        self.text_at(x + 6 * mm, top, f"{index:02d}. {project.title}", 14, self.text, 800)
        top -= 10
        top = self.paragraph(x + 6 * mm, top, project.description, w - 12 * mm, 8.3, 10.8, self.muted)
        top -= 4
        fields = (
            [
                ("문제", project.problem),
                ("역할", project.role),
                ("설계/전달", project.engineering),
                ("결과", project.outcome),
                ("역량 포인트", self.capability_point(project)),
            ]
            if self.lang == "ko"
            else [
                ("Problem", project.problem),
                ("Role", project.role),
                ("Engineering/Delivery", project.engineering),
                ("Outcome", project.outcome),
                ("Capability", self.capability_point(project)),
            ]
        )
        for label_text, value in fields:
            self.text_at(x + 6 * mm, top, label_text, 8.3, self.accent, 750)
            top = self.paragraph(x + 24 * mm, top, value, w - 30 * mm, 7.6, 9.5, self.body)
            top -= 1.5
        chip_x = x + 6 * mm
        chip_y = y - h + 10 * mm
        for tech in project.technologies[:5]:
            if chip_x + self.text_width(tech, 7.4) + 12 * mm > x + w - 5 * mm:
                break
            chip_x = self.chip(chip_x, chip_y, tech, colors.HexColor("#2A261E"), self.accent)


def load_data(lang: str):
    with open(CONFIGS[lang], encoding="utf-8") as f:
        data = json.load(f)
    projects = [
        Project(
            title=p["title"],
            description=p["description"],
            problem=p.get("problem", ""),
            role=p.get("role", ""),
            engineering=p.get("engineering", ""),
            outcome=p.get("outcome", ""),
            relevance=p.get("relevance", ""),
            technologies=p.get("technologies", []),
        )
        for p in data["projects"]
    ]
    return data, projects


def build_pdf(lang: str) -> None:
    data, projects = load_data(lang)
    pdf = PortfolioPDF(OUTPUTS[lang], lang)
    is_ko = lang == "ko"

    # Cover
    pdf.page_bg()
    x = pdf.left
    y = pdf.h - 35 * mm
    pdf.text_at(x, y, data["personal"]["name"], 34, pdf.text, 850)
    y -= 18
    pdf.text_at(x, y, "Application Software · AI Platform · End-to-End Delivery", 11.5, pdf.body)
    y -= 20
    pdf.rounded_rect(x, y - 31 * mm, 142 * mm, 31 * mm, colors.HexColor("#202124"), colors.HexColor("#3A362D"), 5 * mm)
    pdf.text_at(x + 7 * mm, y - 10 * mm, "웹사이트" if is_ko else "Website", 9.5, pdf.accent, 750)
    pdf.text_at(x + 7 * mm, y - 22 * mm, PORTFOLIO_URL, 16, pdf.text, 800)
    pdf.c.linkURL(PORTFOLIO_URL, (x + 7 * mm, y - 24 * mm, x + 72 * mm, y - 14 * mm), relative=0)
    y -= 46 * mm
    summary = (
        "이 포트폴리오는 엔터프라이즈 및 사용자 대상 애플리케이션을 요구사항과 아키텍처부터 구현, 출시, 프로덕션 안정화까지 전달한 경험을 정리한 문서입니다. 각 프로젝트는 문제 상황, 담당 역할, 설계와 전달 포인트, 결과를 중심으로 구성했습니다."
        if is_ko
        else "This portfolio summarizes end-to-end delivery of enterprise and user-facing applications from requirements and architecture through implementation, rollout, and production stabilization. Each project is organized around the problem context, my role, engineering and delivery focus, outcomes, and capability signals."
    )
    pdf.paragraph(x, y, summary, 170 * mm, 11, 16, pdf.body)
    card_y = 65 * mm
    card_w = 57 * mm
    gap = 8 * mm
    cards = (
        [
            ("Application Software", "엔터프라이즈·사용자 대상 앱, 비동기 아키텍처, API 및 시스템 통합", pdf.blue),
            ("End-to-End Delivery", "요구사항, 아키텍처, 구현, 출시 준비, 프로덕션 안정화", pdf.green),
            ("Reliability", "인증·인가, 관측 가능성, 장애 대응, 시스템 성능", pdf.purple),
            ("Cloud Platform", "Azure/AWS/OpenShift, Kubernetes, GitOps, IaC 기반 자동화", pdf.accent),
        ]
        if is_ko
        else [
            ("Application Software", "Enterprise and user-facing apps, asynchronous architecture, API and system integration", pdf.blue),
            ("End-to-End Delivery", "Requirements, architecture, implementation, rollout readiness, and production stabilization", pdf.green),
            ("Reliability", "Authentication, authorization, observability, incident response, and system performance", pdf.purple),
            ("Cloud Platform", "Automation with Azure, AWS, OpenShift, Kubernetes, GitOps, and Infrastructure as Code", pdf.accent),
        ]
    )
    for i, (title, body, accent) in enumerate(cards):
        pdf.capability_card(x + i * (card_w + gap), card_y, card_w, 30 * mm, title, body, accent)

    # Project pages, two cards per page
    accents = [pdf.blue, pdf.green, pdf.blue, pdf.green, pdf.purple, pdf.accent, pdf.blue, pdf.green, pdf.purple, pdf.green]
    selected = projects[:10]
    for page_index in range(0, len(selected), 2):
        pdf.new_page(f"{1 + page_index // 2:02d} / {'프로젝트 사례' if is_ko else 'Project Cases'}")
        y = pdf.section_title(
            pdf.left,
            pdf.h - 31 * mm,
            "프로젝트 상세" if is_ko else "Project Details",
            "문제 상황, 역할, 설계/전달 포인트, 결과, 역량 포인트" if is_ko else "Problem, role, engineering/delivery focus, outcome, and capability point",
        )
        card_w = (pdf.usable - 8 * mm) / 2
        card_h = 145 * mm
        pdf.project_card(pdf.left, y, card_w, card_h, selected[page_index], page_index + 1, accents[page_index])
        if page_index + 1 < len(selected):
            pdf.project_card(pdf.left + card_w + 8 * mm, y, card_w, card_h, selected[page_index + 1], page_index + 2, accents[page_index + 1])

    # Closing
    pdf.new_page(f"06 / {'추가 정보' if is_ko else 'Additional Info'}")
    y = pdf.section_title(
        pdf.left,
        pdf.h - 31 * mm,
        "요약 및 확인 링크" if is_ko else "Links and References",
        "상세 프로젝트와 최신 CV는 온라인 포트폴리오에서 확인할 수 있습니다." if is_ko else "Detailed projects and the latest CV are available on the online portfolio.",
    )
    closing = [
        ("웹사이트" if is_ko else "Website", PORTFOLIO_URL),
        ("GitHub", data["social"]["github"]),
        ("LinkedIn", data["social"]["linkedin"]),
        ("Email", data["personal"]["email"]),
    ]
    box_w = 112 * mm
    for i, (label_text, value) in enumerate(closing):
        bx = pdf.left + (i % 2) * (box_w + 12 * mm)
        by = y - (i // 2) * 33 * mm
        pdf.rounded_rect(bx, by - 24 * mm, box_w, 24 * mm, pdf.panel, colors.HexColor("#3A362D"), 4 * mm)
        pdf.text_at(bx + 6 * mm, by - 9 * mm, label_text, 9, pdf.accent, 750)
        pdf.text_at(bx + 6 * mm, by - 18 * mm, value, 10, pdf.text, 650)
        if value.startswith("http"):
            pdf.c.linkURL(value, (bx + 6 * mm, by - 20 * mm, bx + box_w - 6 * mm, by - 12 * mm), relative=0)
    y -= 78 * mm
    pdf.text_at(pdf.left, y, "논문/발표" if is_ko else "Publications", 16, pdf.text, 800)
    y -= 12
    for pub in data["publications"]:
        line = f"{pub['title']} — {pub['venue']} ({pub['year']})"
        y = pdf.bullet(pdf.left, y, line, pdf.usable, 8.4, 11.5)
    y -= 8
    pdf.paragraph(
        pdf.left,
        y,
        "본 문서는 공개 가능한 경력/프로젝트 내용을 기반으로 정리한 제출용 포트폴리오입니다. 구체적인 내부 구현 세부사항이나 비공개 정보는 포함하지 않았습니다."
        if is_ko
        else "This document is a portfolio summary based on publicly shareable career and project information. It does not include confidential implementation details or non-public information.",
        pdf.usable,
        8.8,
        12.2,
        pdf.muted,
    )
    pdf.save()


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_pdf("ko")
    build_pdf("en")
