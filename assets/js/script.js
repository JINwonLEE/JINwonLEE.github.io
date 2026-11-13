(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  // Name: reveal one character at a time.
  const name = document.querySelector(".name");
  if (name && !reduceMotion) {
    const text = name.textContent.trim();
    name.setAttribute("aria-label", text);
    name.textContent = "";
    [...text].forEach((char, index) => {
      const span = document.createElement("span");
      span.className = "ch";
      span.setAttribute("aria-hidden", "true");
      span.style.setProperty("--i", index);
      span.textContent = char === " " ? " " : char;
      name.appendChild(span);
    });
  }

  // Sections fade in as they enter the viewport.
  const revealed = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    revealed.forEach((element) => revealObserver.observe(element));
  } else {
    revealed.forEach((element) => element.classList.add("is-in"));
  }

  // Sidebar navigation follows the section in view.
  const navLinks = [...document.querySelectorAll(".rail-nav a")];
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);
  const setActive = () => {
    const marker = window.innerHeight * 0.35;
    let current = sections[0];
    sections.forEach((section) => {
      if (section.getBoundingClientRect().top <= marker) current = section;
    });
    const atBottom = window.innerHeight + window.scrollY >= document.body.scrollHeight - 4;
    if (atBottom) current = sections[sections.length - 1];
    navLinks.forEach((link) => {
      link.classList.toggle("is-active", current && link.getAttribute("href") === `#${current.id}`);
    });
  };
  if (sections.length) {
    setActive();
    window.addEventListener("scroll", setActive, { passive: true });
    window.addEventListener("resize", setActive);
  }

  if (!finePointer || reduceMotion) return;

  // Spotlight that follows the cursor, and a glow that tracks it inside cards.
  let pointerX = window.innerWidth / 2;
  let pointerY = window.innerHeight / 3;
  let queued = false;
  const cards = [...document.querySelectorAll(".glow")];
  const applyPointer = () => {
    queued = false;
    root.style.setProperty("--x", `${pointerX}px`);
    root.style.setProperty("--y", `${pointerY}px`);
    cards.forEach((card) => {
      const box = card.getBoundingClientRect();
      if (box.bottom < -200 || box.top > window.innerHeight + 200) return;
      card.style.setProperty("--mx", `${pointerX - box.left}px`);
      card.style.setProperty("--my", `${pointerY - box.top}px`);
    });
  };
  window.addEventListener("pointermove", (event) => {
    pointerX = event.clientX;
    pointerY = event.clientY;
    root.classList.add("has-pointer");
    if (!queued) {
      queued = true;
      requestAnimationFrame(applyPointer);
    }
  }, { passive: true });
  window.addEventListener("scroll", () => {
    if (!queued) {
      queued = true;
      requestAnimationFrame(applyPointer);
    }
  }, { passive: true });

  // Drifting points that link up around the cursor.
  const canvas = document.getElementById("field");
  if (!canvas) return;
  const context = canvas.getContext("2d");
  const REACH = 190;
  const LINK = 120;
  let width = 0;
  let height = 0;
  let points = [];
  let frame = 0;

  const resize = () => {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    const count = Math.round(Math.min(110, (width * height) / 14000));
    points = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 1.1 + 0.4,
      vx: (Math.random() - 0.5) * 0.16,
      vy: (Math.random() - 0.5) * 0.16,
      alpha: Math.random() * 0.35 + 0.12,
      phase: Math.random() * Math.PI * 2,
    }));
  };

  const draw = (time) => {
    context.clearRect(0, 0, width, height);
    const near = [];
    points.forEach((point) => {
      point.x += point.vx;
      point.y += point.vy;
      if (point.x < -10) point.x = width + 10;
      if (point.x > width + 10) point.x = -10;
      if (point.y < -10) point.y = height + 10;
      if (point.y > height + 10) point.y = -10;
      const distance = Math.hypot(point.x - pointerX, point.y - pointerY);
      const pull = distance < REACH ? 1 - distance / REACH : 0;
      if (pull > 0) near.push({ point, pull });
      const twinkle = 0.7 + 0.3 * Math.sin(time / 1500 + point.phase);
      context.globalAlpha = Math.min(1, point.alpha * twinkle + pull * 0.6);
      context.fillStyle = pull > 0 ? "#f3b563" : "#cbd5e1";
      context.beginPath();
      context.arc(point.x, point.y, point.radius + pull * 1.1, 0, Math.PI * 2);
      context.fill();
    });
    context.strokeStyle = "#f3b563";
    context.lineWidth = 0.6;
    for (let a = 0; a < near.length; a += 1) {
      for (let b = a + 1; b < near.length; b += 1) {
        const gap = Math.hypot(near[a].point.x - near[b].point.x, near[a].point.y - near[b].point.y);
        if (gap > LINK) continue;
        context.globalAlpha = (1 - gap / LINK) * Math.min(near[a].pull, near[b].pull) * 0.9;
        context.beginPath();
        context.moveTo(near[a].point.x, near[a].point.y);
        context.lineTo(near[b].point.x, near[b].point.y);
        context.stroke();
      }
    }
    context.globalAlpha = 1;
    frame = requestAnimationFrame(draw);
  };

  resize();
  frame = requestAnimationFrame(draw);
  window.addEventListener("resize", resize);
  document.addEventListener("visibilitychange", () => {
    cancelAnimationFrame(frame);
    if (!document.hidden) frame = requestAnimationFrame(draw);
  });
})();
