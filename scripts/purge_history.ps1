param(
  [Parameter(Mandatory=$true)]
  [string]$Target
)

Write-Host "Removing $Target from history..."
# Requires git-filter-repo installed (python -m pip install git-filter-repo)
git filter-repo --invert-paths --path $Target
Write-Host "Done. If you have a remote, run: git push --force --all; git push --force --tags"
