# Git User Ramp-Up Quickstart Guide

**Purpose:** Practical Git workflow guide for the Nick Pilot Project enhanced branch strategy
**Focus:** PowerShell-first approach with cross-platform compatibility
**Audience:** Team members, collaborators, and future project contributors
**Date:** July 16, 2025

---

## 🚀 Quick Start - Essential Commands

### **Daily Workflow PowerShell Commands**
```powershell
# Check project status
git status
git branch -a

# Create new session workflow
.\scripts\init-enhanced-session.ps1 session nick-article-refinement

# Validate before merge
.\scripts\validate-merge-candidate.ps1

# Standard workflow
git add .
git commit -m "feat: implement article enhancement framework"
git push origin feature/session-2024-12-07-nick-article-refinement
```

### **Emergency Commands**
```powershell
# Quick status check
git log --oneline -5
git diff HEAD

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Force sync with remote
git fetch origin
git reset --hard origin/master
```

---

## 🏗️ Enhanced Branch Strategy Overview

### **Branch Types & Naming Conventions**
```bash
master                              # Production baseline
├── feature/session-YYYY-MM-DD-{topic}    # AI engagement sessions
├── experimental/{category}                # Isolated exploration
├── enhancement/{improvement-area}         # APM framework improvements
├── template/{pattern-name}               # AI consulting patterns
├── client/{client-name}                  # Client customizations
└── integration/{merge-candidate}         # Pre-production validation
```

### **Workflow Selection Guide**
- **Article completion, client work:** `session` workflow
- **New tool development, R&D:** `experimental` workflow
- **APM improvements, system optimization:** `enhancement` workflow
- **Pattern extraction, methodology development:** `template` workflow
- **Client-specific customizations:** `client` workflow

---

## 📋 Step-by-Step CLI Walkthrough

### **Scenario 1: Starting New AI Session Work**

#### **Step 1: Initialize New Session**
```powershell
# Navigate to project directory
cd "C:\Users\{username}\Dev\LocProj\Nick Pilot Project"

# Verify clean starting state
git status
git pull origin master

# Create new session workflow
.\scripts\init-enhanced-session.ps1 session article-visual-integration
```

**Expected Output:**
```
🎯 Creating AI session workflow for structured engagement
🚀 Creating session workflow: feature/session-2024-12-07-article-visual-integration
✅ Branch created successfully
📝 Session context template initialized
🔧 Ready for development
```

#### **Step 2: Work on Your Changes**
```powershell
# Make your changes (edit files, create content, etc.)
# Then check what changed
git status
git diff

# Review changes before committing
git add .
git status  # Verify staged changes
```

#### **Step 3: Commit and Validate**
```powershell
# Commit with descriptive message
git commit -m "feat: implement visual integration framework for Nick article"

# Validate quality before push
.\scripts\validate-merge-candidate.ps1
```

#### **Step 4: Push and Prepare for Merge**
```powershell
# Push to remote
git push origin feature/session-2024-12-07-article-visual-integration

# Switch back to master for merge
git checkout master
git pull origin master

# Merge your work
git merge feature/session-2024-12-07-article-visual-integration
git push origin master

# Clean up branch
git branch -d feature/session-2024-12-07-article-visual-integration
git push origin --delete feature/session-2024-12-07-article-visual-integration
```

---

### **Scenario 2: Quick Experimental Work**

#### **Step 1: Create Experimental Branch**
```powershell
# Create experimental workflow
.\scripts\init-enhanced-session.ps1 experimental cognitive-priming-v2

# Verify branch creation
git branch
```

#### **Step 2: Experiment and Iterate**
```powershell
# Make experimental changes
# Commit frequently with descriptive messages
git add .
git commit -m "experiment: test alternative cognitive priming approach"

# Push for backup/sharing
git push origin experimental/cognitive-priming-v2
```

#### **Step 3: Evaluate and Decide**
```powershell
# If experiment successful, prepare for integration
.\scripts\validate-merge-candidate.ps1

# If experiment unsuccessful, archive and clean up
git checkout master
git branch -d experimental/cognitive-priming-v2
git push origin --delete experimental/cognitive-priming-v2
```

---

### **Scenario 3: Collaborating with Others**

#### **Step 1: Sync with Team Changes**
```powershell
# Always start by syncing
git checkout master
git pull origin master

# Check what's new
git log --oneline -10
```

#### **Step 2: Create Your Work Branch**
```powershell
# Create branch for your contribution
.\scripts\init-enhanced-session.ps1 enhancement task-networking-optimization

# Work on your changes
# Commit regularly
git add .
git commit -m "enhance: optimize task networking performance"
```

#### **Step 3: Keep Updated During Long Work**
```powershell
# Periodically sync with master (during long-running work)
git checkout master
git pull origin master
git checkout enhancement/task-networking-optimization
git rebase master  # Apply your changes on top of latest master
```

#### **Step 4: Submit for Review**
```powershell
# Final validation
.\scripts\validate-merge-candidate.ps1

# Push for review
git push origin enhancement/task-networking-optimization

# Create pull request via GitHub web interface or CLI
gh pr create --title "Optimize task networking performance" --body "Enhances task networking with performance improvements"
```

---

## 🔧 Validation Script Usage Examples

### **validate-merge-candidate.ps1 Deep Dive**

#### **Basic Usage**
```powershell
# Run validation on current branch
.\scripts\validate-merge-candidate.ps1

# Sample output interpretation:
# Score: 75/100 points = CONDITIONAL MERGE (address warnings)
# Score: 85/100 points = READY FOR MERGE (excellent quality)
# Score: 45/100 points = NEEDS IMPROVEMENT (major issues)
```

#### **Understanding Validation Criteria**
```powershell
# Validation checks:
# ✅ Documentation updates: +20 points
# ✅ Generated artifacts: +15 points
# ⚠️ Context bridging documentation: Missing (-10 points)
# ✅ Commit quality: +15 points
# ✅ Branch naming convention: +10 points
```

#### **Improving Your Score**
```powershell
# Common fixes for low scores:
# 1. Add documentation for new features
echo "# New Feature Documentation" > docs/new-feature.md
git add docs/new-feature.md

# 2. Include generated artifacts
# Make sure diagrams, reports, etc. are included

# 3. Improve commit messages
git commit --amend -m "feat: implement comprehensive enhancement with documentation"

# 4. Follow branch naming conventions
# Use: feature/session-*, experimental/*, enhancement/*, template/*, client/*
```

---

## 🖥️ GitHub Desktop + Cursor Integration

### **GitHub Desktop Workflow**

#### **Setting Up GitHub Desktop**
1. **Install GitHub Desktop** from [desktop.github.com](https://desktop.github.com)
2. **Clone Repository:**
   - File → Clone Repository
   - URL: `https://github.com/pfunk5150/nick-pilot-project`
   - Local Path: `C:\Users\{username}\Dev\LocProj\Nick Pilot Project`

#### **Daily Workflow in GitHub Desktop**
1. **Sync Changes:** Click "Fetch origin" to get latest updates
2. **Create Branch:** Current Branch → New Branch → `feature/session-2024-12-07-{topic}`
3. **Make Changes:** Edit files in Cursor IDE
4. **Review Changes:** See file changes in GitHub Desktop left panel
5. **Commit:** Add commit message → Commit to branch
6. **Validate:** Run `.\scripts\validate-merge-candidate.ps1` in terminal
7. **Push:** Click "Publish branch" or "Push origin"
8. **Create PR:** Click "Create Pull Request" button

#### **GitHub Desktop + PowerShell Integration**
```powershell
# Open PowerShell terminal in GitHub Desktop
# Repository → Open in Command Prompt
# Or use Cursor's integrated terminal

# Run validation scripts from GitHub Desktop's terminal
.\scripts\validate-merge-candidate.ps1

# Create session workflows
.\scripts\init-enhanced-session.ps1 session new-work-item
```

### **Cursor IDE Integration**

#### **Cursor Git Integration**
1. **Source Control Panel:** Ctrl+Shift+G to open Git panel
2. **Stage Changes:** Click "+" next to files to stage
3. **Commit:** Type message and Ctrl+Enter to commit
4. **Branch Management:** Bottom status bar shows current branch
5. **Push/Pull:** Use Command Palette (Ctrl+Shift+P) → "Git: Push"

#### **Cursor Terminal Integration**
```powershell
# Use Cursor's integrated terminal (Ctrl+`)
# All PowerShell commands work directly

# Quick Git status
git status

# Run project scripts
.\scripts\validate-merge-candidate.ps1

# Create new workflows
.\scripts\init-enhanced-session.ps1 experimental new-idea
```

#### **Cursor Git Best Practices**
- **Use GitLens Extension:** Enhanced Git visualization and history
- **Configure Git:** Set user name and email in Cursor settings
- **Branch Indicators:** Watch bottom status bar for current branch
- **Merge Conflicts:** Use Cursor's built-in merge conflict resolver

---

## 🔍 Troubleshooting Common Issues

### **Issue: Branch Creation Fails**
```powershell
# Problem: Branch already exists
# Solution: Delete old branch first
git branch -d old-branch-name
git push origin --delete old-branch-name

# Problem: Uncommitted changes
# Solution: Stash or commit changes
git stash  # Save changes temporarily
git checkout master
git stash pop  # Restore changes
```

### **Issue: Validation Script Fails**
```powershell
# Problem: PowerShell execution policy
# Solution: Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Problem: Git not found
# Solution: Add Git to PATH or use full path
$env:PATH += ";C:\Program Files\Git\bin"
```

### **Issue: Merge Conflicts**
```powershell
# Problem: Merge conflicts during rebase/merge
# Solution: Use Git tools or manual resolution

# 1. See conflicted files
git status

# 2. Edit files to resolve conflicts (remove <<<, ===, >>> markers)

# 3. Mark as resolved
git add resolved-file.md

# 4. Continue merge/rebase
git rebase --continue
# or
git merge --continue
```

### **Issue: Lost Work/Accidental Changes**
```powershell
# Problem: Accidentally deleted/changed files
# Solution: Use Git history

# 1. Check recent commits
git log --oneline -10

# 2. Restore specific file from previous commit
git checkout HEAD~1 -- path/to/file.md

# 3. Restore entire working directory to previous state
git reset --hard HEAD~1  # CAUTION: Loses all uncommitted work

# 4. Create branch from specific commit
git checkout -b recovery-branch abc1234
```

---

## ⚡ Power User Tips

### **Advanced PowerShell Git Aliases**
```powershell
# Add to your PowerShell profile
function gs { git status }
function gl { git log --oneline -10 }
function gd { git diff }
function ga { git add . }
function gc { param($msg) git commit -m $msg }
function gp { git push }
function gpu { git pull }

# Usage examples:
gs                              # Quick status
gc "feat: add new feature"      # Quick commit
gp                              # Quick push
```

### **Batch Operations**
```powershell
# Validate all branches
git branch --list | ForEach-Object {
    git checkout $_.Trim()
    .\scripts\validate-merge-candidate.ps1
}

# Clean up old branches
git branch --merged | Where-Object { $_ -notmatch "master|main" } | ForEach-Object {
    git branch -d $_.Trim()
}

# Update all tracking branches
git remote update origin --prune
```

### **Project-Specific Shortcuts**
```powershell
# Quick project navigation
cd "C:\Users\$env:USERNAME\Dev\LocProj\Nick Pilot Project"

# Project status check
function Check-ProjectStatus {
    git status
    .\scripts\validate-merge-candidate.ps1
    Write-Host "Current branch: $(git branch --show-current)" -ForegroundColor Green
}

# Quick session creation
function New-SessionBranch {
    param($topic)
    .\scripts\init-enhanced-session.ps1 session $topic
}
```

---

## 📚 Quick Reference

### **Essential Commands Cheat Sheet**
```powershell
# Project Setup
git clone https://github.com/pfunk5150/nick-pilot-project.git
cd nick-pilot-project

# Daily Workflow
git status                                              # Check status
git pull origin master                                  # Sync with remote
.\scripts\init-enhanced-session.ps1 session {topic}    # Create workflow
git add .                                              # Stage changes
git commit -m "descriptive message"                   # Commit
.\scripts\validate-merge-candidate.ps1                # Validate
git push origin {branch-name}                         # Push

# Branch Management
git branch                                             # List branches
git checkout master                                    # Switch to master
git merge {branch-name}                               # Merge branch
git branch -d {branch-name}                          # Delete local branch
git push origin --delete {branch-name}               # Delete remote branch

# Emergency
git stash                                             # Save work temporarily
git reset --hard origin/master                       # Reset to remote state
git reflog                                           # See command history
```

### **Validation Score Guide**
- **80-100 points:** ✅ Ready for merge (excellent quality)
- **60-79 points:** ⚠️ Conditional merge (address warnings)
- **40-59 points:** ⚠️ Needs improvement (major issues)
- **0-39 points:** ❌ Not ready (quality issues)

---

**Git Workflow Status:** 🔄 READY FOR TEAM ADOPTION
**PowerShell Integration:** ✅ FULLY OPERATIONAL
**Enterprise Support:** ✅ PROFESSIONAL WORKFLOW STANDARDS
**Team Collaboration:** ✅ GITHUB DESKTOP + CURSOR COMPATIBLE
