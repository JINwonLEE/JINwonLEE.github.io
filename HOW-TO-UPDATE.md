# How to Update Your Portfolio

This guide explains how to easily update your portfolio content without diving into HTML.

## 📁 Configuration File

All your portfolio content is stored in **`portfolio-config.json`**. This makes it easy to:
- Add new projects
- Update your information
- Modify skills and experience
- Add publications

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
  "technologies": ["Tech1", "Tech2", "Tech3"],
  "image": "./assets/images/your-image.jpg",
  "url": "https://github.com/yourusername/project",
  "featured": true  // Set to true to show in main portfolio
}
```

### Updating Your CV

1. Replace `Jinwon_CV_260126.pdf` with your new CV file
2. Update the filename in `portfolio-config.json`:
   ```json
   "cv_file": "./YourNewCV.pdf"
   ```
3. Update the download link in `index.html` (line 297):
   ```html
   <a href="./YourNewCV.pdf" download ...>
   ```

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
2. If you added new projects, update `index.html` to use them
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update portfolio content"
   git push origin main
   ```
4. Wait 1-2 minutes for GitHub Pages to rebuild

## 📱 Testing Locally

Before pushing, test your changes:
```bash
open index.html
```

## 🆘 Need Help?

- **CV not downloading?** Check the file path in `index.html` matches your PDF filename
- **Projects not showing?** Verify the category name matches exactly: "infrastructure", "ai/ml", or "automation"
- **Images not loading?** Ensure image paths start with `./assets/images/`
- **Filters not working?** Make sure project categories use lowercase: "ai/ml" not "AI/ML"

## 📂 File Structure

```
JINwonLEE.github.io/
├── index.html                 # Main website file
├── portfolio-config.json      # YOUR CONTENT (edit this!)
├── HOW-TO-UPDATE.md          # This guide
├── Jinwon_CV_260126.pdf      # Your CV PDF
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

**Quick Tip:** Always keep a backup of `portfolio-config.json` before making major changes!
