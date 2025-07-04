#!/bin/bash

# =============================================================================
# Nick Pilot Project - Git Repository Initialization Script
# =============================================================================
# Purpose: Initialize Git repository with retrospective baseline
# Usage: ./scripts/init-git-repository.sh
# =============================================================================

set -e  # Exit on any error

echo "🚀 Initializing Nick Pilot Project Git Repository..."
echo "=================================================="

# -----------------------------------------------------------------------------
# Step 1: Verify we're in the correct directory
# -----------------------------------------------------------------------------
if [[ ! -f "README.md" ]] || [[ ! -d "handbooks" ]]; then
    echo "❌ Error: Please run this script from the Nick Pilot Project root directory"
    echo "   Expected files: README.md, handbooks/, meta/, etc."
    exit 1
fi

echo "✅ Verified project directory structure"

# -----------------------------------------------------------------------------
# Step 2: Initialize Git repository
# -----------------------------------------------------------------------------
if [[ -d ".git" ]]; then
    echo "⚠️  Git repository already exists. Continuing with existing repo..."
else
    git init
    echo "✅ Initialized new Git repository"
fi

# -----------------------------------------------------------------------------
# Step 3: Create initial commit with baseline structure
# -----------------------------------------------------------------------------
echo "📦 Creating retrospective baseline commit..."

# Add core project structure (before AI engagement)
git add README.md
git add artifacts/
git add context_files/
git add handbooks/
git add meta/
git add prompts/
git add .gitignore

# Add initial logs structure (but not session content)
mkdir -p logs
touch logs/.gitkeep
git add logs/.gitkeep

# Add empty outputs directory
mkdir -p outputs
touch outputs/.gitkeep
git add outputs/.gitkeep

# Create baseline commit
git commit -m "📦 Initial baseline: Pre-AI engagement project structure

- Core scaffolding: artifacts/, handbooks/, meta/, prompts/
- Context materials: ILPA templates and client requirements
- Operations framework: engagement playbooks and orchestration
- Documentation: README.md with system architecture

This represents the project state before any AI chat sessions."

echo "✅ Created retrospective baseline commit"

# -----------------------------------------------------------------------------
# Step 4: Create branch structure
# -----------------------------------------------------------------------------
echo "🌿 Setting up branch structure..."

# Create development branch for ongoing work
git checkout -b dev/main-development
git checkout main

# Create experimental branch for script isolation
git checkout -b experimental/thread-condensing

# Move experimental scripts to this branch
if [[ -f "../chat_conversion_script.py" ]]; then
    mv ../chat_conversion_script.py ./
    git add chat_conversion_script.py
fi

if [[ -f "../chat_converter.py" ]]; then
    mv ../chat_converter.py ./
    git add chat_converter.py
fi

if [[ -f "../optimized_chat_context.json" ]]; then
    mv ../optimized_chat_context.json ./
    git add optimized_chat_context.json
fi

# Commit experimental scripts
if git diff --staged --quiet; then
    echo "ℹ️  No experimental scripts found to isolate"
else
    git commit -m "🧪 Isolate experimental thread condensing scripts

- chat_conversion_script.py: Session processing utilities
- chat_converter.py: Alternative conversation processor
- optimized_chat_context.json: Context optimization data

These scripts represent experimental work on Claude thread
condensing and should be developed separately from main project."
fi

# Return to main branch
git checkout main
echo "✅ Branch structure created"

# -----------------------------------------------------------------------------
# Step 5: Create scripts directory and automation
# -----------------------------------------------------------------------------
echo "🔧 Setting up automation scripts..."

mkdir -p scripts

# Create session initialization script
cat > scripts/init-session.sh << 'EOF'
#!/bin/bash
# Session initialization script for Claude engagement workflows

echo "🚀 Initializing new Claude session..."
echo "Current branch: $(git branch --show-current)"
echo "Recent commits:"
git log --oneline -3

read -p "📝 Enter session topic: " topic
read -p "🎯 Session type (feature/experiment/dev): " type

# Clean topic name for branch
clean_topic=$(echo "$topic" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
branch_name="${type}/session-$(date +%Y-%m-%d)-${clean_topic}"

git checkout main
git pull 2>/dev/null || echo "ℹ️  No remote configured yet"
git checkout -b "$branch_name"

echo "✅ Created branch: $branch_name"
echo "📋 Ready for Claude session initialization"
echo ""
echo "Next steps:"
echo "1. Start Claude session with project context"
echo "2. Generate artifacts and reasoning logs"
echo "3. Review and approve outputs"
echo "4. Run merge-session.sh to integrate approved work"
EOF

chmod +x scripts/init-session.sh

# Create merge script
cat > scripts/merge-session.sh << 'EOF'
#!/bin/bash
# Merge approved session work back to main branch

current_branch=$(git branch --show-current)

if [[ "$current_branch" == "main" ]]; then
    echo "❌ Error: Please run this from a session branch, not main"
    exit 1
fi

echo "🔄 Merging session: $current_branch"
echo "Files to be merged:"
git diff --name-only main

read -p "Continue with merge? (y/N): " confirm
if [[ $confirm != "y" && $confirm != "Y" ]]; then
    echo "❌ Merge cancelled"
    exit 1
fi

git checkout main
git merge "$current_branch" --no-ff -m "🔀 Merge session: $current_branch

$(git log --oneline main..$current_branch)"

echo "✅ Session merged successfully"
echo "🏷️  Creating tag..."
tag_name="session-$(date +%Y%m%d-%H%M)"
git tag "$tag_name" -m "Session completion: $current_branch"

echo "✅ Tagged as: $tag_name"
EOF

chmod +x scripts/merge-session.sh

git add scripts/
git commit -m "🔧 Add session management automation scripts

- init-session.sh: Guided session branch creation
- merge-session.sh: Approved work integration
- Supports feature/experiment/dev workflow patterns"

echo "✅ Automation scripts created"

# -----------------------------------------------------------------------------
# Step 6: Create README for Git workflow
# -----------------------------------------------------------------------------
cat > GIT_WORKFLOW.md << 'EOF'
# Git Workflow Guide - Nick Pilot Project

## Quick Start

### Starting a New Session
```bash
./scripts/init-session.sh
# Follow prompts to create session branch
```

### Merging Approved Work
```bash
./scripts/merge-session.sh
# Review changes and confirm merge
```

## Branch Strategy

- **main**: Stable baseline + approved deliverables
- **feature/session-YYYY-MM-DD-topic**: Structured AI engagement sessions
- **experiment/**: Exploratory work and alternative approaches
- **dev/**: Quick iterations and development work

## Workflow Pattern

1. **Initialize**: `./scripts/init-session.sh`
2. **Work**: Claude session generates artifacts
3. **Review**: Human quality gate and approval
4. **Integrate**: `./scripts/merge-session.sh`
5. **Archive**: Session branch preserved for reference

## File Management

- **Tracked**: Approved artifacts, core scaffolding, documentation
- **Ignored**: Large logs, temporary files, experimental outputs
- **Selective**: Use `git add -f` for specific artifacts worth preserving

## Best Practices

- Always work in session branches, never directly on main
- Use descriptive commit messages with emoji prefixes
- Tag major milestones and completed sessions
- Preserve experimental work in dedicated branches
EOF

git add GIT_WORKFLOW.md
git commit -m "📚 Add Git workflow documentation

- Quick start guide for session management
- Branch strategy explanation
- Best practices for AI engagement workflows"

echo "✅ Git workflow documentation created"

# -----------------------------------------------------------------------------
# Step 7: Summary and next steps
# -----------------------------------------------------------------------------
echo ""
echo "🎉 Git Repository Initialization Complete!"
echo "=========================================="
echo ""
echo "Repository structure:"
echo "├── main branch: Stable baseline"
echo "├── dev/main-development: Ongoing work"
echo "├── experimental/thread-condensing: Isolated scripts"
echo "└── scripts/: Session management automation"
echo ""
echo "Next steps:"
echo "1. Review GIT_WORKFLOW.md for usage patterns"
echo "2. Test session workflow: ./scripts/init-session.sh"
echo "3. Configure GitHub remote (optional)"
echo "4. Begin Phase 2: Context Export & Branch Workflow"
echo ""
echo "✅ Ready for AI engagement workflows!"
