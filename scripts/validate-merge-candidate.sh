#!/bin/bash
# scripts/validate-merge-candidate.sh
# Pre-merge validation with APM compliance checking

CURRENT_BRANCH=$(git branch --show-current)
VALIDATION_SCORE=0
MAX_SCORE=100

echo "🔍 Validating merge candidate: $CURRENT_BRANCH"
echo "================================================"

# APM methodology compliance check
echo "📋 Checking APM compliance..."
if [[ -f "workflow_context_*.md" ]]; then
    echo "✅ Workflow context documented (+20 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 20))
else
    echo "⚠️ Warning: Workflow context documentation missing"
fi

if [[ -f "task_completion_checklist.md" ]]; then
    echo "✅ Task completion checklist present (+15 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 15))
else
    echo "⚠️ Warning: Task completion checklist missing"
fi

# Documentation completeness validation
echo ""
echo "📚 Validating documentation..."
DOC_UPDATES=$(git diff --name-only master | grep -E "\.(md|mmd)$" | wc -l)
if [[ $DOC_UPDATES -gt 0 ]]; then
    echo "✅ Documentation updates detected: $DOC_UPDATES files (+20 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 20))
else
    echo "⚠️ Warning: No documentation updates found"
fi

# Artifact quality assessment
echo ""
echo "🎨 Checking artifact quality..."
ARTIFACTS=$(git diff --name-only master | grep -E "\.(mmd|json|py|sh)$" | wc -l)
if [[ $ARTIFACTS -gt 0 ]]; then
    echo "✅ Generated artifacts: $ARTIFACTS files (+15 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 15))
else
    echo "ℹ️ No artifacts generated (documentation-only changes)"
fi

# Context preservation verification
echo ""
echo "🌉 Verifying context preservation..."
if [[ -f "context_bridge_log.md" ]]; then
    echo "✅ Context bridging documented (+10 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 10))
else
    echo "⚠️ Warning: Context bridging documentation missing"
fi

# Git commit quality check
echo ""
echo "📝 Checking commit quality..."
COMMIT_COUNT=$(git rev-list --count master..$CURRENT_BRANCH)
if [[ $COMMIT_COUNT -gt 0 ]]; then
    echo "✅ Commits present: $COMMIT_COUNT commits (+10 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 10))

    # Check for meaningful commit messages
    MEANINGFUL_COMMITS=$(git log --oneline master..$CURRENT_BRANCH | grep -E "(feat|fix|docs|style|refactor|test|chore)" | wc -l)
    if [[ $MEANINGFUL_COMMITS -gt 0 ]]; then
        echo "✅ Meaningful commit messages: $MEANINGFUL_COMMITS commits (+10 points)"
        VALIDATION_SCORE=$((VALIDATION_SCORE + 10))
    fi
else
    echo "❌ No commits found on branch"
fi

# Branch naming compliance
echo ""
echo "🏷️ Checking branch naming..."
if [[ $CURRENT_BRANCH =~ ^(feature/session-|experimental/|enhancement/|template/|client/) ]]; then
    echo "✅ Branch naming follows convention (+10 points)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 10))
else
    echo "⚠️ Warning: Branch naming doesn't follow enhanced convention"
fi

# Calculate final score and recommendation
echo ""
echo "================================================"
echo "📊 VALIDATION SUMMARY"
echo "================================================"
echo "Score: $VALIDATION_SCORE / $MAX_SCORE points"

if [[ $VALIDATION_SCORE -ge 80 ]]; then
    echo "✅ READY FOR MERGE - Excellent quality"
    echo "🎯 Recommendation: Proceed with merge"
elif [[ $VALIDATION_SCORE -ge 60 ]]; then
    echo "⚠️ CONDITIONAL MERGE - Good quality with minor issues"
    echo "🎯 Recommendation: Address warnings and merge"
elif [[ $VALIDATION_SCORE -ge 40 ]]; then
    echo "⚠️ NEEDS IMPROVEMENT - Moderate quality issues"
    echo "🎯 Recommendation: Address major issues before merge"
else
    echo "❌ NOT READY FOR MERGE - Quality issues detected"
    echo "🎯 Recommendation: Complete missing requirements"
fi

echo ""
echo "🔧 Next steps:"
echo "  git add . && git commit -m 'Address validation feedback'"
echo "  git checkout master && git merge $CURRENT_BRANCH"
echo "  git push origin master"

exit 0
