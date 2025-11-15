#!/bin/bash

# Setup Fork Workflow for Moon Dev AI Agents
# This script helps you set up the proper Git workflow to:
# - Keep Moon Dev's repo as "upstream" (read-only)
# - Use YOUR fork as "origin" (read-write)
# - Sync your work across your computers
# - Pull Moon Dev's updates when available

set -e  # Exit on error

echo "🌙 Moon Dev Fork Workflow Setup"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "src/agents" ]; then
    echo -e "${RED}❌ Error: This doesn't look like the moon-dev-ai-agents directory${NC}"
    echo "Please run this script from the project root."
    exit 1
fi

echo -e "${GREEN}✅ Found moon-dev-ai-agents project${NC}"
echo ""

# Step 2: Check current remote setup
echo "📡 Current Git remote configuration:"
git remote -v
echo ""

# Step 3: Ask for GitHub username
echo -e "${YELLOW}⚠️  IMPORTANT: You need to fork the repository on GitHub first!${NC}"
echo ""
echo "Steps:"
echo "1. Open: https://github.com/moondevonyt/moon-dev-ai-agents"
echo "2. Click the 'Fork' button (top-right)"
echo "3. Wait for the fork to complete"
echo "4. Come back here"
echo ""
read -p "Have you forked the repository? (yes/no): " forked

if [ "$forked" != "yes" ]; then
    echo -e "${YELLOW}Please fork the repository first, then run this script again.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}Your GitHub username: inasacu${NC}"
github_username="inasacu"

echo ""
echo -e "${BLUE}Setting up workflow for: $github_username${NC}"
echo ""

# Step 4: Check if remotes need to be updated
current_origin=$(git remote get-url origin 2>/dev/null || echo "")

if [[ "$current_origin" == *"$github_username"* ]]; then
    echo -e "${GREEN}✅ Your fork is already set as 'origin'${NC}"
else
    echo "🔧 Updating remote configuration..."

    # Rename current origin to upstream (if it exists and points to moondevonyt)
    if [[ "$current_origin" == *"moondevonyt"* ]]; then
        echo "  - Renaming 'origin' to 'upstream'"
        git remote rename origin upstream
    fi

    # Add your fork as origin
    echo "  - Adding YOUR fork as 'origin'"
    git remote add origin "https://github.com/$github_username/moon-dev-ai-agents.git"

    echo -e "${GREEN}✅ Remotes updated${NC}"
fi

# Step 5: Ensure upstream is set correctly
if git remote | grep -q "upstream"; then
    upstream_url=$(git remote get-url upstream)
    if [[ "$upstream_url" != *"moondevonyt"* ]]; then
        echo "🔧 Fixing upstream URL..."
        git remote set-url upstream "https://github.com/moondevonyt/moon-dev-ai-agents.git"
    fi
else
    echo "🔧 Adding upstream remote..."
    git remote add upstream "https://github.com/moondevonyt/moon-dev-ai-agents.git"
fi

echo ""
echo "📡 Updated remote configuration:"
git remote -v
echo ""

# Step 6: Check current branch
current_branch=$(git branch --show-current)
echo "📌 Current branch: $current_branch"
echo ""

# Step 7: Ask about uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes:${NC}"
    git status --short
    echo ""
    read -p "Do you want to commit these changes now? (yes/no): " commit_changes

    if [ "$commit_changes" == "yes" ]; then
        echo ""
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
        echo -e "${GREEN}✅ Changes committed${NC}"
    else
        echo -e "${YELLOW}⚠️  Skipping commit. You can do it later.${NC}"
    fi
    echo ""
fi

# Step 8: Push to your fork
echo "🚀 Pushing to YOUR fork..."
read -p "Ready to push to your fork? (yes/no): " ready_push

if [ "$ready_push" == "yes" ]; then
    echo ""
    echo "Pushing current branch ($current_branch) to origin..."

    if git push -u origin "$current_branch" 2>&1; then
        echo -e "${GREEN}✅ Successfully pushed to YOUR fork!${NC}"
    else
        echo -e "${YELLOW}⚠️  Push failed. This might happen if the branch doesn't exist on your fork yet.${NC}"
        echo "Try this manually:"
        echo "  git push -u origin $current_branch --force"
        echo ""
        read -p "Try force push now? (yes/no): " force_push

        if [ "$force_push" == "yes" ]; then
            git push -u origin "$current_branch" --force
            echo -e "${GREEN}✅ Force pushed successfully!${NC}"
        fi
    fi
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo -e "${GREEN}Your Git workflow is now configured!${NC}"
echo ""
echo "📋 What you can do now:"
echo ""
echo "1️⃣  Push YOUR changes:"
echo "   git add ."
echo "   git commit -m 'Your changes'"
echo "   git push origin main"
echo ""
echo "2️⃣  Sync to your other computer:"
echo "   git clone https://github.com/$github_username/moon-dev-ai-agents.git"
echo "   cd moon-dev-ai-agents"
echo "   git remote add upstream https://github.com/moondevonyt/moon-dev-ai-agents.git"
echo ""
echo "3️⃣  Get Moon Dev's latest updates:"
echo "   git fetch upstream"
echo "   git merge upstream/main"
echo "   git push origin main"
echo ""
echo "4️⃣  Create a personal branch (recommended):"
echo "   git checkout -b my-work"
echo "   git push -u origin my-work"
echo ""
echo "📚 For detailed instructions, see: GIT_WORKFLOW.md"
echo ""
echo -e "${BLUE}Your fork URL: https://github.com/$github_username/moon-dev-ai-agents${NC}"
echo ""
