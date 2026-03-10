# Script de Configuración de WSL2 para Proyecto ML Data
# Ejecutar como Administrador en PowerShell

Write-Host "1. Verificando/Instalando WSL..." -ForegroundColor Cyan
wsl --install -d Ubuntu

Write-Host "2. Preparando migración de archivos..." -ForegroundColor Cyan
$wslPath = "\\wsl$\Ubuntu\home\$env:USERNAME\proyecto_ml_data"
Write-Host "El proyecto deberá copiarse a: $wslPath" -ForegroundColor Yellow

Write-Host "3. Instrucciones de Post-Instalación:" -ForegroundColor Green
Write-Host "   - Abre Ubuntu desde el menú Inicio."
Write-Host "   - Ejecuta: sudo apt update && sudo apt install -y python3-pip python3-venv tree"
Write-Host "   - Copia tu proyecto: cp -r /mnt/c/Users/$env:USERNAME/Documents/proyecto_ml_data ~/ "
