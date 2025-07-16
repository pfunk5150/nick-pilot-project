# Git Workflow Guide - Nick Pilot Project

**Evolution Layer:** ✅ [BASELINE] - Original engagement workflow foundation

## Quick Start

### Starting a New Session
```powershell
./scripts/init-enhanced-session.ps1
# Follow prompts to create session branch
```

### Merging Approved Work
```powershell
./scripts/validate-merge-candidate.ps1
# Run validation and follow merge instructions
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

## Current Repository Status

**✅ Git Repository Initialized**
- Core project structure committed to main branch
- .gitignore configured for AI engagement workflows
- Session management scripts created
- Ready for Phase 2: Context Export & Branch Workflow Setup

## Experimental Files Identified for Isolation

The following files should be moved to `experimental/thread-condensing` branch:
- `chat_conversion_script.py` (11,960 bytes)
- `chat_converter.py` (7,426 bytes)
- `optimized_chat_context.json` (4,504 bytes)
- `example_optimized_output.json` (7,585 bytes)

## Next Steps

1. **Complete Branch Setup**: Create experimental and development branches
2. **Isolate Experimental Scripts**: Move thread condensing utilities to separate branch
3. **Phase 2 Preparation**: Set up context export automation
4. **GitHub Integration**: Configure remote repository and branch protection
