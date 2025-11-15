# Git Quick Reference - Fork Workflow

## 🎯 Quick Setup (First Time)

```bash
# 1. Fork on GitHub (browser)
# Go to: https://github.com/moondevonyt/moon-dev-ai-agents
# Click: Fork button

# 2. Run the setup script
./setup_fork_workflow.sh

# OR do it manually:
git remote rename origin upstream
git remote add origin https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git
git push -u origin main
```

---

## 📋 Daily Commands

### Push YOUR changes

```bash
git add .
git commit -m "Updated my analysis"
git push origin main
```

### Pull YOUR changes on another computer

```bash
git pull origin main
```

### Get Moon Dev's latest updates

```bash
git fetch upstream
git merge upstream/main
git push origin main  # Share with your other computers
```

### Check status

```bash
git status              # What changed locally
git remote -v           # Show all remotes
git log --oneline -5    # Recent commits
```

---

## 🔄 Common Workflows

### Scenario: Working on Computer 1

```bash
# Morning routine
git pull origin main              # Get changes from Computer 2
git fetch upstream                # Check Moon Dev's updates
git merge upstream/main           # Merge if needed

# Make changes to ANALYSIS.md, custom agents, etc.

# Evening commit
git add ANALYSIS.md src/agents/custom/my_agent.py
git commit -m "Added custom agent, updated analysis"
git push origin main
```

### Scenario: Switch to Computer 2

```bash
# Pull your latest work
git pull origin main

# Continue working...

# Commit and push
git add .
git commit -m "Continued work from Computer 2"
git push origin main
```

### Scenario: Moon Dev Released New Agents

```bash
# Check what's new
git fetch upstream
git log main..upstream/main

# Merge his updates
git merge upstream/main

# If conflicts, resolve and commit
git add .
git commit -m "Merged upstream updates"

# Push to your fork
git push origin main
```

---

## 🚨 Emergency Commands

### "I'm confused, what's my setup?"

```bash
git remote -v
# Should show:
# origin    https://github.com/YOUR_USERNAME/... (YOUR fork)
# upstream  https://github.com/moondevonyt/... (Moon Dev's)
```

### "I have uncommitted changes but need to pull"

```bash
# Option 1: Commit them
git add .
git commit -m "WIP: saving progress"
git pull origin main

# Option 2: Stash them temporarily
git stash
git pull origin main
git stash pop  # Restore your changes
```

### "My computers are out of sync"

```bash
# On Computer 1
git pull origin main  # Get Computer 2's changes
git push origin main  # Send Computer 1's changes

# On Computer 2
git pull origin main  # Now synced
```

### "I accidentally modified a file Moon Dev also updated"

```bash
# After git merge upstream/main shows conflict:

# Keep his version
git checkout upstream/main -- src/config.py

# OR keep your version
git checkout --ours src/config.py

# Then commit
git add src/config.py
git commit -m "Resolved conflict"
```

---

## 📊 Understanding Your Setup

```
┌─────────────────────────────────────┐
│   Moon Dev's Repo (upstream)        │
│   github.com/moondevonyt/...        │
│   ⬇️ You can PULL                    │
│   ❌ You CANNOT push                 │
└─────────────────────────────────────┘
                ↓ fetch/merge
                ↓
┌─────────────────────────────────────┐
│   YOUR Computer (local)             │
│   /Users/padi/WorkLocal/...      │
│   ✏️ Make changes here                │
└─────────────────────────────────────┘
                ↕️ push/pull
                ↓
┌─────────────────────────────────────┐
│   YOUR Fork (origin)                │
│   github.com/YOUR_USERNAME/...      │
│   ✅ You can push/pull               │
└─────────────────────────────────────┘
                ↕️
┌─────────────────────────────────────┐
│   Your Other Computer               │
│   git clone from YOUR fork          │
└─────────────────────────────────────┘
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] `git remote -v` shows both `origin` (yours) and `upstream` (Moon Dev's)
- [ ] `git push` sends to YOUR fork
- [ ] ANALYSIS.md and GIT_WORKFLOW.md exist in YOUR repo only
- [ ] .env is ignored (never committed)
- [ ] You can clone YOUR fork on Computer 2

---

## 🎓 Key Concepts

| Term | Meaning |
|------|---------|
| **origin** | YOUR fork on GitHub (you can push/pull) |
| **upstream** | Moon Dev's original repo (you can pull only) |
| **fork** | Your copy of Moon Dev's repo on YOUR GitHub |
| **local** | Files on your computer |
| **remote** | Repository on GitHub |
| **main** | Primary branch (default) |
| **commit** | Save changes locally |
| **push** | Send commits to GitHub |
| **pull** | Get commits from GitHub |
| **fetch** | Download commits (don't merge yet) |
| **merge** | Combine commits from different sources |

---

## 🔒 Files That Stay Private

These are in `.gitignore` and will NEVER be pushed:

```
.env                    # Your API keys ✅
NOTES.md                # Your personal notes ✅
*.local                 # Any .local files ✅
src/data/my_data/       # Your data folder ✅
src/agents/custom/my_*  # Your custom agents ✅
```

---

## 🆘 Need Help?

**Check configuration:**
```bash
git remote show origin
git remote show upstream
git branch -vv
```

**See differences:**
```bash
git diff                        # Uncommitted changes
git diff origin/main           # Difference from YOUR GitHub
git diff upstream/main         # Difference from Moon Dev's
```

**Reset if needed:**
```bash
# ⚠️ WARNING: Discards all local changes!
git stash                      # Save changes temporarily
git reset --hard origin/main   # Match YOUR GitHub
git stash pop                  # Restore your changes (optional)
```

---

## 📚 Full Documentation

For detailed explanations, see:
- **GIT_WORKFLOW.md** - Complete guide with scenarios
- **setup_fork_workflow.sh** - Automated setup script

---

**Quick Help URLs:**
- Fork Guide: https://docs.github.com/en/get-started/quickstart/fork-a-repo
- Syncing Fork: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork

---

**Last Updated:** 2025-11-15
**Your Fork:** https://github.com/YOUR_USERNAME/moon-dev-ai-agents
