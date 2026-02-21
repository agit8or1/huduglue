# Screenshot Update - Quick Start Guide

## 🚀 Quick Method (5 minutes)

### Option 1: Manual Screenshots (Recommended)
```bash
# 1. Open Firefox/Chrome
# 2. Login to Client St0r
# 3. Take screenshots of these pages (in order of priority):

# NEW FEATURES (MUST HAVE):
- http://localhost:8000/vehicles/ → Save as: vehicles-dashboard.png
- http://localhost:8000/vehicles/vehicles/ → Save as: vehicles-list.png
- http://localhost:8000/vehicles/1/ → Save as: vehicle-detail-overview.png
- http://localhost:8000/security/package-scanner/ → Save as: package-scanner-dashboard.png
- http://localhost:8000/monitoring/racks/1/ → Save as: rack-enhanced.png

# CORE UPDATES (NICE TO HAVE):
- http://localhost:8000/ → Save as: dashboard.png
- http://localhost:8000/about/ → Save as: about-page.png
- http://localhost:8000/security/ → Save as: security-dashboard.png
```

### How to Take Screenshots in Firefox
1. Press **Shift + F2** (opens developer toolbar)
2. Type: `screenshot --fullpage filename.png`
3. Screenshot saves to Downloads folder
4. Move to `/home/administrator/docs/screenshots/`

### How to Take Screenshots in Chrome
1. Press **Ctrl + Shift + P** (Command Palette)
2. Type: "Capture full size screenshot"
3. Screenshot saves to Downloads folder
4. Move to `/home/administrator/docs/screenshots/`

---

## 📋 After Taking Screenshots

```bash
# 1. Move screenshots to correct folder
mv ~/Downloads/*.png /home/administrator/docs/screenshots/

# 2. Optimize (optional, saves space)
cd /home/administrator/docs/screenshots/
optipng -o7 *.png

# 3. Commit and push
git add docs/screenshots/
git commit -m "Add v3.10 feature screenshots"
git push origin main
```

---

## 🤖 Automated Method (Advanced)

If you have headless Chrome installed:

```bash
# Run automated screenshot capture
bash /home/administrator/scripts/take_screenshots.sh

# Review results
ls -lh /home/administrator/docs/screenshots/*.png

# Commit
git add docs/screenshots/ README.md
git commit -m "Update all screenshots for v3.10.7"
git push origin main
```

---

## ✅ Checklist

**Priority 1 - New Features (Required):**
- [ ] vehicles-dashboard.png
- [ ] vehicles-list.png
- [ ] vehicle-detail-overview.png
- [ ] vehicle-detail-maintenance.png
- [ ] vehicle-detail-fuel.png
- [ ] vehicle-detail-damage.png
- [ ] vehicle-damage-form.png
- [ ] package-scanner-dashboard.png
- [ ] rack-enhanced.png

**Priority 2 - Core Updates (Recommended):**
- [ ] dashboard.png (show v3.10.7)
- [ ] about-page.png (show v3.10.7)
- [ ] security-dashboard.png (show package scanner widget)

**Priority 3 - Verification (Optional):**
- [ ] Verify all existing screenshots still accurate

---

## 📝 Tips

1. **Demo Data**: Use test/demo data, not real client information
2. **Resolution**: 1920x1080 browser window
3. **Zoom**: 100% zoom level (Ctrl+0)
4. **Theme**: Use default light theme
5. **Version**: Ensure v3.10.7 shows in footer
6. **Clean UI**: Close notifications/alerts before capturing

---

## 🎯 Goal

**12 new screenshots** minimum to showcase v3.9-3.10 features on GitHub!
