#!/bin/bash

# Daily Upstream Sync Script for Moon Dev AI Agents
# This script automatically pulls updates from Moon Dev's repo and pushes to your fork
# Runs daily via cron

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log file
LOG_DIR="/Users/padilla/WorkLocal/moon-dev-ai-agents/logs"
LOG_FILE="$LOG_DIR/sync_$(date +%Y%m%d_%H%M%S).log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🌙 Starting daily upstream sync..."

# Navigate to project directory
cd /Users/padilla/WorkLocal/moon-dev-ai-agents || {
    log "${RED}❌ Error: Could not navigate to project directory${NC}"
    exit 1
}

log "📍 Current directory: $(pwd)"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    log "${RED}❌ Error: Not a git repository${NC}"
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
log "📌 Current branch: $CURRENT_BRANCH"

# Stash any uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    log "${YELLOW}⚠️  Uncommitted changes detected, stashing...${NC}"
    git stash push -m "Auto-stash before daily sync $(date +%Y%m%d_%H%M%S)" | tee -a "$LOG_FILE"
    STASHED=true
else
    STASHED=false
    log "✅ No uncommitted changes"
fi

# Fetch from upstream
log "📡 Fetching from upstream (Moon Dev's repo)..."
if git fetch upstream 2>&1 | tee -a "$LOG_FILE"; then
    log "${GREEN}✅ Fetch successful${NC}"
else
    log "${RED}❌ Fetch failed${NC}"
    exit 1
fi

# Check if there are updates
BEHIND_COUNT=$(git rev-list --count HEAD..upstream/main 2>/dev/null || echo "0")
log "📊 Commits behind upstream: $BEHIND_COUNT"

if [ "$BEHIND_COUNT" -eq 0 ]; then
    log "${GREEN}✅ Already up-to-date with Moon Dev's repo${NC}"

    # Restore stashed changes if any
    if [ "$STASHED" = true ]; then
        log "♻️  Restoring stashed changes..."
        git stash pop | tee -a "$LOG_FILE"
    fi

    log "🎉 Sync complete - no updates needed"
    exit 0
fi

# Merge upstream changes
log "🔄 Merging $BEHIND_COUNT new commits from Moon Dev's repo..."
if git merge upstream/main --no-edit -m "Auto-merge upstream updates $(date +%Y-%m-%d)" 2>&1 | tee -a "$LOG_FILE"; then
    log "${GREEN}✅ Merge successful${NC}"
else
    log "${RED}❌ Merge failed - conflicts detected${NC}"
    log "${YELLOW}⚠️  Manual intervention required${NC}"
    log "Please resolve conflicts manually and run: git push origin main"

    # Send notification (macOS)
    osascript -e 'display notification "Git merge conflicts detected. Manual intervention required." with title "Moon Dev Sync Failed"' 2>/dev/null || true

    exit 1
fi

# Push to your fork
log "🚀 Pushing merged updates to YOUR fork..."
if git push origin "$CURRENT_BRANCH" 2>&1 | tee -a "$LOG_FILE"; then
    log "${GREEN}✅ Push successful${NC}"
else
    log "${RED}❌ Push failed${NC}"
    exit 1
fi

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    log "♻️  Restoring stashed changes..."
    if git stash pop 2>&1 | tee -a "$LOG_FILE"; then
        log "${GREEN}✅ Stashed changes restored${NC}"
    else
        log "${YELLOW}⚠️  Conflict restoring stashed changes${NC}"
        log "Your changes are still in stash. Run: git stash list"
    fi
fi

# Summary
log "📝 Sync Summary:"
log "   - Merged $BEHIND_COUNT commits from Moon Dev"
log "   - Pushed to github.com/inasacu/moon-dev-ai-agents"
log "   - Branch: $CURRENT_BRANCH"

# Send success notification (macOS)
osascript -e "display notification \"Successfully synced $BEHIND_COUNT updates from Moon Dev\" with title \"Moon Dev Sync Complete\"" 2>/dev/null || true

log "🎉 Daily sync complete!"

# Keep only last 30 days of logs
find "$LOG_DIR" -name "sync_*.log" -type f -mtime +30 -delete 2>/dev/null || true

exit 0
