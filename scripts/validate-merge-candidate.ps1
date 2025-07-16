# scripts/validate-merge-candidate.ps1
# Pre-merge validation with APM compliance checking (PowerShell)

$CurrentBranch = git branch --show-current
$ValidationScore = 0
$MaxScore = 100

Write-Host "🔍 Validating merge candidate: $CurrentBranch" -ForegroundColor Cyan
Write-Host '================================================' -ForegroundColor Gray

# APM methodology compliance check
Write-Host '📋 Checking APM compliance...' -ForegroundColor Yellow
if (Test-Path 'workflow_context_*.md') {
    Write-Host '✅ Workflow context documented (+20 points)' -ForegroundColor Green
    $ValidationScore += 20
}
else {
    Write-Host '⚠️ Warning: Workflow context documentation missing' -ForegroundColor Yellow
}

if (Test-Path 'task_completion_checklist.md') {
    Write-Host '✅ Task completion checklist present (+15 points)' -ForegroundColor Green
    $ValidationScore += 15
}
else {
    Write-Host '⚠️ Warning: Task completion checklist missing' -ForegroundColor Yellow
}

# Documentation completeness validation
Write-Host ''
Write-Host '📚 Validating documentation...' -ForegroundColor Yellow
try {
    $DocUpdates = (git diff --name-only master | Where-Object { $_ -match '\.(md|mmd)$' }).Count
    if ($DocUpdates -gt 0) {
        Write-Host "✅ Documentation updates detected: $DocUpdates files (+20 points)" -ForegroundColor Green
        $ValidationScore += 20
    }
    else {
        Write-Host '⚠️ Warning: No documentation updates found' -ForegroundColor Yellow
    }
}
catch {
    Write-Host '⚠️ Warning: Could not check documentation updates' -ForegroundColor Yellow
}

# Artifact quality assessment
Write-Host ''
Write-Host '🎨 Checking artifact quality...' -ForegroundColor Yellow
try {
    $Artifacts = (git diff --name-only master | Where-Object { $_ -match '\.(mmd|json|py|ps1)$' }).Count
    if ($Artifacts -gt 0) {
        Write-Host "✅ Generated artifacts: $Artifacts files (+15 points)" -ForegroundColor Green
        $ValidationScore += 15
    }
    else {
        Write-Host 'ℹ️ No artifacts generated (documentation-only changes)' -ForegroundColor Cyan
    }
}
catch {
    Write-Host 'ℹ️ Could not check artifacts' -ForegroundColor Cyan
}

# Context preservation verification
Write-Host ''
Write-Host '🌉 Verifying context preservation...' -ForegroundColor Yellow
if (Test-Path 'context_bridge_log.md') {
    Write-Host '✅ Context bridging documented (+10 points)' -ForegroundColor Green
    $ValidationScore += 10
}
else {
    Write-Host '⚠️ Warning: Context bridging documentation missing' -ForegroundColor Yellow
}

# Git commit quality check
Write-Host ''
Write-Host '📝 Checking commit quality...' -ForegroundColor Yellow
try {
    $CommitCount = (git rev-list --count master..$CurrentBranch)
    if ($CommitCount -gt 0) {
        Write-Host "✅ Commits present: $CommitCount commits (+10 points)" -ForegroundColor Green
        $ValidationScore += 10

        # Check for meaningful commit messages
        $MeaningfulCommits = (git log --oneline master..$CurrentBranch | Select-String -Pattern '(feat|fix|docs|style|refactor|test|chore)').Count
        if ($MeaningfulCommits -gt 0) {
            Write-Host "✅ Meaningful commit messages: $MeaningfulCommits commits (+10 points)" -ForegroundColor Green
            $ValidationScore += 10
        }
    }
    else {
        Write-Host '❌ No commits found on branch' -ForegroundColor Red
    }
}
catch {
    Write-Host '❌ Could not check commit history' -ForegroundColor Red
}

# Branch naming compliance
Write-Host ''
Write-Host '🏷️ Checking branch naming...' -ForegroundColor Yellow
if ($CurrentBranch -match '^(feature/session-|experimental/|enhancement/|template/|client/)') {
    Write-Host '✅ Branch naming follows convention (+10 points)' -ForegroundColor Green
    $ValidationScore += 10
}
else {
    Write-Host "⚠️ Warning: Branch naming doesn't follow enhanced convention" -ForegroundColor Yellow
}

# Calculate final score and recommendation
Write-Host ''
Write-Host '================================================' -ForegroundColor Gray
Write-Host '📊 VALIDATION SUMMARY' -ForegroundColor Cyan
Write-Host '================================================' -ForegroundColor Gray
Write-Host "Score: $ValidationScore / $MaxScore points" -ForegroundColor White

if ($ValidationScore -ge 80) {
    Write-Host '✅ READY FOR MERGE - Excellent quality' -ForegroundColor Green
    Write-Host '🎯 Recommendation: Proceed with merge' -ForegroundColor Green
}
elseif ($ValidationScore -ge 60) {
    Write-Host '⚠️ CONDITIONAL MERGE - Good quality with minor issues' -ForegroundColor Yellow
    Write-Host '🎯 Recommendation: Address warnings and merge' -ForegroundColor Yellow
}
elseif ($ValidationScore -ge 40) {
    Write-Host '⚠️ NEEDS IMPROVEMENT - Moderate quality issues' -ForegroundColor Yellow
    Write-Host '🎯 Recommendation: Address major issues before merge' -ForegroundColor Yellow
}
else {
    Write-Host '❌ NOT READY FOR MERGE - Quality issues detected' -ForegroundColor Red
    Write-Host '🎯 Recommendation: Complete missing requirements' -ForegroundColor Red
}

Write-Host ''
Write-Host '🔧 Next steps:' -ForegroundColor White
Write-Host "  git add . && git commit -m 'Address validation feedback'" -ForegroundColor Gray
Write-Host "  git checkout master && git merge $CurrentBranch" -ForegroundColor Gray
Write-Host '  git push origin master' -ForegroundColor Gray

exit 0
