Set-StrictMode -Version Latest

$ErrorActionPreference = "stop"

$StopWatch = [System.Diagnostics.Stopwatch]::StartNew()

vagrant up

$StopWatch.Stop()

Write-Host -ForegroundColor Green "Elapsed Time:" $StopWatch.Elapsed