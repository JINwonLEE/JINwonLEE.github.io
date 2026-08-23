# How to Update Your Portfolio

This guide explains how to update the portfolio content, CV links, and bilingual files for GitHub Pages.

## 📁 Configuration File

Project data is stored in two configuration files:

- **`portfolio-config.json`**: English portfolio data
- **`portfolio-config-ko.json`**: Korean portfolio data

These files make it easy to:
- Add new projects
- Update your information
- Modify skills and experience
- Add publications

Important: the About and Resume sections are still partly hardcoded in **`index.html`** and **`index-ko.html`**. When you change career summaries or experience periods, update both the config files and the HTML files.

## 🚀 Quick Start

### Adding a New Project

1. Open `portfolio-config.json`
2. Find the `"projects"` section
3. Add a new project entry:

```json
{
  "title": "Your Project Name",
  "category": "infrastructure",  // Options: "infrastructure", "ai/ml", "automation"
  "description": "Brief description of what you built",
  "detailedDescription": "Longer project explanation for the modal",
  "problem": "Problem or context",
  "role": "Your role",
  "engineering": "Design and operations focus",
  "outcome": "Result or learning without invented metrics",
  "relevance": "Why this matters for AI/platform/system/data roles",
  "technologies": ["Tech1", "Tech2", "Tech3"],
  "image": "./assets/images/your-image.jpg",
  "detailedImage": "./assets/images/your-image.jpg",
  "url": "https://github.com/yourusername/project",
  "featured": true  // Set to true to show in main portfolio
}
```

### Updating Your CV

1. Replace the PDF files:
   - `CV-Eng.pdf`
   - `CV-Kor.pdf`
2. Update the filename in `portfolio-config.json` and `portfolio-config-ko.json` if the PDF names change:
   ```json
   "cv_file": "./CV-Eng.pdf"
   ```
3. Update the download links in `index.html` and `index-ko.html` if the PDF names change:
   ```html
   <a href="./CV-Eng.pdf" download ...>
   ```

### CV Consistency Checklist

Before submitting to SK hynix or another target role, make sure the CV PDFs, HTML pages, and config files agree on:

- Years of experience: use "around 8 years" / "약 8년 차" unless the CV source is intentionally changed.
- Current positioning: keep "Software · AI Platform · SRE" / "소프트웨어 · AI 플랫폼 · SRE" consistent.
- Latest role: Samsung Electronics (AX Development Group), 2026 — Present.
- Samsung Research role: 2024 — 2025.
- Verified metrics only: 30,000 employees, 130,000 packets/sec, and 2.3x speedup are supported by the current PDFs.
- Remove or avoid unsupported metrics such as deployment-time reduction percentages unless the source CV or evidence supports them.
- Korean CV teaching assistant period currently needs source verification because it appears as `2018.03 - 2018.01`.
- Keep addresses/privacy level consistent across Korean and English CVs if you plan to publish the PDFs publicly.

### Changing Contact Information

Update the `"personal"` section in `portfolio-config.json`:

```json
"personal": {
  "name": "Your Name",
  "title": "Your Title",
  "email": "your@email.com",
  "phone": "+82 10-XXXX-XXXX",
  "location": "Your Location"
}
```

### Adding Social Links

Update the `"social"` section:

```json
"social": {
  "github": "https://github.com/yourusername",
  "linkedin": "https://www.linkedin.com/in/yourprofile",
  "twitter": "https://twitter.com/yourhandle"  // Add new platforms
}
```

### Updating Skills

Modify the `"skills"` array with skill levels (0-100):

```json
{
  "name": "Your Skill Name",
  "level": 85
}
```

### Adding Work Experience

Add to the `"experience"` array:

```json
{
  "title": "Job Title",
  "company": "Company Name",
  "period": "2020 — 2023",
  "location": "City, Country",
  "highlights": [
    "Achievement 1",
    "Achievement 2",
    "Achievement 3"
  ]
}
```

### Adding Publications

Add to the `"publications"` array:

```json
{
  "type": "paper",  // or "poster"
  "title": "Publication Title",
  "authors": "Author1, Author2, Your Name, Author3",
  "venue": "Conference/Journal Name",
  "year": 2024
}
```

## 🎨 Adding Custom Project Images

1. Add your image to `assets/images/` folder
2. Name it something like `my-project.jpg` or `my-project.png`
3. Reference it in your project:
   ```json
   "image": "./assets/images/my-project.jpg"
   ```

## 📝 Project Categories

Use these categories for projects:
- `"infrastructure"` - Cloud, Kubernetes, DevOps
- `"ai/ml"` - AI/ML systems, LLMs, distributed training
- `"automation"` - CI/CD, scripting, workflow automation

## 🔗 Project URLs

You can link to:
- GitHub repositories: `"https://github.com/username/repo"`
- Live demos: `"https://yourdemo.com"`
- Documentation: `"https://docs.yourproject.com"`
- Research papers: `"https://arxiv.org/abs/..."`

## ⚡ After Making Changes

1. Save your changes to `portfolio-config.json`
2. Save matching Korean changes to `portfolio-config-ko.json`
3. If you changed About, Resume, skills, PDF names, or language labels, update `index.html` and `index-ko.html`
4. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update portfolio content"
   git push origin main
   ```
5. Wait 1-2 minutes for GitHub Pages to rebuild

## 📱 Testing Locally

Before pushing, test your changes:
```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Then open:

- English: `http://127.0.0.1:4173/index.html`
- Korean: `http://127.0.0.1:4173/index-ko.html`

Do not rely only on opening `index.html` directly from Finder. The project fetches JSON config files, so testing over HTTP is safer.

## 🆘 Need Help?

- **CV not downloading?** Check the file path in `index.html` matches your PDF filename
- **Korean CV not downloading?** Check the file path in `index-ko.html` matches your Korean PDF filename
- **Projects not showing?** Verify the category name matches exactly: "infrastructure", "ai/ml", or "automation" in English and "인프라", "ai/ml", or "자동화" in Korean
- **Images not loading?** Ensure image paths start with `./assets/images/`
- **Filters not working?** Make sure project categories use lowercase: "ai/ml" not "AI/ML"

## 📂 File Structure

```
JINwonLEE.github.io/
├── index.html                 # Main website file
├── index-ko.html              # Korean website file
├── portfolio-config.json      # English project/config content
├── portfolio-config-ko.json   # Korean project/config content
├── HOW-TO-UPDATE.md          # This guide
├── CV-Eng.pdf                 # English CV PDF
├── CV-Kor.pdf                 # Korean CV PDF
├── assets/
│   ├── css/
│   │   └── style.css         # Styling
│   ├── images/               # Your images
│   │   ├── my-avatar.png     # Your profile photo
│   │   ├── project-1.jpg     # Project images
│   │   └── ...
│   └── js/
│       └── script.js         # Interactive features
```

## 🎯 Future Enhancements

Want to automate this further? You could:
1. Create a script that reads `portfolio-config.json` and generates HTML
2. Use a static site generator like Jekyll or Hugo
3. Build a simple admin panel

---

**Quick Tip:** Always keep backups of both config files and both CV PDFs before making major changes.
