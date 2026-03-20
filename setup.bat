@echo off
echo.
echo ==========================================
echo Configurando el entorno del proyecto...
echo ==========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)

:: Crear entorno virtual si no existe
if not exist .venv (
    echo [+] Creando entorno virtual (.venv)...
    python -m venv .venv
) else (
    echo [!] El entorno virtual ya existe.
)

:: Actualizar pip e instalar dependencias
echo [+] Instalando/Actualizando dependencias...
.venv\Scripts\python -m pip install -U pip setuptools wheel
.venv\Scripts\pip install -r requirements.txt

echo.
echo ==========================================
echo [LISTO] Entorno configurado correctamente.
echo Para activarlo usa: .venv\Scripts\activate
echo ==========================================
echo.
pause
