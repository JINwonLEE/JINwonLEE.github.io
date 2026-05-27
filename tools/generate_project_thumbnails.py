from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images"


def text(x: int, y: int, value: str, size: int = 24, color: str = "#f6f4ee", weight: int = 500) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" font-family="Inter, Arial, sans-serif">{escape(value)}</text>'
    )


def label(x: int, y: int, value: str, color: str = "#f2c46d") -> str:
    return text(x, y, value, 18, color, 650)


def rect(x: int, y: int, w: int, h: int, fill: str, stroke: str = "#4a4133", rx: int = 16, opacity: float = 1) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="{opacity}"/>'
    )


def circle(cx: int, cy: int, r: int, fill: str, stroke: str = "#4a4133", opacity: float = 1) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="{opacity}"/>'


def line(x1: int, y1: int, x2: int, y2: int, color: str = "#d9ae59", width: int = 3, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash_attr}/>'


def path(d: str, color: str = "#d9ae59", width: int = 3, fill: str = "none", dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{dash_attr}/>'


def base(title: str, subtitle: str, body: str, accent: str = "#d9ae59") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#151515"/>
      <stop offset="0.55" stop-color="#202022"/>
      <stop offset="1" stop-color="#111114"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>
  <rect width="800" height="500" rx="28" fill="url(#bg)"/>
  <circle cx="680" cy="80" r="150" fill="{accent}" opacity="0.07"/>
  <circle cx="92" cy="430" r="180" fill="#ffffff" opacity="0.035"/>
  {text(44, 70, title, 30, "#fff8ea", 750)}
  {text(44, 104, subtitle, 17, "#b9b2a7", 500)}
  {body}
</svg>
"""


def ai_serving_global() -> str:
    nodes = [
        rect(86, 188, 130, 86, "#23262b", "#5d4b2e", 18),
        label(119, 220, "Azure"),
        text(114, 247, "Global AI", 17, "#d7d2c8"),
        rect(333, 163, 138, 132, "#202a2f", "#4b7180", 22),
        label(361, 205, "K8s"),
        text(360, 233, "Serving", 19, "#e7f8ff", 650),
        text(371, 260, "Pods", 16, "#9fc9d6"),
        rect(586, 188, 128, 86, "#23262b", "#5d4b2e", 18),
        label(611, 220, "Users"),
        text(608, 247, "B2C Traffic", 17, "#d7d2c8"),
        line(216, 231, 333, 231, "#56c1d8", 4),
        line(471, 231, 586, 231, "#56c1d8", 4),
        path("M400 330 C340 330 306 360 306 396 C306 426 330 444 400 444 C470 444 494 426 494 396 C494 360 460 330 400 330Z", "#d9ae59", 3, "#211c14"),
        label(346, 392, "Multi-region"),
        text(344, 420, "readiness", 17, "#d7d2c8"),
    ]
    return base("Global Generative AI Service", "Azure · Kubernetes · Model Serving", "\n  ".join(nodes), "#48c7e8")


def enterprise_chatbot() -> str:
    items = [
        rect(74, 177, 135, 180, "#222226", "#514634", 20),
        label(105, 217, "30K"),
        text(101, 248, "Employees", 18, "#d7d2c8"),
        circle(121, 296, 18, "#d9ae59", "#d9ae59"),
        circle(162, 296, 18, "#65d6a4", "#65d6a4"),
        circle(141, 329, 18, "#72b7ff", "#72b7ff"),
        rect(315, 142, 178, 206, "#1f2929", "#51886e", 22),
        label(350, 190, "Enterprise"),
        text(349, 224, "AI Chatbot", 24, "#f6f4ee", 750),
        rect(350, 260, 108, 40, "#263a34", "#65d6a4", 12),
        text(374, 286, "LLM", 19, "#dff7ec", 700),
        rect(584, 177, 136, 180, "#222226", "#514634", 20),
        label(615, 217, "Policy"),
        text(616, 248, "Auth", 18, "#d7d2c8"),
        text(616, 279, "Data", 18, "#d7d2c8"),
        text(616, 310, "Guard", 18, "#d7d2c8"),
        line(209, 262, 315, 245, "#65d6a4", 4),
        line(493, 245, 584, 262, "#65d6a4", 4),
    ]
    return base("Company-wide AI Chatbot", "Kubernetes operations · Enterprise AI", "\n  ".join(items), "#65d6a4")


def ai_observability() -> str:
    items = [
        rect(68, 154, 152, 88, "#222226", "#5d4b2e", 18),
        label(100, 190, "Keycloak"),
        text(103, 217, "OAuth", 17, "#d7d2c8"),
        rect(323, 141, 154, 116, "#20272d", "#4c7893", 20),
        label(356, 181, "AI Apps"),
        text(357, 212, "Document LLM", 17, "#d7d2c8"),
        rect(582, 154, 152, 88, "#222226", "#5d4b2e", 18),
        label(615, 190, "Langfuse"),
        text(612, 217, "Traces", 17, "#d7d2c8"),
        rect(244, 340, 312, 68, "#1e2528", "#5d6770", 16),
        label(328, 381, "Observable Runtime"),
        line(220, 199, 323, 199, "#72b7ff", 4),
        line(477, 199, 582, 199, "#72b7ff", 4),
        line(400, 257, 400, 340, "#72b7ff", 4),
        circle(400, 199, 42, "#20272d", "#72b7ff"),
        text(381, 207, "SRE", 22, "#e7f8ff", 750),
    ]
    return base("Enterprise AI Services", "Authentication · AI observability · SRE", "\n  ".join(items), "#72b7ff")


def k8s_automation() -> str:
    items = [
        rect(76, 182, 150, 110, "#222226", "#5d4b2e", 20),
        label(113, 222, "Input"),
        text(111, 252, "One click", 19, "#f6f4ee", 700),
        rect(324, 145, 154, 184, "#202a26", "#58805a", 24),
        label(355, 190, "Provision"),
        text(356, 225, "Terraform", 18, "#d7d2c8"),
        text(356, 256, "Ansible", 18, "#d7d2c8"),
        text(356, 287, "Python", 18, "#d7d2c8"),
        rect(572, 132, 120, 72, "#222226", "#4f795f", 16),
        rect(572, 228, 120, 72, "#222226", "#4f795f", 16),
        rect(572, 324, 120, 72, "#222226", "#4f795f", 16),
        label(599, 174, "Dev"),
        label(592, 270, "Stage"),
        label(596, 366, "Prod"),
        line(226, 237, 324, 237, "#65d6a4", 4),
        line(478, 213, 572, 168, "#65d6a4", 4),
        line(478, 237, 572, 264, "#65d6a4", 4),
        line(478, 263, 572, 360, "#65d6a4", 4),
    ]
    return base("Kubernetes Cluster Automation", "Repeatable environments · IaC", "\n  ".join(items), "#65d6a4")


def llm_evaluation() -> str:
    items = [
        rect(74, 162, 132, 176, "#222226", "#5d4b2e", 20),
        label(107, 208, "Dataset"),
        text(108, 240, "MT tasks", 18, "#d7d2c8"),
        line(108, 274, 172, 274, "#d9ae59", 4),
        line(108, 300, 156, 300, "#d9ae59", 4),
        rect(319, 143, 162, 214, "#25232b", "#66538d", 24),
        label(359, 190, "Evaluate"),
        text(354, 226, "LLM A", 18, "#d7d2c8"),
        text(354, 256, "LLM B", 18, "#d7d2c8"),
        text(354, 286, "LLM C", 18, "#d7d2c8"),
        rect(594, 162, 130, 176, "#222226", "#5d4b2e", 20),
        label(622, 208, "MLflow"),
        text(619, 240, "Metrics", 18, "#d7d2c8"),
        path("M626 294 L655 262 L683 284 L707 238", "#b69cff", 5),
        line(206, 250, 319, 250, "#b69cff", 4),
        line(481, 250, 594, 250, "#b69cff", 4),
    ]
    return base("LLM Evaluation Pipeline", "Quality metrics · MLflow · MLOps", "\n  ".join(items), "#b69cff")


def gitops_cicd() -> str:
    items = [
        rect(64, 172, 126, 100, "#222226", "#5d4b2e", 18),
        label(97, 213, "Git"),
        text(92, 243, "Source", 17, "#d7d2c8"),
        rect(250, 172, 126, 100, "#20262a", "#4c7893", 18),
        label(280, 213, "Scan"),
        text(278, 243, "DevSecOps", 17, "#d7d2c8"),
        rect(436, 172, 126, 100, "#25232b", "#66538d", 18),
        label(465, 213, "ArgoCD"),
        text(466, 243, "GitOps", 17, "#d7d2c8"),
        rect(622, 172, 126, 100, "#202a26", "#58805a", 18),
        label(647, 213, "K8s"),
        text(646, 243, "Deploy", 17, "#d7d2c8"),
        line(190, 222, 250, 222, "#d9ae59", 4),
        line(376, 222, 436, 222, "#d9ae59", 4),
        line(562, 222, 622, 222, "#d9ae59", 4),
        rect(260, 338, 280, 50, "#211c14", "#d9ae59", 14),
        label(321, 371, "Repeatable release flow"),
    ]
    return base("GitOps CI/CD Pipeline", "ArgoCD · Python automation · security checks", "\n  ".join(items), "#d9ae59")


def observability_stack() -> str:
    bars = [
        rect(118, 312, 34, 74, "#d9ae59", "#d9ae59", 8),
        rect(174, 270, 34, 116, "#72b7ff", "#72b7ff", 8),
        rect(230, 222, 34, 164, "#65d6a4", "#65d6a4", 8),
        rect(286, 296, 34, 90, "#b69cff", "#b69cff", 8),
    ]
    items = [
        rect(78, 150, 280, 270, "#202226", "#534633", 24),
        *bars,
        label(130, 195, "Metrics"),
        rect(452, 156, 248, 62, "#222226", "#4c7893", 16),
        rect(452, 246, 248, 62, "#222226", "#4f795f", 16),
        rect(452, 336, 248, 62, "#222226", "#66538d", 16),
        label(489, 194, "Prometheus"),
        label(502, 284, "Grafana"),
        label(520, 374, "Loki / OTel"),
        line(358, 286, 452, 187, "#d9ae59", 3, "8 8"),
        line(358, 286, 452, 277, "#d9ae59", 3, "8 8"),
        line(358, 286, 452, 367, "#d9ae59", 3, "8 8"),
    ]
    return base("Monitoring & Observability", "System metrics · runtime traces · alerts", "\n  ".join(items), "#72b7ff")


def packet_mirroring() -> str:
    items = [
        rect(64, 192, 132, 94, "#222226", "#5d4b2e", 18),
        label(103, 232, "NIC"),
        text(94, 260, "Packets", 17, "#d7d2c8"),
        rect(312, 154, 176, 170, "#20272d", "#4c7893", 22),
        label(352, 207, "Mirror"),
        text(347, 241, "Filter", 20, "#f6f4ee", 750),
        text(344, 276, "130K pps", 20, "#72b7ff", 750),
        rect(604, 192, 132, 94, "#222226", "#5d4b2e", 18),
        label(632, 232, "Target"),
        text(632, 260, "Server", 17, "#d7d2c8"),
        path("M196 238 C244 202 267 276 312 238", "#65d6a4", 5),
        path("M488 238 C536 202 559 276 604 238", "#65d6a4", 5),
        line(270, 374, 530, 374, "#d9ae59", 3),
        text(288, 406, "resource-aware datapath", 18, "#d7d2c8"),
    ]
    return base("High-throughput Packet Mirroring", "Linux runtime · constrained resources", "\n  ".join(items), "#65d6a4")


def distributed_cnn() -> str:
    items = [
        rect(70, 154, 145, 220, "#222226", "#5d4b2e", 20),
        label(110, 198, "CNN"),
        text(103, 230, "Layers", 18, "#d7d2c8"),
        line(112, 270, 176, 270, "#d9ae59", 5),
        line(112, 300, 168, 300, "#d9ae59", 5),
        line(112, 330, 184, 330, "#d9ae59", 5),
        rect(332, 136, 132, 92, "#20272d", "#4c7893", 18),
        rect(332, 272, 132, 92, "#20272d", "#4c7893", 18),
        rect(584, 204, 132, 92, "#20272d", "#4c7893", 18),
        label(367, 175, "GPU 1"),
        label(367, 311, "GPU 2"),
        label(619, 243, "GPU 3"),
        path("M215 254 C272 176 292 176 332 182", "#b69cff", 4),
        path("M215 292 C282 318 292 318 332 318", "#b69cff", 4),
        path("M464 182 C528 166 540 250 584 250", "#b69cff", 4),
        path("M464 318 C528 336 540 250 584 250", "#b69cff", 4),
        text(309, 420, "resource-aware layer placement", 18, "#d7d2c8"),
    ]
    return base("Distributed CNN Training", "Model parallelism · network bottleneck", "\n  ".join(items), "#b69cff")


def ai_assistant_os() -> str:
    items = [
        rect(74, 170, 160, 158, "#222226", "#5d4b2e", 22),
        label(118, 217, "TmaxOS"),
        text(116, 250, "System APIs", 18, "#d7d2c8"),
        rect(326, 132, 148, 236, "#202a26", "#58805a", 28),
        circle(400, 210, 46, "#65d6a4", "#65d6a4"),
        text(377, 218, "AI", 28, "#102019", 850),
        label(362, 298, "Assistant"),
        text(352, 330, "Async runtime", 17, "#d7d2c8"),
        rect(582, 170, 150, 158, "#222226", "#4c7893", 22),
        label(622, 217, "User"),
        text(620, 250, "Voice / UX", 18, "#d7d2c8"),
        line(234, 249, 326, 249, "#65d6a4", 4),
        line(474, 249, 582, 249, "#65d6a4", 4),
        path("M630 380 C650 354 684 354 704 380", "#72b7ff", 4),
    ]
    return base("AI Assistant on TmaxOS", "System integration · inference · async design", "\n  ".join(items), "#65d6a4")


ASSETS = {
    "thumb-ai-serving-global.svg": ai_serving_global,
    "thumb-enterprise-chatbot.svg": enterprise_chatbot,
    "thumb-ai-services-observability.svg": ai_observability,
    "thumb-k8s-automation.svg": k8s_automation,
    "thumb-llm-evaluation.svg": llm_evaluation,
    "thumb-gitops-cicd.svg": gitops_cicd,
    "thumb-observability-stack.svg": observability_stack,
    "thumb-packet-mirroring.svg": packet_mirroring,
    "thumb-distributed-cnn-training.svg": distributed_cnn,
    "thumb-ai-assistant-os.svg": ai_assistant_os,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in ASSETS.items():
        (OUT / filename).write_text(builder(), encoding="utf-8")


if __name__ == "__main__":
    main()
