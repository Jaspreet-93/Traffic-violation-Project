# PowerShell script to automatically stage, commit, and push changes to Git

$status = git status --porcelain
$unpushed = git log '@{u}..HEAD' --oneline 2>$null

if ($status -or $null -eq $unpushed -or $unpushed.Length -gt 0) {
    Write-Host "Changes or unpushed commits detected. Syncing with GitHub..." -ForegroundColor Cyan
    
    # Stage all changes
    git add -A
    
    # Create a descriptive commit message if there are staged changes
    $hasStaged = git diff --cached --name-only
    if ($hasStaged) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $commitMessage = "Sync project files - $timestamp"
        git commit -m $commitMessage
    }
    
    # Push to remote repository
    Write-Host "Pushing to remote origin main..." -ForegroundColor Cyan
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully synced with remote repository!" -ForegroundColor Green
    } else {
        Write-Warning "Failed to push to remote repository. Please check your internet connection or git permissions."
    }
} else {
    Write-Host "No changes detected. Repository is up-to-date." -ForegroundColor Green
}
