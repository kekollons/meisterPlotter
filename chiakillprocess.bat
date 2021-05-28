@echo off
taskkill /IM chia.exe /F
taskkill /IM start_farmer.exe /F
taskkill /IM start_full_node.exe /F
taskkill /IM start_harvester.exe /F
taskkill /IM start_wallet.exe /F
TIMEOUT /T 3
exit