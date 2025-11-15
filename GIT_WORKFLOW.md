# Git Workflow Guide - Working with Upstream Repository

**Your Situation:**
- You're pulling from Moon Dev's repository (moondevonyt/moon-dev-ai-agents)
- You want to add your own files (ANALYSIS.md, private configs, notes)
- You want to sync YOUR changes across YOUR computers
- You DON'T want to push to Moon Dev's repo
- You DO want to pull Moon Dev's latest updates

---

## 🎯 RECOMMENDED SOLUTION: Fork + Upstream Workflow

### Step-by-Step Setup

#### 1. Create Your Own Fork on GitHub

**Go to:** https://github.com/moondevonyt/moon-dev-ai-agents

**Click:** "Fork" button (top-right)

**Result:** Creates `https://github.com/YOUR_USERNAME/moon-dev-ai-agents`

This is now YOUR repository that you control completely.

---

#### 2. Update Your Local Repository Configuration

Currently, your local repo points to Moon Dev's repo as "origin". We'll change this:

```bash
# Navigate to your project
cd /Users/padi/WorkLocal/moon-dev-ai-agents

# Rename current "origin" to "upstream" (Moon Dev's repo)
git remote rename origin upstream

# Add YOUR fork as "origin"
git remote add origin https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git

# Verify the setup
git remote -v
```

**Expected output:**
```
origin    https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git (fetch)
origin    https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git (push)
upstream  https://github.com/moondevonyt/moon-dev-ai-agents.git (fetch)
upstream  https://github.com/moondevonyt/moon-dev-ai-agents.git (push)
```

---

#### 3. Push Your Current Work to YOUR Fork

```bash
# Make sure you're on main branch
git checkout main

# Push to YOUR fork
git push -u origin main

# If you get errors about diverged history, use:
git push -u origin main --force  # ⚠️ Only first time!
```

---

#### 4. Set Up Your Private Files

Create a list of files that should ONLY exist in your fork:

```bash
# Files to keep private/local to your fork:
# - ANALYSIS.md (your analysis)
# - .env (your API keys - already in .gitignore)
# - NOTES.md (your personal notes)
# - GIT_WORKFLOW.md (this file)
# - Any custom agents you create in src/agents/custom/
```

**These files will NOT be in Moon Dev's repo**, so when you pull his updates, they won't conflict.

---

### 📋 Daily Workflow

#### Working on Your Computer

```bash
# 1. Make changes to your files
# Edit ANALYSIS.md, create custom agents, etc.

# 2. Commit YOUR changes
git add ANALYSIS.md GIT_WORKFLOW.md
git commit -m "Updated my analysis and notes"

# 3. Push to YOUR fork (origin)
git push origin main

# Now your changes are on GitHub in YOUR fork
# You can pull these on your other computer
```

---

#### Syncing to Your Other Computer

**On Computer 2:**

```bash
# First time setup on Computer 2
git clone https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git
cd moon-dev-ai-agents

# Add upstream (Moon Dev's repo)
git remote add upstream https://github.com/moondevonyt/moon-dev-ai-agents.git

# Regular syncing (pull YOUR latest changes)
git pull origin main
```

---

#### Getting Moon Dev's Latest Updates

**When Moon Dev publishes new agents or features:**

```bash
# 1. Fetch updates from upstream (Moon Dev's repo)
git fetch upstream

# 2. Merge his changes into your main branch
git checkout main
git merge upstream/main

# 3. Resolve conflicts if any (see below)

# 4. Push merged changes to YOUR fork
git push origin main
```

---

### 🔀 Handling Conflicts

**Scenario:** Moon Dev updates `src/config.py` and you also modified it.

```bash
# After `git merge upstream/main`, you might see:
# CONFLICT (content): Merge conflict in src/config.py

# 1. Open the conflicting file
code src/config.py  # or nano, vim, etc.

# 2. You'll see conflict markers:
<<<<<<< HEAD
# Your changes
MONITORED_TOKENS = ['your_token_address']
=======
# Moon Dev's changes
MONITORED_TOKENS = ['his_new_token']
>>>>>>> upstream/main

# 3. Decide what to keep (manual edit)
# Option A: Keep both
MONITORED_TOKENS = ['your_token_address', 'his_new_token']

# Option B: Keep yours
MONITORED_TOKENS = ['your_token_address']

# Option C: Keep his
MONITORED_TOKENS = ['his_new_token']

# 4. Remove conflict markers, save file

# 5. Mark as resolved
git add src/config.py
git commit -m "Merged upstream changes, kept my token list"

# 6. Push to YOUR fork
git push origin main
```

---

## 🎨 ALTERNATIVE: Separate Branch for Your Work

**Better option if you want cleaner separation:**

### Create a Personal Branch

```bash
# Create and switch to personal branch
git checkout -b my-work

# Make your changes
# Add ANALYSIS.md, custom agents, configs

# Commit to personal branch
git add .
git commit -m "My personal analysis and configs"

# Push personal branch to YOUR fork
git push -u origin my-work
```

### Keep Main Branch Clean (Tracking Upstream)

```bash
# Switch to main
git checkout main

# Pull Moon Dev's latest (main stays clean)
git pull upstream main

# Push to YOUR fork's main
git push origin main

# Merge upstream updates into your work
git checkout my-work
git merge main  # Brings in Moon Dev's updates
git push origin my-work
```

### Branch Workflow Diagram

```
main branch (tracks Moon Dev)
  ↓ pull from upstream
  ↓ merge into ↓
my-work branch (your stuff)
  ↓ push to origin
  ↓
Your Fork on GitHub
  ↓ pull on Computer 2
  ↓
Computer 2: my-work branch
```

---

## 📁 File Organization Strategy

### Files That Moon Dev Updates (Track Upstream)

```
src/
├── agents/          # Moon Dev adds new agents
├── models/          # Moon Dev updates LLM providers
├── nice_funcs.py    # Moon Dev adds utilities
├── config.py        # ⚠️ CAREFUL - you both modify this
├── main.py          # Moon Dev updates orchestrator
└── requirements.txt # Moon Dev adds dependencies
```

**Strategy:** Let Moon Dev's changes take precedence, merge carefully

---

### Your Personal Files (Never in Upstream)

```
ANALYSIS.md              # Your comprehensive analysis ✅
GIT_WORKFLOW.md          # This file ✅
NOTES.md                 # Your personal notes ✅
TODO.md                  # Your task tracking ✅
.env                     # Your API keys (in .gitignore) ✅

src/agents/custom/       # Your custom agents ✅
├── my_agent.py
└── my_strategy.py

src/strategies/custom/   # Your strategies ✅
└── my_rsi_strategy.py

docs/my_docs/            # Your documentation ✅
└── setup_notes.md
```

**These files won't conflict** because they don't exist in Moon Dev's repo.

---

### Files You Both Modify (Conflict Risk ⚠️)

```
src/config.py            # You: add tokens, he: updates settings
.gitignore               # You: add patterns, he: adds too
README.md                # He updates docs
```

**Strategy:** Use branches OR accept his changes and re-apply yours

---

## 🛡️ Protecting Your Private Data

### Current .gitignore (Already Safe)

```bash
# Check what's already ignored
cat .gitignore
```

**Should include:**
```
.env               # ✅ Your API keys
*.pyc              # ✅ Python compiled files
__pycache__/       # ✅ Python cache
.vscode/           # ✅ Editor settings
.DS_Store          # ✅ macOS files
```

### Add More Private Patterns

```bash
# Edit .gitignore
echo "NOTES.md" >> .gitignore
echo "TODO.md" >> .gitignore
echo "src/data/my_data/" >> .gitignore
echo "*.local" >> .gitignore

# Commit updated .gitignore
git add .gitignore
git commit -m "Added private file patterns"
```

**Pro tip:** Name your private configs with `.local` extension:
```
config.local.py       # Your local overrides (ignored)
secrets.local.json    # Your secrets (ignored)
```

---

## 🔄 Complete Sync Workflow

### Scenario: You Work on 2 Computers + Track Moon Dev's Updates

#### Computer 1 (Main Dev Machine)

```bash
# Morning: Get latest from everywhere
git fetch upstream        # Get Moon Dev's updates
git fetch origin          # Get your other computer's updates

# Check what changed
git log upstream/main..main     # See Moon Dev's new commits
git log origin/main..main       # See your pending commits

# Merge Moon Dev's updates
git merge upstream/main

# Work on your stuff
# Edit ANALYSIS.md, create custom agents, etc.

# Commit and push
git add ANALYSIS.md src/agents/custom/my_agent.py
git commit -m "Updated analysis, added custom agent"
git push origin main
```

#### Computer 2 (Laptop)

```bash
# Pull your latest work
git pull origin main

# Continue work
# Edit configs, test agents

# Commit and push
git add NOTES.md
git commit -m "Added testing notes"
git push origin main
```

#### Weekly: Check Moon Dev's Updates

```bash
# On either computer
git fetch upstream
git log main..upstream/main  # See what's new

# If there are updates you want:
git merge upstream/main
git push origin main  # Share with your other computer
```

---

## 🚨 Common Scenarios & Solutions

### Scenario 1: "I Accidentally Pushed to Upstream!"

**Problem:** You ran `git push` and it tried to push to Moon Dev's repo.

**Solution:**
```bash
# Don't panic! You don't have write access, so it failed.
# Just set your default push location:
git push -u origin main  # -u sets default

# Now `git push` will go to YOUR fork
```

---

### Scenario 2: "My Computers Have Different Changes"

**Problem:** Edited different files on each computer, now out of sync.

**Solution:**
```bash
# On Computer 1
git pull origin main  # Get Computer 2's changes
# If conflicts, resolve them
git add .
git commit -m "Merged changes from Computer 2"
git push origin main

# On Computer 2
git pull origin main  # Now in sync
```

---

### Scenario 3: "Moon Dev Updated a File I Modified"

**Problem:** Both modified `src/config.py`, merge conflict.

**Solution:**

**Option A: Accept his changes, re-apply yours**
```bash
git merge upstream/main
# Conflict in src/config.py

# Accept his version
git checkout upstream/main -- src/config.py
git add src/config.py

# Re-apply your changes manually
nano src/config.py
# Add your MONITORED_TOKENS back

git add src/config.py
git commit -m "Merged config, kept my tokens"
```

**Option B: Keep your version**
```bash
git merge upstream/main
# Conflict in src/config.py

# Keep your version
git checkout --ours src/config.py
git add src/config.py
git commit -m "Kept my config, will review his changes later"
```

**Option C: Merge manually** (see [Handling Conflicts](#-handling-conflicts) above)

---

### Scenario 4: "I Want to Ignore Config Changes"

**Problem:** Don't want to track `src/config.py` at all because you modify it constantly.

**Solution: Create a local config override**

```bash
# 1. Copy config.py to config.local.py
cp src/config.py src/config.local.py

# 2. Add to .gitignore
echo "src/config.local.py" >> .gitignore

# 3. Modify your code to use local config
# In your agents:
try:
    from src.config_local import *  # Your overrides
except ImportError:
    pass  # Fall back to default config
```

---

## 📊 Visual Workflow Summary

### Current Setup (Problematic)
```
Moon Dev's Repo
      ↓
Your Computer (origin points to his repo)
      ❌ Can't push
      ✅ Can pull
```

### Recommended Setup (Fork)
```
Moon Dev's Repo (upstream)
      ↓ (fetch/merge)
      ↓
Your Computer (local)
      ↕ (push/pull)
      ↓
Your Fork (origin)
      ↕ (push/pull)
      ↓
Your Other Computer
```

### With Personal Branch
```
Moon Dev's Repo (upstream)
      ↓
Your Fork (origin)
      ├── main (tracks upstream, clean)
      └── my-work (your changes)
            ↕
      Your Computers
```

---

## 🎯 Recommended Setup Command Summary

Run these commands to set up the **fork workflow**:

```bash
# 1. Fork on GitHub (web browser)
# Go to: https://github.com/moondevonyt/moon-dev-ai-agents
# Click: Fork button

# 2. Update local remotes
cd /Users/padi/WorkLocal/moon-dev-ai-agents
git remote rename origin upstream
git remote add origin https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git

# 3. Push your current work to YOUR fork
git push -u origin main

# 4. Create personal branch (optional but recommended)
git checkout -b my-work
git push -u origin my-work

# 5. Add private files to .gitignore
cat >> .gitignore << 'EOF'
# Personal files
NOTES.md
TODO.md
*.local
src/data/my_data/
EOF

git add .gitignore
git commit -m "Added private patterns to gitignore"
git push origin my-work
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `git remote -v` shows both `origin` (yours) and `upstream` (Moon Dev's)
- [ ] `git push` sends to YOUR fork without errors
- [ ] `git pull origin main` gets YOUR changes from YOUR fork
- [ ] `git fetch upstream` gets Moon Dev's updates without errors
- [ ] ANALYSIS.md exists only in YOUR fork, not in Moon Dev's repo
- [ ] .env is in .gitignore and never gets committed
- [ ] You can clone YOUR fork on Computer 2 and see your files

---

## 🆘 Getting Help

**Check remote configuration:**
```bash
git remote -v
git remote show origin
git remote show upstream
```

**Check branch status:**
```bash
git status
git branch -vv  # Shows tracking branches
```

**See what's different:**
```bash
git log origin/main..main           # Your unpushed commits
git log main..origin/main           # Commits on GitHub not in local
git log main..upstream/main         # Moon Dev's new commits
git diff upstream/main main         # All differences
git diff upstream/main main -- src/config.py  # Specific file
```

**Reset if needed:**
```bash
# ⚠️ DANGER: Discard all local changes
git reset --hard origin/main  # Match YOUR fork
git reset --hard upstream/main  # Match Moon Dev's repo

# Safer: Create backup first
git branch backup-$(date +%Y%m%d)
git reset --hard origin/main
```

---

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Get YOUR latest changes | `git pull origin main` |
| Push YOUR changes | `git push origin main` |
| Get Moon Dev's updates | `git fetch upstream && git merge upstream/main` |
| Check what's new from Moon Dev | `git log main..upstream/main` |
| Create personal branch | `git checkout -b my-work` |
| Switch to main branch | `git checkout main` |
| See all remotes | `git remote -v` |
| Sync Computer 2 | `git pull origin main` |

---

## 🎓 Learning Resources

**Understanding Git Workflows:**
- Official Git Book: https://git-scm.com/book/en/v2
- Fork vs Clone: https://docs.github.com/en/get-started/quickstart/fork-a-repo
- Syncing a Fork: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork

**Visual Git Tools:**
- GitKraken: https://www.gitkraken.com/ (GUI for Git)
- Git Graph (VS Code): Visualize branches
- `git log --graph --oneline --all` (command-line visualization)

---

## 🎉 Summary

**Your Workflow:**

1. ✅ Fork Moon Dev's repo to YOUR GitHub account
2. ✅ Push/pull YOUR changes to YOUR fork
3. ✅ Sync YOUR fork across YOUR computers
4. ✅ Pull Moon Dev's updates from upstream when needed
5. ✅ Keep ANALYSIS.md and other personal files in YOUR fork only
6. ✅ Never worry about pushing to Moon Dev's repo (you can't!)

**Result:**
- 🔒 Your private data stays private
- 🔄 You can sync across your computers
- ⬇️ You can pull Moon Dev's latest updates
- 🚫 You can't accidentally push to his repo
- 😊 Everyone's happy!

---

**Need Help?** Review this guide or check the [Getting Help](#-getting-help) section.

**Ready to Set Up?** Follow [Recommended Setup Command Summary](#-recommended-setup-command-summary).
