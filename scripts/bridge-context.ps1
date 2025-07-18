# scripts/bridge-context.ps1
# Enhanced context bridging for Claude AI sessions
# Generates comprehensive context packages for session initialization

param(
    [Parameter(Mandatory = $false)]
    [string]$WorkflowType = 'session',

    [Parameter(Mandatory = $false)]
    [string]$Topic = 'general',

    [Parameter(Mandatory = $false)]
    [switch]$IncludeGitHistory,

    [Parameter(Mandatory = $false)]
    [switch]$IncludeDiagnostics,

    [Parameter(Mandatory = $false)]
    [switch]$FullContext
)

Write-Host '🌉 Enhanced Context Bridging for Claude AI Sessions' -ForegroundColor Cyan
Write-Host '=================================================' -ForegroundColor Gray

$Date = Get-Date -Format 'yyyy-MM-dd-HHmm'
$ContextFile = "context_bridge_$Date.md"
$CurrentBranch = git branch --show-current

# Initialize context content
$ContextContent = @"
# Context Bridge: $WorkflowType Session

**Generated:** $(Get-Date)
**Branch:** $CurrentBranch
**Topic:** $Topic
**Session Type:** $WorkflowType

---

## 📋 SESSION CONTEXT OVERVIEW

### Project State
- **Repository:** Nick Pilot Project
- **Architecture:** Dual APM + EA Master Model
- **Phase:** Post-remediation with Git attribution strategy
- **Current Focus:** $Topic

### Key Commits for Reference
- **AI Baseline:** ``da76905`` (diagnostics/ai_baseline_post_remediation_quality_assessment.md)
- **User Enhanced:** ``71ce813`` (diagnostics/user_enhanced_post_remediation_quality_assessment.md)
- **Documentation:** ``ecbfb62`` (Git attribution strategy and analysis)

---

## 🎯 WORKFLOW-SPECIFIC CONTEXT

"@

# Add workflow-specific context
switch ($WorkflowType) {
    'session' {
        $ContextContent += @'

### Session Workflow Context
- **Purpose:** Structured AI engagement with clear deliverables
- **Expected Outputs:** Documentation, analysis, implementation artifacts
- **Success Criteria:** Meets APM methodology compliance standards
- **Merge Strategy:** Feature branch with validation before master integration

'@
    }
    'experimental' {
        $ContextContent += @'

### Experimental Workflow Context
- **Purpose:** Exploratory development and alternative approaches
- **Expected Outputs:** Proof of concepts, alternative implementations
- **Success Criteria:** Learning objectives met, documented findings
- **Merge Strategy:** Experimental branch isolation, selective integration

'@
    }
    'enhancement' {
        $ContextContent += @'

### Enhancement Workflow Context
- **Purpose:** APM framework improvements and optimization
- **Expected Outputs:** Enhanced methodologies, improved templates
- **Success Criteria:** Backward compatibility, improved effectiveness
- **Merge Strategy:** Enhancement branch with comprehensive testing

'@
    }
    'template' {
        $ContextContent += @'

### Template Development Context
- **Purpose:** AI consulting pattern development and standardization
- **Expected Outputs:** Reusable templates, pattern documentation
- **Success Criteria:** Generalizability, clear implementation guidance
- **Merge Strategy:** Template branch with validation across use cases

'@
    }
    'client' {
        $ContextContent += @'

### Client Customization Context
- **Purpose:** Engagement-specific customizations and adaptations
- **Expected Outputs:** Client-specific artifacts, custom implementations
- **Success Criteria:** Client requirements satisfaction, deliverable quality
- **Merge Strategy:** Client branch with selective master integration

'@
    }
}

# Add Git history if requested
if ($IncludeGitHistory -or $FullContext) {
    Write-Host '📚 Including Git history context...' -ForegroundColor Yellow
    $ContextContent += @"

## 📚 RECENT GIT HISTORY

### Recent Commits
``````
$(git log --oneline -10)
``````

### Current Status
``````
$(git status --porcelain)
``````

"@
}

# Add diagnostics if requested
if ($IncludeDiagnostics -or $FullContext) {
    Write-Host '🔍 Including diagnostic context...' -ForegroundColor Yellow
    $ContextContent += @'

## 🔍 DIAGNOSTIC CONTEXT

### Critical Issues Status
- **logs/README.md:** Documentation integrity failure (CRITICAL)
- **Python Environment:** .mypy_cache cleanup with uv environment preservation
- **Mermaid Diagrams:** Organization and quality assessment needed
- **Git Workflow:** Multi-branch documentation requests pending

### User Feedback Priority Items
1. Git workflow Mermaid diagrams (multi-branch + session mapping)
2. Tools directory README.md creation
3. 3-tier diagram abstraction review
4. Directory structure vs Git branch alignment

'@
}

# Add file references
$ContextContent += @"

## 📂 KEY FILE REFERENCES

### Git Attribution Strategy Files
- ``@diagnostics/ai_vs_user_comparison_analysis.md`` - Comprehensive change analysis
- ``@diagnostics/git_attribution_quick_reference.md`` - Usage guide for Cursor AI
- ``@diagnostics/line_by_line_annotations.txt`` - Complete blame analysis
- ``@diagnostics/meta_cognitive_context_analysis.md`` - Gap identification and user intent

### Current Diagnostic Assessment
- ``@diagnostics/user_enhanced_post_remediation_quality_assessment.md`` - User-corrected version
- ``@diagnostics/ai_baseline_post_remediation_quality_assessment.md`` - Original AI analysis

### Workflow Scripts
- ``@scripts/init-enhanced-session.ps1`` - Session initialization
- ``@scripts/validate-merge-candidate.ps1`` - Pre-merge validation
- ``@scripts/bridge-context.ps1`` - This bridging script

---

## 🚀 CURSOR AI USAGE PATTERNS

### For Immediate Context Loading
``````
@$ContextFile - This complete context bridge
@71ce813 - Reference user-enhanced diagnostics
@da76905 - Reference AI baseline for comparison
``````

### For Specific Analysis
``````
@diagnostics/meta_cognitive_context_analysis.md - User intent and gaps
git diff da76905..71ce813 -- diagnostics/ - Show exact user changes
``````

### For Workflow Execution
``````
Follow APM methodology with EA Master Model principles
Use smart-chain tool sequences for efficiency
Maintain Git attribution strategy for clear collaboration
``````

---

## ✅ CONTEXT BRIDGE CHECKLIST

- [ ] Repository state documented
- [ ] Workflow context established
- [ ] Key commits referenced
- [ ] File references provided
- [ ] User intent captured
- [ ] Gap analysis included
- [ ] Usage patterns documented

---

*Generated by bridge-context.ps1*
*Ready for Claude AI session initialization*

"@

# Write context file
$ContextContent | Out-File -FilePath $ContextFile -Encoding UTF8

Write-Host "✅ Context bridge generated: $ContextFile" -ForegroundColor Green
Write-Host '📋 Bridge includes:' -ForegroundColor Cyan
Write-Host "  - Workflow-specific context for $WorkflowType" -ForegroundColor White
Write-Host '  - Git attribution references (da76905, 71ce813, ecbfb62)' -ForegroundColor White
Write-Host '  - Key file references for Cursor AI' -ForegroundColor White
Write-Host '  - User intent and gap analysis integration' -ForegroundColor White

if ($IncludeGitHistory -or $FullContext) {
    Write-Host '  - Git history and status' -ForegroundColor White
}

if ($IncludeDiagnostics -or $FullContext) {
    Write-Host '  - Diagnostic context and priority items' -ForegroundColor White
}

Write-Host ''
Write-Host '🎯 Next Steps:' -ForegroundColor Yellow
Write-Host '1. Start new Claude session' -ForegroundColor White
Write-Host "2. Reference: @$ContextFile" -ForegroundColor White
Write-Host '3. Execute workflow with full context awareness' -ForegroundColor White
Write-Host ''
Write-Host '🔧 Available flags for next run:' -ForegroundColor Gray
Write-Host '  -IncludeGitHistory    # Add recent commits and status' -ForegroundColor Gray
Write-Host '  -IncludeDiagnostics   # Add diagnostic context' -ForegroundColor Gray
Write-Host '  -FullContext          # Include everything' -ForegroundColor Gray
