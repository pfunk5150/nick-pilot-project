# =============================================================================
# Nick Pilot Project - Automated Cleanup Script (PowerShell)
# =============================================================================
# Purpose: Automate file organization and Git branch setup
# Usage: ./scripts/cleanup-project.ps1
# =============================================================================

Write-Host '🚀 Starting Nick Pilot Project Cleanup...' -ForegroundColor Green
Write-Host '=========================================' -ForegroundColor Green

# -----------------------------------------------------------------------------
# Step 1: Create Archive Directory Structure
# -----------------------------------------------------------------------------
Write-Host '📁 Creating archive directories...' -ForegroundColor Yellow

$archiveDir = 'logs\archived-sessions'
if (!(Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
    Write-Host "✅ Created: $archiveDir" -ForegroundColor Green
}
else {
    Write-Host "ℹ️  Already exists: $archiveDir" -ForegroundColor Cyan
}

$experimentalDir = 'experimental'
if (!(Test-Path $experimentalDir)) {
    New-Item -ItemType Directory -Path $experimentalDir -Force | Out-Null
    Write-Host "✅ Created: $experimentalDir" -ForegroundColor Green
}
else {
    Write-Host "ℹ️  Already exists: $experimentalDir" -ForegroundColor Cyan
}

# -----------------------------------------------------------------------------
# Step 2: Archive Session Files
# -----------------------------------------------------------------------------
Write-Host '📦 Archiving session files...' -ForegroundColor Yellow

$sessionFiles = @(
    'export-claude-thread_PRIME-Initialization-Protocol_2025-06-20T06_38_45.784Z.md',
    'conversion_guide.md',
    'article_version_comparison.py',
    'executive_summary_comparison.md',
    'change_summary.md',
    'progressive_diff.md'
)

foreach ($file in $sessionFiles) {
    if (Test-Path $file) {
        Move-Item $file $archiveDir -Force
        Write-Host "✅ Archived: $file" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Not found: $file" -ForegroundColor Yellow
    }
}

# -----------------------------------------------------------------------------
# Step 3: Identify Experimental Files for Isolation
# -----------------------------------------------------------------------------
Write-Host '🧪 Preparing experimental files for isolation...' -ForegroundColor Yellow

$experimentalFiles = @(
    'chat_conversion_script.py',
    'chat_converter.py',
    'optimized_chat_context.json',
    'example_optimized_output.json'
)

Write-Host 'Files to isolate to experimental branch:' -ForegroundColor Cyan
foreach ($file in $experimentalFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ $file (not found)" -ForegroundColor Red
    }
}

# -----------------------------------------------------------------------------
# Step 4: Git Operations (if Git is available)
# -----------------------------------------------------------------------------
Write-Host '🔧 Attempting Git operations...' -ForegroundColor Yellow

try {
    # Check if we're in a Git repository
    $gitStatus = git status --porcelain 2>$null

    if ($LASTEXITCODE -eq 0) {
        Write-Host '✅ Git repository detected' -ForegroundColor Green

        # Add new documentation files
        git add 'GIT_WORKFLOW.md' 'PHASE1_COMPLETION_REPORT.md' 'scripts/cleanup-project.ps1' 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host '✅ Added documentation files to Git' -ForegroundColor Green
        }

        # Create experimental branch and isolate files
        Write-Host '🌿 Creating experimental branch...' -ForegroundColor Yellow
        git checkout -b experimental/thread-condensing 2>$null

        if ($LASTEXITCODE -eq 0) {
            Write-Host '✅ Created experimental/thread-condensing branch' -ForegroundColor Green

            # Add experimental files to this branch
            foreach ($file in $experimentalFiles) {
                if (Test-Path $file) {
                    git add $file 2>$null
                }
            }

            git commit -m '🧪 Isolate experimental thread condensing scripts' 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host '✅ Committed experimental files' -ForegroundColor Green
            }

            # Return to main branch
            git checkout main 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host '✅ Returned to main branch' -ForegroundColor Green
            }

            # Remove experimental files from main branch
            foreach ($file in $experimentalFiles) {
                if (Test-Path $file) {
                    Remove-Item $file -Force
                    Write-Host "✅ Removed $file from main branch" -ForegroundColor Green
                }
            }
        }

    }
    else {
        Write-Host '⚠️  Not a Git repository - skipping Git operations' -ForegroundColor Yellow
    }

}
catch {
    Write-Host "⚠️  Git operations failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# -----------------------------------------------------------------------------
# Step 5: Validation Report
# -----------------------------------------------------------------------------
Write-Host '📊 Cleanup Validation Report' -ForegroundColor Magenta
Write-Host '=============================' -ForegroundColor Magenta

Write-Host 'Archive Directory:' -ForegroundColor Cyan
if (Test-Path $archiveDir) {
    $archivedFiles = Get-ChildItem $archiveDir
    Write-Host "  📁 $archiveDir ($($archivedFiles.Count) files)" -ForegroundColor Green
    foreach ($file in $archivedFiles) {
        Write-Host "    📄 $($file.Name)" -ForegroundColor Gray
    }
}
else {
    Write-Host '  ❌ Archive directory not created' -ForegroundColor Red
}

Write-Host "`nRoot Directory Status:" -ForegroundColor Cyan
$rootFiles = Get-ChildItem -File | Where-Object { $_.Extension -eq '.py' -or $_.Extension -eq '.json' -or $_.Extension -eq '.md' }
foreach ($file in $rootFiles) {
    if ($file.Name -in $experimentalFiles) {
        Write-Host "  🧪 $($file.Name) (experimental - should be isolated)" -ForegroundColor Yellow
    }
    elseif ($file.Name -in $sessionFiles) {
        Write-Host "  📦 $($file.Name) (session file - should be archived)" -ForegroundColor Yellow
    }
    else {
        Write-Host "  ✅ $($file.Name) (core project file)" -ForegroundColor Green
    }
}

Write-Host "`n🎉 Cleanup Process Complete!" -ForegroundColor Green
Write-Host 'Next Steps:' -ForegroundColor Cyan
Write-Host '1. Review validation report above' -ForegroundColor White
Write-Host '2. Verify experimental files are isolated' -ForegroundColor White
Write-Host '3. Proceed with Phase 2 preparation' -ForegroundColor White
