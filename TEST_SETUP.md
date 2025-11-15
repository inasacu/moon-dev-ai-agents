# Testing Your Fork Workflow Setup

## 🎯 Purpose

This guide helps you verify that your Git fork workflow is set up correctly.

We'll test:
1. ✅ Git remotes are configured
2. ✅ You can push to YOUR fork
3. ✅ You can pull from YOUR fork
4. ✅ You can fetch from upstream (Moon Dev's repo)
5. ✅ Private files are ignored
6. ✅ You're ready to sync across computers

---

## 📋 Pre-Test Checklist

Before running tests, make sure you:

- [ ] Forked the repository on GitHub
- [ ] Ran `./setup_fork_workflow.sh` (or configured manually)
- [ ] Know your fork URL: `https://github.com/YOUR_USERNAME/moon-dev-ai-agents`

---

## 🧪 Test Suite

### Test 1: Verify Git Remotes

**What we're testing:** Git knows about both repos

**Run this command:**
```bash
git remote -v
```

**Expected output:**
```
origin    https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git (fetch)
origin    https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git (push)
upstream  https://github.com/moondevonyt/moon-dev-ai-agents.git (fetch)
upstream  https://github.com/moondevonyt/moon-dev-ai-agents.git (push)
```

**✅ Pass criteria:**
- Shows both `origin` and `upstream`
- `origin` points to YOUR GitHub username
- `upstream` points to `moondevonyt`

**❌ If failed:**
```bash
# Fix: Add missing remote
git remote add origin https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git
# OR
git remote add upstream https://github.com/moondevonyt/moon-dev-ai-agents.git
```

---

### Test 2: Check Current Branch

**What we're testing:** You're on the main branch

**Run this command:**
```bash
git branch --show-current
```

**Expected output:**
```
main
```

**✅ Pass criteria:**
- Shows `main` (or `master` in older repos)

**❌ If failed:**
```bash
# Switch to main
git checkout main
```

---

### Test 3: Check Git Status

**What we're testing:** No unexpected changes

**Run this command:**
```bash
git status
```

**Expected output (if clean):**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**OR (if you have new files):**
```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        ANALYSIS.md
        GIT_WORKFLOW.md
        ... (other new files)
```

**✅ Pass criteria:**
- Shows current branch
- Lists files you added (ANALYSIS.md, etc.)
- .env is NOT listed (it's ignored)

---

### Test 4: Verify .gitignore Works

**What we're testing:** Private files are ignored

**Run this command:**
```bash
# Check if .env is ignored
git check-ignore -v .env
```

**Expected output:**
```
.gitignore:8:.env    .env
```

**✅ Pass criteria:**
- Shows that .env is ignored
- Points to .gitignore rule

**Test with another file:**
```bash
# Create a test private file
echo "test" > NOTES.md

# Check if it's ignored
git status | grep NOTES.md
```

**Expected: Nothing** (because NOTES.md is in .gitignore)

**Cleanup:**
```bash
rm NOTES.md
```

---

### Test 5: Test Commit (Dry Run)

**What we're testing:** You can create commits

**Run these commands:**
```bash
# Create a test file
echo "Test commit - $(date)" > test_file.txt

# Stage it
git add test_file.txt

# Check status
git status
```

**Expected output:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   test_file.txt
```

**✅ Pass criteria:**
- File is staged (green in git status)
- Ready to commit

**Commit it:**
```bash
git commit -m "Test commit - verifying setup"
```

**Expected output:**
```
[main abc1234] Test commit - verifying setup
 1 file changed, 1 insertion(+)
 create mode 100644 test_file.txt
```

---

### Test 6: Test Push to YOUR Fork

**What we're testing:** You can push to origin (YOUR fork)

**⚠️ This actually pushes to GitHub!**

**Run this command:**
```bash
git push origin main
```

**Expected output:**
```
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 345 bytes | 345.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git
   abc1234..def5678  main -> main
```

**✅ Pass criteria:**
- Push succeeds
- Shows your fork URL
- No errors

**❌ If failed with "Permission denied":**
```bash
# Fix: Make sure origin points to YOUR fork
git remote set-url origin https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git
git push origin main
```

**Verify on GitHub:**
1. Go to `https://github.com/YOUR_USERNAME/moon-dev-ai-agents`
2. You should see `test_file.txt` in the file list
3. Latest commit message should show "Test commit - verifying setup"

---

### Test 7: Test Fetch from Upstream

**What we're testing:** You can fetch from Moon Dev's repo

**Run this command:**
```bash
git fetch upstream
```

**Expected output:**
```
From https://github.com/moondevonyt/moon-dev-ai-agents
 * [new branch]      main       -> upstream/main
```

**OR (if already fetched):**
```
From https://github.com/moondevonyt/moon-dev-ai-agents
```

**✅ Pass criteria:**
- Command succeeds
- No errors
- Shows Moon Dev's repo URL

**Check what was fetched:**
```bash
git log --oneline main..upstream/main
```

**Expected:**
- Shows any commits Moon Dev has that you don't
- OR nothing (if you're up to date)

---

### Test 8: Test Pull from YOUR Fork

**What we're testing:** You can pull from origin (simulate Computer 2)

**Run this command:**
```bash
git pull origin main
```

**Expected output:**
```
From https://github.com/YOUR_USERNAME/moon-dev-ai-agents
 * branch            main       -> FETCH_HEAD
Already up to date.
```

**✅ Pass criteria:**
- Command succeeds
- Shows "Already up to date" (because you just pushed)

---

### Test 9: Verify File Tracking

**What we're testing:** Right files are tracked/ignored

**Run this command:**
```bash
# List tracked files
git ls-files | head -20
```

**Should include:**
- ✅ README.md
- ✅ src/config.py
- ✅ src/agents/*.py
- ✅ ANALYSIS.md (if you added it)
- ✅ GIT_WORKFLOW.md (if you added it)

**Should NOT include:**
- ❌ .env
- ❌ __pycache__/
- ❌ *.pyc files

**Check ignored files:**
```bash
git status --ignored
```

**Should show ignored files like:**
- .env
- __pycache__/
- temp_data/
- etc.

---

### Test 10: Simulate Computer 2 Workflow

**What we're testing:** End-to-end sync simulation

**In a different directory (simulate Computer 2):**
```bash
# Go to different location
cd /tmp

# Clone YOUR fork
git clone https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git test-clone
cd test-clone

# Add upstream remote
git remote add upstream https://github.com/moondevonyt/moon-dev-ai-agents.git

# Verify remotes
git remote -v

# Check files
ls -la
```

**Expected:**
- ✅ Clone succeeds
- ✅ All your files are there (ANALYSIS.md, test_file.txt, etc.)
- ✅ Can see remotes properly configured

**Make a change (simulate work on Computer 2):**
```bash
echo "Work from Computer 2" > computer2_work.txt
git add computer2_work.txt
git commit -m "Work from Computer 2"
git push origin main
```

**Back on Computer 1:**
```bash
cd /Users/padi/WorkLocal/moon-dev-ai-agents
git pull origin main
```

**Expected:**
- ✅ You get `computer2_work.txt` on Computer 1
- ✅ Sync works!

**Cleanup:**
```bash
rm -rf /tmp/test-clone
```

---

## 📊 Test Results Summary

### After Running All Tests

**Create results file:**
```bash
cat > TEST_RESULTS.txt << EOF
Git Fork Workflow Test Results
===============================
Date: $(date)

Test 1 - Git Remotes: ___________
Test 2 - Current Branch: ___________
Test 3 - Git Status: ___________
Test 4 - .gitignore: ___________
Test 5 - Commit: ___________
Test 6 - Push to Fork: ___________
Test 7 - Fetch Upstream: ___________
Test 8 - Pull from Fork: ___________
Test 9 - File Tracking: ___________
Test 10 - Computer Sync: ___________

Overall Status: ___________
Notes:


EOF

cat TEST_RESULTS.txt
```

**Fill in with:**
- ✅ PASS
- ❌ FAIL
- ⚠️ WARNING

---

## 🎯 Success Criteria

**You're ready to use the fork workflow if:**

- ✅ All 10 tests pass
- ✅ You can push to YOUR fork
- ✅ You can fetch from upstream
- ✅ Private files (.env) are ignored
- ✅ Sync simulation worked

---

## 🧹 Cleanup Test Files

**After all tests pass, clean up:**
```bash
# Remove test files
rm -f test_file.txt computer2_work.txt TEST_RESULTS.txt

# Commit cleanup
git add .
git commit -m "Cleanup: removed test files"
git push origin main
```

---

## 🆘 Troubleshooting Test Failures

### Test 6 Failed: Can't Push to Fork

**Error:** `Permission denied` or `Authentication failed`

**Solutions:**

1. **Check if you're pushing to the right place:**
   ```bash
   git remote get-url origin
   # Should be YOUR username, not moondevonyt
   ```

2. **Fix the URL:**
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/moon-dev-ai-agents.git
   ```

3. **Check GitHub authentication:**
   ```bash
   # If using HTTPS, you might need a personal access token
   # Go to: GitHub → Settings → Developer settings → Personal access tokens
   # Create token with 'repo' scope
   # Use token as password when pushing
   ```

---

### Test 7 Failed: Can't Fetch from Upstream

**Error:** `Repository not found`

**Solution:**
```bash
# Fix upstream URL
git remote set-url upstream https://github.com/moondevonyt/moon-dev-ai-agents.git

# Try again
git fetch upstream
```

---

### Test 4 Failed: .env Not Ignored

**Problem:** `git status` shows .env

**Solution:**
```bash
# Make sure .env is in .gitignore
grep ".env" .gitignore

# If not there, add it
echo ".env" >> .gitignore

# If it was already tracked, untrack it
git rm --cached .env

# Commit .gitignore
git add .gitignore
git commit -m "Updated .gitignore"
```

---

## ✅ Final Verification

**Run this command to verify everything:**
```bash
cat << 'EOF'
╔════════════════════════════════════════════╗
║  Git Fork Workflow - Final Verification   ║
╚════════════════════════════════════════════╝

Checking Git remotes...
EOF

git remote -v

cat << 'EOF'

Checking current branch...
EOF

git branch --show-current

cat << 'EOF'

Checking if .env is ignored...
EOF

git check-ignore -v .env

cat << 'EOF'

Checking your fork on GitHub...
EOF

echo "Your fork: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/')"

cat << 'EOF'

✅ If all above look correct, you're ready!

Next steps:
1. Commit your documentation files
2. Push to your fork
3. Start working!
EOF
```

---

## 🎓 What You Learned

By completing these tests, you verified:

1. **Git Configuration** - Remotes point to the right places
2. **Push Access** - You can push to YOUR fork
3. **Pull Access** - You can pull from YOUR fork
4. **Upstream Access** - You can fetch from Moon Dev's repo
5. **Privacy** - .env and other private files are ignored
6. **Sync** - You can sync between computers
7. **Workflow** - The entire fork workflow functions

---

**Test Status:** [ ] Not Started / [ ] In Progress / [ ] Complete

**Last Tested:** ___________

**Issues Found:** ___________
