@echo off
REM Build script for Magic Box - Windows
REM La Boite Magique de Severus Rogue

echo ================================================================
echo.
echo     🧪 LA BOITE MAGIQUE DE SEVERUS ROGUE 🧪
echo                  Build Script
echo.
echo ================================================================
echo.

REM Check for CMake
where cmake >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ CMake is not installed or not in PATH
    echo Please install CMake 3.15 or later
    pause
    exit /b 1
)

echo ✅ CMake found
cmake --version | findstr /C:"cmake version"
echo.

REM Create build directory
echo 📁 Creating build directory...
if not exist build mkdir build
cd build

REM Configure
echo.
echo ⚙️  Configuring project with CMake...
cmake ..
if %ERRORLEVEL% NEQ 0 (
    echo ❌ CMake configuration failed
    pause
    exit /b 1
)

REM Build
echo.
echo 🔨 Building project...
cmake --build . --config Release
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

REM Check if build was successful
if exist bin\Release\magic-box.exe (
    echo.
    echo ✅ Build successful!
    echo.
    echo 📦 Binary location: %CD%\bin\Release\magic-box.exe
    echo.
    echo 🚀 To run the program:
    echo    cd build
    echo    .\bin\Release\magic-box.exe --help
    echo.
) else (
    echo ❌ Build failed - executable not found
    pause
    exit /b 1
)

pause
