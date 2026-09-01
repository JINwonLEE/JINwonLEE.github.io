const documents = [
  {
    id: "platform-deployment",
    title: "Application Deployment Handbook",
    department: "Platform Engineering",
    roles: ["engineer", "manager"],
    content: "Deployments start from an approved repository and a signed container image. The platform creates a service domain after the release policy passes. Application owners assign an access group before production traffic is enabled. Rollback uses the previous signed release and must be recorded in the change log."
  },
  {
    id: "incident-response",
    title: "Production Incident Response",
    department: "Site Reliability Engineering",
    roles: ["engineer", "manager"],
    content: "For a severity-one incident, page the on-call engineer, open an incident channel, and assign an incident commander. Stabilize customer impact before investigating root cause. Record the timeline, mitigation, and follow-up actions in the incident review."
  },
  {
    id: "financial-plan",
    title: "Confidential Annual Financial Plan",
    department: "Finance",
    roles: ["manager"],
    content: "The annual planning document contains confidential revenue scenarios, cost envelopes, and investment priorities. It may be viewed only by managers who are members of the finance planning access group."
  },
  {
    id: "vendor-onboarding",
    title: "Vendor Onboarding Guide",
    department: "Operations",
    roles: ["engineer", "manager", "contractor"],
    content: "Vendors must complete identity verification and security training before receiving temporary access. Contractor access expires automatically at the end of the engagement and requires a sponsoring employee for renewal."
  },
  {
    id: "ai-usage-policy",
    title: "Responsible AI Usage Policy",
    department: "AI Governance",
    roles: ["engineer", "manager", "contractor"],
    content: "Do not submit secrets, personal data, or restricted source code to an AI system. Use only approved models and gateways. Human review is required before generated content is used for customer-facing, legal, security, or financial decisions."
  }
];

const suggestions = [
  "How do I deploy an application and enable production traffic?",
  "What should I do first during a severity-one incident?",
  "What must a contractor complete before temporary access?",
  "Can I submit secrets to an AI system and use the answer for a legal decision?",
  "What are the confidential annual revenue and investment scenarios?"
];

const auditEvents = [];
let activeRole = "engineer";
let suggestionIndex = 0;
const apiEnabled = window.location.port === "8088";
const stopWords = new Set(["and", "are", "before", "can", "could", "for", "from", "how", "into", "show", "that", "the", "this", "what", "when", "where", "which", "with", "would"]);

function tokenize(value) {
  return (value.toLowerCase().match(/[a-z0-9-]{2,}/g) || []).filter((term) => !stopWords.has(term));
}

function retrieve(query) {
  const queryTerms = new Set(tokenize(query));
  const ranked = documents
    .map((document) => {
      const terms = tokenize(`${document.title} ${document.content}`);
      const score = terms.reduce((total, term) => total + (queryTerms.has(term) ? 1 : 0), 0);
      return { document, score };
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score);
  const bestScore = ranked[0]?.score || 0;
  return ranked.filter((entry) => entry.score >= Math.max(3, bestScore * 0.6));
}

function answerQuestion(query, role) {
  const started = performance.now();
  const candidates = retrieve(query);
  const authorized = candidates.filter(({ document }) => document.roles.includes(role)).slice(0, 3);
  const denied = candidates.length - authorized.length;
  const elapsed = Math.max(1, Math.round(performance.now() - started) + 7);

  if (!authorized.length) {
    return {
      text: "I could not find authorized source material that answers this question.",
      sources: [],
      decision: "NO AUTHORIZED CONTEXT",
      denied,
      latency: elapsed
    };
  }

  const statements = authorized.map(({ document }) => {
    const excerpt = document.content.split(". ").slice(0, 3).map((sentence) => sentence.replace(/\.$/, "")).join(". ");
    return `${excerpt} [${document.id}].`;
  });
  return {
    text: `Based on the authorized sources: ${statements.join(" ")}`,
    sources: authorized.map(({ document }) => document),
    decision: "ALLOWED",
    denied,
    latency: elapsed
  };
}

async function requestAnswer(query, role) {
  if (!apiEnabled) return answerQuestion(query, role);
  const response = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, role })
  });
  if (!response.ok) throw new Error(`Assistant API returned ${response.status}`);
  const data = await response.json();
  return {
    text: data.answer,
    sources: data.citations.map((citation) => ({
      id: citation.document_id,
      title: citation.title,
      department: citation.department,
      content: citation.excerpt
    })),
    decision: data.access_decision.replaceAll("-", " ").toUpperCase(),
    denied: data.denied_candidate_count,
    latency: data.latency_ms,
    provider: data.provider,
    model: data.model
  };
}

function renderSources(sources) {
  const container = document.querySelector("#sources");
  if (!sources.length) {
    container.innerHTML = `<div class="empty-state"><i data-lucide="shield-x"></i><p>No authorized source entered the generation context.</p></div>`;
  } else {
    container.innerHTML = sources.map((source, index) => `
      <article class="source-item">
        <span class="source-number">SOURCE ${String(index + 1).padStart(2, "0")}</span>
        <h3>${source.title}</h3>
        <small>${source.department} · ${source.id}</small>
        <p>${source.content}</p>
      </article>
    `).join("");
  }
  if (window.lucide) window.lucide.createIcons();
}

function renderAudit() {
  const table = document.querySelector("#audit-table");
  if (!auditEvents.length) {
    table.innerHTML = `<tr><td colspan="6" class="table-empty">Ask a question to create an audit event.</td></tr>`;
    return;
  }
  table.innerHTML = auditEvents.map((event) => `
    <tr>
      <td>${event.time}</td>
      <td>${event.role}</td>
      <td>${event.query}</td>
      <td><span class="decision ${event.allowed ? "pass" : "fail"}">${event.decision}</span></td>
      <td>${event.sources}</td>
      <td>${event.latency} ms</td>
    </tr>
  `).join("");
}

function setView(name) {
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("is-active", tab.dataset.view === name));
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("is-active"));
  document.querySelector(`#${name}-view`).classList.add("is-active");
}

async function submitQuestion(event) {
  event.preventDefault();
  const query = document.querySelector("#query").value.trim();
  if (query.length < 3) return;
  const result = await requestAnswer(query, activeRole);

  document.querySelector("#user-role-label").textContent = activeRole[0].toUpperCase() + activeRole.slice(1);
  document.querySelector("#user-query").textContent = query;
  document.querySelector("#user-message").classList.remove("is-hidden");
  document.querySelector("#answer-text").textContent = result.text;
  document.querySelector("#answer-decision").textContent = result.decision;
  document.querySelector("#answer-message").classList.remove("is-hidden");
  document.querySelector("#runtime-metadata").textContent = `${result.provider || "offline"} / ${result.model || "extractive-v1"} · ${result.latency} ms · ${result.sources.length} source(s) · ${result.denied} candidate(s) withheld`;
  const policyState = document.querySelector("#policy-state");
  policyState.textContent = result.decision;
  policyState.className = `policy-state ${result.sources.length ? "allowed" : "denied"}`;
  renderSources(result.sources);

  auditEvents.unshift({
    time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
    role: activeRole,
    query,
    decision: result.decision,
    allowed: Boolean(result.sources.length),
    sources: result.sources.length,
    latency: result.latency
  });
  renderAudit();
}

async function runEvaluations() {
  const cases = [
    { name: "deployment-guidance", role: "engineer", query: suggestions[0], expected: "platform-deployment", forbidden: null },
    { name: "contractor-onboarding", role: "contractor", query: suggestions[2], expected: "vendor-onboarding", forbidden: "financial-plan" },
    { name: "financial-access-denied", role: "contractor", query: suggestions[4], expected: null, forbidden: "financial-plan" },
    { name: "responsible-ai", role: "manager", query: suggestions[3], expected: "ai-usage-policy", forbidden: null }
  ];
  let results;
  let summary;
  if (apiEnabled) {
    const response = await fetch("/api/evaluations/run", { method: "POST" });
    if (!response.ok) throw new Error(`Evaluation API returned ${response.status}`);
    const payload = await response.json();
    summary = payload.summary;
    results = payload.cases.map((result) => ({
      name: result.name,
      role: result.role,
      retrieval: result.retrieval_pass,
      access: result.access_pass,
      grounding: result.grounding_pass,
      latency: result.latency_ms
    }));
  } else {
    results = cases.map((testCase) => {
      const result = answerQuestion(testCase.query, testCase.role);
      const ids = result.sources.map((source) => source.id);
      return {
        ...testCase,
        retrieval: !testCase.expected || ids.includes(testCase.expected),
        access: !testCase.forbidden || !ids.includes(testCase.forbidden),
        grounding: result.text.includes("[") || !result.sources.length,
        latency: result.latency
      };
    });
    const rate = (field) => results.filter((result) => result[field]).length / results.length;
    const sortedLatency = results.map((result) => result.latency).sort((a, b) => a - b);
    summary = {
      retrieval_hit_rate: rate("retrieval"),
      access_safety_rate: rate("access"),
      grounding_check_rate: rate("grounding"),
      median_latency_ms: sortedLatency[2]
    };
  }
  document.querySelector("#retrieval-metric").textContent = `${Math.round(summary.retrieval_hit_rate * 100)}%`;
  document.querySelector("#access-metric").textContent = `${Math.round(summary.access_safety_rate * 100)}%`;
  document.querySelector("#grounding-metric").textContent = `${Math.round(summary.grounding_check_rate * 100)}%`;
  document.querySelector("#latency-metric").textContent = `${summary.median_latency_ms} ms`;
  document.querySelector("#eval-table").innerHTML = results.map((result) => `
    <tr>
      <td>${result.name}</td><td>${result.role}</td>
      <td class="${result.retrieval ? "pass" : "fail"}">${result.retrieval ? "PASS" : "FAIL"}</td>
      <td class="${result.access ? "pass" : "fail"}">${result.access ? "PASS" : "FAIL"}</td>
      <td class="${result.grounding ? "pass" : "fail"}">${result.grounding ? "PASS" : "FAIL"}</td>
      <td>${result.latency} ms</td>
    </tr>
  `).join("");
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();
  if (apiEnabled) document.querySelector(".runtime-status").lastChild.textContent = " API demo";
  document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => setView(tab.dataset.view)));
  document.querySelectorAll(".segment").forEach((button) => button.addEventListener("click", () => {
    activeRole = button.dataset.role;
    document.querySelectorAll(".segment").forEach((segment) => segment.classList.toggle("is-active", segment === button));
  }));
  document.querySelector("#assistant-form").addEventListener("submit", submitQuestion);
  document.querySelector("#suggestion-button").addEventListener("click", () => {
    suggestionIndex = (suggestionIndex + 1) % suggestions.length;
    document.querySelector("#query").value = suggestions[suggestionIndex];
  });
  document.querySelector("#run-evals").addEventListener("click", runEvaluations);
  document.querySelector("#clear-audit").addEventListener("click", () => {
    auditEvents.length = 0;
    renderAudit();
  });
  if (new URLSearchParams(window.location.search).get("demo") === "answered") {
    window.setTimeout(() => document.querySelector("#assistant-form").requestSubmit(), 120);
  }
});
