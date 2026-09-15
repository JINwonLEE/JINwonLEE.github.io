const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const output = path.join(root, 'tmp', 'portfolio-alignment');
const diagrams = [
  'thumb-ax-agent-platform.svg', 'thumb-observability-stack.svg',
  'thumb-ai-serving-global.svg', 'thumb-enterprise-chatbot.svg',
  'thumb-k8s-automation.svg', 'thumb-gitops-cicd.svg',
  'thumb-llm-cluster-monitoring.svg',
];
let browser;
const measured = [];

before(async () => {
  fs.mkdirSync(output, { recursive: true });
  browser = await chromium.launch({ channel: 'chrome', headless: true });
  for (const filename of diagrams) {
    const page = await browser.newPage({ viewport: { width: 800, height: 500 } });
    await page.goto(`file://${root}/assets/images/${filename}`);
    const labels = await page.evaluate(() => {
      const shapes = [...document.querySelectorAll('rect, path')]
        .map(el => ({ el, box: el.getBBox() }))
        .filter(({ box }) => box.width >= 80 && box.width < 800 && box.height >= 40);
      return [...document.querySelectorAll('text')].flatMap(el => {
        const x = el.x.baseVal[0].value;
        const y = el.y.baseVal[0].value;
        const matches = shapes.filter(({ box }) => x >= box.x && x <= box.x + box.width && y >= box.y && y <= box.y + box.height);
        const shape = matches.sort((a, b) => a.box.width * a.box.height - b.box.width * b.box.height)[0];
        if (!shape) return [];
        const r = shape.box;
        const b = el.getBBox();
        const hasVisual = [...document.querySelectorAll('rect, circle')].some(other => {
          if (other === shape.el) return false;
          const inner = other.getBBox();
          return inner.x >= r.x && inner.y >= r.y && inner.x + inner.width <= r.x + r.width && inner.y + inner.height <= r.y + r.height;
        });
        return [{ text: el.textContent, x: b.x, y: b.y, width: b.width, height: b.height,
          rect: { x: r.x, y: r.y, width: r.width, height: r.height }, hasVisual,
          anchor: getComputedStyle(el).textAnchor, baseline: getComputedStyle(el).dominantBaseline }];
      });
    });
    measured.push({ filename, labels });
    await page.screenshot({ path: path.join(output, `${filename}.png`) });
    await page.close();
  }
});

after(async () => { if (browser) await browser.close(); });

test('diagram labels are horizontally centered and stay inside their boxes', () => {
  for (const { filename, labels } of measured) {
    assert.ok(labels.length > 0);
    for (const b of labels) {
      const message = `${filename}: ${b.text}`;
      assert.equal(b.anchor, 'middle', message);
      assert.equal(b.baseline, 'central', message);
      assert.ok(Math.abs(b.x + b.width / 2 - b.rect.x - b.rect.width / 2) < 1, message);
      assert.ok(b.x >= b.rect.x + 6 && b.x + b.width <= b.rect.x + b.rect.width - 6, message);
      assert.ok(b.y >= b.rect.y + 6 && b.y + b.height <= b.rect.y + b.rect.height - 6, message);
    }
  }
});

test('text-only diagram boxes vertically center their label groups', () => {
  for (const { filename, labels } of measured) {
    const groups = Map.groupBy(labels.filter(b => !b.hasVisual), b => JSON.stringify(b.rect));
    for (const group of groups.values()) {
      const top = Math.min(...group.map(b => b.y));
      const bottom = Math.max(...group.map(b => b.y + b.height));
      const r = group[0].rect;
      assert.ok(Math.abs((top + bottom) / 2 - r.y - r.height / 2) < 3, `${filename}: ${group.map(b => b.text).join(', ')}`);
    }
  }
});

for (const [name, width] of [['desktop', 1440], ['mobile', 390], ['small mobile', 320]]) {
  test(`${name}: bilingual page title, images, and text fit`, async () => {
    for (const filename of ['index.html', 'index-ko.html']) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      try {
        await page.goto(`file://${root}/${filename}`, { waitUntil: 'load' });
        await page.evaluate(async () => {
          document.querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
          await document.fonts.ready;
          await Promise.all([...document.images].map(img => img.decode()));
        });
        assert.equal(await page.locator('.professional-title').innerText(), 'AI Platform & Reliability Engineer');
        assert.match(await page.title(), /AI Platform & Reliability Engineer/);
        const overflow = await page.evaluate(() => ({
          page: document.documentElement.scrollWidth > window.innerWidth,
          text: [...document.querySelectorAll('h1, h2, h3, p, .site-brand')].filter(el => {
            const clipsVertically = ['hidden', 'clip'].includes(getComputedStyle(el).overflowY);
            return el.clientWidth > 0 && (el.scrollWidth > el.clientWidth + 1 || (clipsVertically && el.scrollHeight > el.clientHeight + 1));
          }).map(el => el.textContent),
        }));
        assert.deepEqual(overflow, { page: false, text: [] });
        await page.screenshot({ path: path.join(output, `${filename}-${width}-hero.png`) });
        await page.locator('.featured-case').screenshot({ path: path.join(output, `${filename}-${width}-ax.png`) });
        await page.locator('.case-grid').screenshot({ path: path.join(output, `${filename}-${width}-projects.png`) });
      } finally {
        await page.close();
      }
    }
  });
}
