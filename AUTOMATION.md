# 🤖 Automated Daily Sync - Documentation

**Setup Date:** 2025-11-15
**Status:** ✅ Active

---

## What This Does

Automatically syncs Moon Dev's latest updates to your fork **every day at 3:00 AM**.

```
Every Day at 3 AM:
1. Fetch Moon Dev's latest changes
2. Merge them into your local code
3. Push to YOUR fork (github.com/inasacu/moon-dev-ai-agents)
4. Send macOS notification with results
5. Log everything
```

---

## Files Created

### 1. Sync Script
**Location:** `/Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh`

**What it does:**
- ✅ Fetches from upstream (Moon Dev's repo)
- ✅ Checks for new commits
- ✅ Auto-stashes your uncommitted work (if any)
- ✅ Merges Moon Dev's updates
- ✅ Pushes to YOUR fork
- ✅ Restores your uncommitted work
- ✅ Sends macOS notifications
- ✅ Creates detailed logs
- ✅ Handles conflicts gracefully

### 2. Cron Job
**Schedule:** Daily at 3:00 AM

**Crontab entry:**
```bash
0 3 * * * /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh >> /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/cron.log 2>&1
```

### 3. Logs Directory
**Location:** `/Users/padilla/WorkLocal/moon-dev-ai-agents/logs/`

**Files:**
- `sync_YYYYMMDD_HHMMSS.log` - Detailed sync logs for each run
- `cron.log` - Cron execution log
- Logs older than 30 days are auto-deleted

---

## How to Check It's Working

### View Recent Sync Logs
```bash
# See the latest sync log
ls -lt /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/sync_*.log | head -1 | xargs cat

# See all sync logs
ls -lt /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/sync_*.log
```

### View Cron Log
```bash
tail -f /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/cron.log
```

### Check Cron Job Status
```bash
crontab -l | grep moon-dev
```

**Expected output:**
```
# Moon Dev AI Agents - Daily upstream sync (runs at 3 AM)
0 3 * * * /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh >> /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/cron.log 2>&1
```

---

## Manual Sync (Run Anytime)

If you want to sync NOW instead of waiting for 3 AM:

```bash
cd /Users/padilla/WorkLocal/moon-dev-ai-agents
./sync_upstream_daily.sh
```

**You'll see:**
```
🌙 Starting daily upstream sync...
📍 Current directory: /Users/padilla/WorkLocal/moon-dev-ai-agents
📌 Current branch: main
✅ No uncommitted changes
📡 Fetching from upstream (Moon Dev's repo)...
✅ Fetch successful
📊 Commits behind upstream: 5
🔄 Merging 5 new commits from Moon Dev's repo...
✅ Merge successful
🚀 Pushing merged updates to YOUR fork...
✅ Push successful
🎉 Daily sync complete!
```

---

## What Happens in Different Scenarios

### Scenario 1: No Updates Available
```
✅ Already up-to-date with Moon Dev's repo
🎉 Sync complete - no updates needed
```
**Result:** Nothing changes, script exits cleanly

---

### Scenario 2: New Updates Available
```
📊 Commits behind upstream: 3
🔄 Merging 3 new commits from Moon Dev's repo...
✅ Merge successful
🚀 Pushing merged updates to YOUR fork...
✅ Push successful
```
**Result:**
- Your local code updated with Moon Dev's 3 new commits
- Your fork on GitHub updated
- macOS notification: "Successfully synced 3 updates from Moon Dev"

---

### Scenario 3: You Have Uncommitted Work
```
⚠️  Uncommitted changes detected, stashing...
Saved working directory and index state WIP on main: 13c1bd3
📡 Fetching from upstream...
🔄 Merging 2 new commits...
✅ Merge successful
🚀 Pushing to fork...
✅ Push successful
♻️  Restoring stashed changes...
✅ Stashed changes restored
```
**Result:**
- Your uncommitted work is temporarily saved
- Moon Dev's updates are merged
- Your uncommitted work is restored
- Everything works seamlessly!

---

### Scenario 4: Merge Conflict Detected
```
🔄 Merging updates...
❌ Merge failed - conflicts detected
⚠️  Manual intervention required
Please resolve conflicts manually and run: git push origin main
```
**Result:**
- macOS notification: "Git merge conflicts detected. Manual intervention required."
- Script stops safely
- You need to manually resolve conflicts

**How to fix:**
```bash
cd /Users/padilla/WorkLocal/moon-dev-ai-agents

# See which files have conflicts
git status

# Edit conflicting files to resolve
# (Git marks conflicts with <<<<<<< and >>>>>>>)

# After resolving:
git add .
git commit -m "Resolved merge conflicts"
git push origin main
```

---

## Notifications

### Success Notification
When sync succeeds with updates:
```
Title: Moon Dev Sync Complete
Message: Successfully synced 3 updates from Moon Dev
```

### Failure Notification
When conflicts are detected:
```
Title: Moon Dev Sync Failed
Message: Git merge conflicts detected. Manual intervention required.
```

---

## Logs Explained

### Sample Log Entry
```
[2025-11-15 03:00:01] 🌙 Starting daily upstream sync...
[2025-11-15 03:00:01] 📍 Current directory: /Users/padilla/WorkLocal/moon-dev-ai-agents
[2025-11-15 03:00:01] 📌 Current branch: main
[2025-11-15 03:00:01] ✅ No uncommitted changes
[2025-11-15 03:00:02] 📡 Fetching from upstream (Moon Dev's repo)...
[2025-11-15 03:00:03] ✅ Fetch successful
[2025-11-15 03:00:03] 📊 Commits behind upstream: 2
[2025-11-15 03:00:03] 🔄 Merging 2 new commits from Moon Dev's repo...
[2025-11-15 03:00:04] ✅ Merge successful
[2025-11-15 03:00:04] 🚀 Pushing merged updates to YOUR fork...
[2025-11-15 03:00:06] ✅ Push successful
[2025-11-15 03:00:06] 📝 Sync Summary:
[2025-11-15 03:00:06]    - Merged 2 commits from Moon Dev
[2025-11-15 03:00:06]    - Pushed to github.com/inasacu/moon-dev-ai-agents
[2025-11-15 03:00:06]    - Branch: main
[2025-11-15 03:00:06] 🎉 Daily sync complete!
```

**What this tells you:**
- Started at 3:00:01 AM ✅
- Found 2 new commits from Moon Dev ✅
- Merged successfully ✅
- Pushed to your fork ✅
- Total time: 5 seconds

---

## Managing the Automation

### Stop Daily Sync
```bash
# Remove the cron job
crontab -l | grep -v "sync_upstream_daily.sh" | crontab -
```

### Change Sync Time
```bash
# Edit crontab
crontab -e

# Change this line:
0 3 * * * /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh

# Examples:
# 0 1 * * *   = 1:00 AM daily
# 0 12 * * *  = 12:00 PM daily
# 0 */6 * * * = Every 6 hours
# 0 3 * * 1   = 3:00 AM every Monday only
```

### Re-enable After Stopping
```bash
(crontab -l 2>/dev/null; echo "# Moon Dev AI Agents - Daily upstream sync"; echo "0 3 * * * /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh >> /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/cron.log 2>&1") | crontab -
```

---

## Troubleshooting

### Problem: No logs being created

**Check if cron is running:**
```bash
crontab -l | grep sync_upstream
```

**Run manually to see errors:**
```bash
/Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh
```

---

### Problem: Script runs but nothing happens

**Check the logs:**
```bash
cat /Users/padilla/WorkLocal/moon-dev-ai-agents/logs/cron.log
```

**Verify you're up-to-date:**
```bash
cd /Users/padilla/WorkLocal/moon-dev-ai-agents
git fetch upstream
git log HEAD..upstream/main --oneline
# If empty output = you're up-to-date
```

---

### Problem: Notifications not appearing

**macOS notification permissions:**
1. System Preferences → Notifications
2. Find "Script Editor" or "Terminal"
3. Enable "Allow Notifications"

**Test notification manually:**
```bash
osascript -e 'display notification "Test" with title "Test Title"'
```

---

### Problem: Sync stopped working

**Check if script is executable:**
```bash
ls -la /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh
# Should show: -rwxr-xr-x (x = executable)
```

**If not executable:**
```bash
chmod +x /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh
```

**Check Git remotes:**
```bash
cd /Users/padilla/WorkLocal/moon-dev-ai-agents
git remote -v
# Should show:
# origin   → github.com/inasacu/moon-dev-ai-agents.git
# upstream → github.com/moondevonyt/moon-dev-ai-agents.git
```

---

## What Gets Synced

### Automatically Synced ✅
- New agents Moon Dev creates
- Updates to existing agents
- Bug fixes
- New features
- Documentation updates from Moon Dev
- Changes to src/, scripts/, etc.

### NOT Synced (Protected) ✅
Your personal files in `.gitignore`:
- `.env` (your API keys)
- `src/data/padi/` (your personal data)
- `NOTES.md`, `TODO.md` (your notes)
- All your documentation (ANALYSIS.md, etc.)
- Personal strategies in `src/strategies/custom/padi_*.py`

---

## Benefits of Automation

**Before automation:**
```bash
# Every week, manually:
git fetch upstream
git merge upstream/main
git push origin main
# Easy to forget!
```

**With automation:**
```
✅ Happens every night at 3 AM
✅ Never forget
✅ Wake up to latest Moon Dev updates
✅ Your fork stays synced automatically
✅ Your other computers get updates automatically
✅ You get notified if something needs attention
```

---

## Log Retention

**Automatic cleanup:**
- Logs older than 30 days are automatically deleted
- Keeps your logs directory clean
- Prevents disk space issues

**Override cleanup period:**
Edit `sync_upstream_daily.sh` line 118:
```bash
# Change 30 to desired days
find "$LOG_DIR" -name "sync_*.log" -type f -mtime +30 -delete
```

---

## Security Notes

**Safe operations:**
- ✅ Never overwrites your uncommitted work (uses stash)
- ✅ Never force pushes (preserves your fork's history)
- ✅ Stops on conflicts (requires manual review)
- ✅ Logs everything (full audit trail)
- ✅ Your `.env` is protected by `.gitignore`

**What the script CAN'T do:**
- ❌ Cannot expose your API keys
- ❌ Cannot delete your personal files
- ❌ Cannot push to Moon Dev's repo (you don't have permission)
- ❌ Cannot run without your computer being on

---

## Computer Sleep / Power

**Important:** Your computer must be ON and awake at 3 AM for cron to run.

**Options:**

### Option 1: Keep computer awake
```bash
# Disable sleep until 4 AM (macOS)
caffeinate -u -t 3600 &  # Runs at 2 AM, keeps awake for 1 hour
```

### Option 2: Use pmset to wake computer (macOS)
```bash
# Wake computer at 2:55 AM daily
sudo pmset repeat wakeorpoweron MTWRFSU 02:55:00
```

### Option 3: Run sync at convenient time
Change cron to run when your computer is usually on:
```bash
# Example: 10 AM instead of 3 AM
0 10 * * * /Users/padilla/WorkLocal/moon-dev-ai-agents/sync_upstream_daily.sh
```

---

## Summary

**What you have now:**
- ✅ Automated daily sync at 3 AM
- ✅ Stash/unstash uncommitted work automatically
- ✅ macOS notifications for success/failure
- ✅ Detailed logs with 30-day retention
- ✅ Conflict detection with safe failure
- ✅ Manual run capability anytime
- ✅ Your work protected by .gitignore

**Your workflow:**
1. Wake up each morning
2. Check notification (if Moon Dev added updates)
3. Pull changes on your other computers: `git pull origin main`
4. Start coding with latest Moon Dev updates!

**Zero maintenance required!** 🎉

---

**Automation Status:** ✅ Active (runs daily at 3:00 AM)
**Next Run:** Tomorrow at 03:00:00
**Logs:** `/Users/padilla/WorkLocal/moon-dev-ai-agents/logs/`
**Manual Sync:** `./sync_upstream_daily.sh`

---

**Related Documentation:**
- `GIT_WORKFLOW.md` - Complete Git workflow guide
- `GIT_QUICK_REFERENCE.md` - Quick command reference
- `SETUP_FOR_INASACU.md` - Initial setup guide
