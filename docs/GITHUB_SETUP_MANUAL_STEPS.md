# GitHub Feature Request System - Manual Setup Steps

The feature request and voting system has been partially configured via files in `.github/` and documentation in `docs/`. However, some steps require manual configuration through the GitHub web interface.

---

## ✅ Already Done (via code/git)

These files have been created and committed:

- ✅ `.github/ISSUE_TEMPLATE/feature_request.yml` - Structured issue form for feature requests
- ✅ `.github/DISCUSSION_TEMPLATE/idea.yml` - Discussion template for ideas
- ✅ `docs/FEATURE_REQUESTS.md` - Comprehensive guide for users
- ✅ `docs/MANUAL_UPDATE_GUIDE.md` - CLI update troubleshooting guide
- ✅ `README.md` - Updated with feature request process

---

## 🔨 Manual Steps Required (GitHub Web UI)

### Step 1: Enable GitHub Discussions

**Why:** Discussions provide the voting and community feedback system for ideas.

**How:**
1. Go to: https://github.com/agit8or1/huduglue/settings
2. Scroll to "Features" section
3. Check ☑️ **Discussions**
4. Click **Save changes**
5. Navigate to the Discussions tab
6. Click **Set up discussions** (if prompted)

**Then configure categories:**
1. Go to: https://github.com/agit8or1/huduglue/discussions/categories
2. **Keep these default categories:**
   - 💬 **General** - General discussions
   - 🙋 **Q&A** - Questions and answers (enable answer marking)
3. **Create new categories:**

#### Category 1: Ideas 💡
- **Name:** Ideas
- **Description:** Propose new features and enhancements. Upvote (👍) ideas you want to see!
- **Emoji:** 💡 `:bulb:`
- **Format:** Open-ended discussion
- **Purpose:** Feature suggestions & community voting

#### Category 2: Polls 📊
- **Name:** Polls
- **Description:** Vote on feature priorities, design decisions, and project direction
- **Emoji:** 📊 `:bar_chart:`
- **Format:** Poll
- **Purpose:** Community voting on multiple options

---

### Step 2: Create GitHub Project (Roadmap)

**Why:** Tracks feature request lifecycle from triage to completion.

**How:**
1. Go to: https://github.com/agit8or1/huduglue/projects
2. Click **New project**
3. Choose **Board** layout
4. Name: `🗺️ Roadmap`
5. Description: `Feature requests and enhancements tracking`

**Configure columns:**
1. Delete default columns
2. Create these columns (in order):

| Column | Description |
|--------|-------------|
| **💡 Triage** | New requests being evaluated |
| **📋 Planned** | Approved for development |
| **🚧 In Progress** | Actively being worked on |
| **🧪 Testing** | Ready for testing/review |
| **✅ Done** | Completed and released |
| **🧊 On Hold** | Deferred pending dependencies |
| **❌ Won't Do** | Declined with explanation |

**Add automation:**
1. Click column name → **...** → **Workflows**
2. Enable these for **💡 Triage**:
   - Auto-add items: Issues with label `type:feature`
3. Enable these for **✅ Done**:
   - Auto-archive items: When issue is closed

---

### Step 3: Create Labels

**Why:** Organizes and filters feature requests by type, status, priority, and area.

**How:**
1. Go to: https://github.com/agit8or1/huduglue/labels
2. Click **New label** for each label below

#### Type Labels
- `type:feature` - #0075ca (blue) - New feature or enhancement
- `type:bug` - #d73a4a (red) - Bug report
- `type:documentation` - #0075ca (blue) - Documentation improvement

#### Status Labels
- `needs-triage` - #d4c5f9 (purple) - Needs initial review
- `status:planned` - #0e8a16 (green) - Approved for backlog
- `status:in-progress` - #fbca04 (yellow) - Active development
- `status:blocked` - #e99695 (red) - Waiting on external factors
- `status:completed` - #0e8a16 (green) - Shipped in release
- `status:wontfix` - #ffffff (white/gray) - Will not be implemented

#### Priority Labels
- `priority:critical` - #b60205 (dark red) - Blocking workflow
- `priority:high` - #d93f0b (orange) - Significantly improves productivity
- `priority:medium` - #fbca04 (yellow) - Nice to have
- `priority:low` - #0e8a16 (green) - Minor enhancement

#### Area Labels
- `area:assets` - #006b75 (teal) - Asset Management
- `area:vault` - #1d76db (blue) - Password Vault
- `area:docs` - #0075ca (blue) - Documentation system
- `area:monitoring` - #d4c5f9 (purple) - Website/Cert monitoring
- `area:integrations` - #5319e7 (purple) - PSA/RMM integrations
- `area:security` - #b60205 (red) - Security features
- `area:ui-ux` - #fbca04 (yellow) - User interface
- `area:performance` - #0e8a16 (green) - Speed/optimization
- `area:api` - #0075ca (blue) - REST API

#### Helper Labels
- `good first issue` - #7057ff (purple) - Good for newcomers
- `help wanted` - #008672 (teal) - Seeking contributors
- `duplicate` - #cfd3d7 (gray) - Duplicate of existing issue

**Tip:** You can bulk-import labels using GitHub CLI if available:
```bash
gh label create "type:feature" --color 0075ca --description "New feature or enhancement"
# ... repeat for each label
```

---

### Step 4: Create Pinned Discussion - "How to Request Features"

**Why:** Explains the feature request system to new users.

**How:**
1. Go to: https://github.com/agit8or1/huduglue/discussions
2. Click **New discussion**
3. Category: **💬 General**
4. Title: `🚀 How to Request Features & Vote on Ideas`
5. Body: (see content below)
6. Click **Start discussion**
7. Click **...** (three dots) → **Pin discussion**

**Content:**
```markdown
# 🚀 How to Request Features & Vote on Ideas

Welcome! HuduGlue uses a community-driven approach to feature development. Here's how you can help shape the project:

## 📝 Suggesting a New Feature

### Step 1: Start with an Idea Discussion

Have an idea? [Create a new discussion in the Ideas category](https://github.com/agit8or1/huduglue/discussions/new?category=ideas).

**What happens:**
1. Community members discuss and refine your idea
2. Others upvote by reacting with 👍 on your first post
3. Maintainers review popular ideas weekly

### Step 2: High-Voted Ideas Become Feature Requests

If your idea gets enough votes and aligns with project goals, maintainers will:
1. Promote it to a [Feature Request Issue](https://github.com/agit8or1/huduglue/issues/new?template=feature_request.yml)
2. Add it to the [🗺️ Roadmap Project](https://github.com/agit8or1/huduglue/projects)
3. Prioritize based on votes + impact + feasibility

## 👍 Voting on Existing Ideas

Browse [Ideas Category](https://github.com/agit8or1/huduglue/discussions/categories/ideas) and:
- **👍 Upvote** ideas you want (react to the first post)
- **💬 Comment** with your use case or suggestions
- ❌ Avoid "+1" comments (use reactions instead)

**Vote weight:**
- 1-5 votes: Low priority
- 6-15 votes: Medium priority
- 16-30 votes: High priority
- 31+ votes: Very high priority

## 🗺️ Tracking Progress

Watch the [Roadmap Project](https://github.com/agit8or1/huduglue/projects) to see:
- 💡 **Triage** - Being evaluated
- 📋 **Planned** - Approved for backlog
- 🚧 **In Progress** - Active development
- ✅ **Done** - Released

## 📖 Full Guide

Read the complete documentation: [docs/FEATURE_REQUESTS.md](https://github.com/agit8or1/huduglue/blob/main/docs/FEATURE_REQUESTS.md)

## ❓ Questions?

Post in the [Q&A category](https://github.com/agit8or1/huduglue/discussions/categories/q-a) or check out the [Getting Started](https://github.com/agit8or1/huduglue#readme) guide.

---

**Thank you for helping shape HuduGlue!** 🐕
```

---

### Step 5: Create Pinned Discussion - "How to Manually Update from CLI"

**Why:** Provides troubleshooting guide for users experiencing update issues.

**How:**
1. Go to: https://github.com/agit8or1/huduglue/discussions
2. Click **New discussion**
3. Category: **🙋 Q&A**
4. Title: `🔄 How to Manually Update HuduGlue from CLI (Troubleshooting)`
5. Body: Copy content from `docs/MANUAL_UPDATE_GUIDE.md` or link to it:

```markdown
# 🔄 How to Manually Update HuduGlue from CLI

If you're experiencing issues with automatic updates or need to manually update your installation, this guide will help.

## Quick Update

```bash
cd /home/administrator
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart huduglue-gunicorn.service
python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

Then **hard refresh your browser**: `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)

## 📖 Full Troubleshooting Guide

For complete step-by-step instructions, common issues, and automated update script, see:

👉 **[docs/MANUAL_UPDATE_GUIDE.md](https://github.com/agit8or1/huduglue/blob/main/docs/MANUAL_UPDATE_GUIDE.md)**

## Common Issues Covered

- ✅ Version shows old number after update
- ✅ Static files (CSS/JS) not updating
- ✅ Database migration failures
- ✅ Gunicorn won't start
- ✅ 502 Bad Gateway errors
- ✅ Merge conflicts during pull

## Need More Help?

If you're still stuck:
1. Check the [full guide](https://github.com/agit8or1/huduglue/blob/main/docs/MANUAL_UPDATE_GUIDE.md)
2. Post in [Q&A Discussions](https://github.com/agit8or1/huduglue/discussions/categories/q-a)
3. Report a bug: [Bug Report Form](https://github.com/agit8or1/huduglue/issues/new?template=bug_report.yml)
```

6. Click **Start discussion**
7. Click **...** (three dots) → **Pin discussion**

---

### Step 6: Update Repository Description

**Why:** Helps people find your project and understand it at a glance.

**How:**
1. Go to: https://github.com/agit8or1/huduglue
2. Click ⚙️ (gear icon) next to "About"
3. **Description:** `Self-hosted IT documentation platform with asset management, encrypted vault, PSA/RMM integrations, and monitoring for MSPs`
4. **Website:** (if you have a demo site)
5. **Topics:** Add relevant tags:
   - `msp`
   - `it-documentation`
   - `asset-management`
   - `password-manager`
   - `django`
   - `self-hosted`
   - `rmm`
   - `psa-integration`
6. Check ☑️ **Releases** and **Packages** (if using)
7. Click **Save changes**

---

### Step 7: Create Initial GitHub Issue for Update Troubleshooting

**Why:** Provides a sticky issue that users can reference for update problems.

**How:**
1. Go to: https://github.com/agit8or1/huduglue/issues
2. Click **New issue**
3. Choose **Open a blank issue** (don't use template)
4. **Title:** `[STICKY] Update Troubleshooting: How to Manually Update from CLI`
5. **Body:**

```markdown
## 📌 This is a sticky issue for update troubleshooting

If HuduGlue's automatic update isn't working or you're seeing an old version number, follow these manual update steps.

### Quick Fix

```bash
cd /home/administrator
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart huduglue-gunicorn.service
python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

**Then hard refresh your browser**: `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)

### Full Guide

For detailed troubleshooting, automated script, and common issues:

👉 **[docs/MANUAL_UPDATE_GUIDE.md](https://github.com/agit8or1/huduglue/blob/main/docs/MANUAL_UPDATE_GUIDE.md)**

### Related

- [Discussion: Manual Update Guide](https://github.com/agit8or1/huduglue/discussions) (pinned in Discussions)
- [CHANGELOG](https://github.com/agit8or1/huduglue/blob/main/CHANGELOG.md) - See what's new

### Still Having Issues?

Post in [Discussions → Q&A](https://github.com/agit8or1/huduglue/discussions/categories/q-a) or create a [Bug Report](https://github.com/agit8or1/huduglue/issues/new?template=bug_report.yml).
```

6. **Labels:** `documentation`, `help wanted`
7. Click **Submit new issue**
8. **Pin the issue:**
   - On the right sidebar, click **Pin issue**
   - This makes it stay at the top of the issues list

---

## 🎉 Setup Complete!

Once all steps are done, users will be able to:
- ✅ Suggest features via Discussions → Ideas
- ✅ Vote on ideas with 👍 reactions
- ✅ Track progress on the Roadmap Project
- ✅ Submit formal Feature Requests via issue form
- ✅ Get update help from pinned Discussion and sticky Issue

---

## 🔧 Optional: Set Up Automation

**Automatic label application:**

If you want issues to be automatically labeled based on keywords:
1. Go to: https://github.com/agit8or1/huduglue/settings/rules
2. Create rule: "Auto-label feature requests"
3. Trigger: Issue opened with template `feature_request.yml`
4. Action: Add labels `type:feature`, `needs-triage`

**Note:** This requires GitHub Pro or organization account. For free repos, labels must be added manually.

---

## 📝 Summary Checklist

Use this checklist to track your progress:

```
[ ] Step 1: Enable GitHub Discussions + create Idas and Polls categories
[ ] Step 2: Create Roadmap Project with 7 columns + automation
[ ] Step 3: Create all labels (type, status, priority, area, helper)
[ ] Step 4: Create + pin "How to Request Features" discussion
[ ] Step 5: Create + pin "Manual Update Guide" discussion
[ ] Step 6: Update repository description and topics
[ ] Step 7: Create + pin "Update Troubleshooting" issue
```

---

**Need help with these steps?** Feel free to reach out or post in Discussions!
