# test_run.ps1

$Yellow = 'Yellow'
$Green = 'Green'

Write-Host "Running unit tests for API and Agent logic..." -ForegroundColor $Yellow
pytest test_main.py test_agent.py -v

Write-Host ""
Write-Host "Running code coverage (agent.py + main.py)..." -ForegroundColor $Yellow
pytest --cov=agent --cov=main --cov-report=term-missing

Write-Host ""
Write-Host "Unit tests complete." -ForegroundColor $Green
