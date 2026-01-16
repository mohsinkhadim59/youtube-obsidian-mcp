# YouTube Lecture Notes MCP - Installation Script for Windows
# Run this in PowerShell (Admin rights recommended but not required)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YouTube Lecture Notes MCP Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin (needed for some installations)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Note: Running without admin privileges. Some installations may require admin rights." -ForegroundColor Yellow
    Write-Host ""
}

# Function to check if a command exists
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
if (Test-CommandExists python) {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host "    Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "    Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    exit 1
}

# Check FFmpeg
Write-Host "Checking FFmpeg..." -ForegroundColor Yellow
if (Test-CommandExists ffmpeg) {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "  ✓ FFmpeg found" -ForegroundColor Green
} else {
    Write-Host "  ✗ FFmpeg not found. Installing via winget..." -ForegroundColor Yellow
    try {
        winget install ffmpeg --accept-source-agreements --accept-package-agreements
        Write-Host "  ✓ FFmpeg installed" -ForegroundColor Green
    }
    catch {
        Write-Host "  ✗ Could not install FFmpeg automatically." -ForegroundColor Red
        Write-Host "    Please install manually from https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor Red
    }
}

# Install Python packages
Write-Host ""
Write-Host "Installing Python packages..." -ForegroundColor Yellow

Write-Host "  Installing mcp..." -ForegroundColor Gray
pip install mcp --quiet
Write-Host "  ✓ mcp installed" -ForegroundColor Green

Write-Host "  Installing yt-dlp..." -ForegroundColor Gray
pip install yt-dlp --quiet
Write-Host "  ✓ yt-dlp installed" -ForegroundColor Green

# Create MCP server directory
Write-Host ""
Write-Host "Setting up MCP server..." -ForegroundColor Yellow

$mcpDir = "$env:USERPROFILE\mcp-servers\youtube-notes-mcp"
if (-not (Test-Path $mcpDir)) {
    New-Item -ItemType Directory -Path $mcpDir -Force | Out-Null
    Write-Host "  ✓ Created directory: $mcpDir" -ForegroundColor Green
} else {
    Write-Host "  ✓ Directory exists: $mcpDir" -ForegroundColor Green
}

# Check if server.py exists in current directory and copy it
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverSource = Join-Path $scriptDir "server.py"
$serverDest = Join-Path $mcpDir "server.py"

if (Test-Path $serverSource) {
    Copy-Item $serverSource $serverDest -Force
    Write-Host "  ✓ Copied server.py to $mcpDir" -ForegroundColor Green
} else {
    Write-Host "  ! server.py not found in current directory" -ForegroundColor Yellow
    Write-Host "    Please copy server.py to: $mcpDir" -ForegroundColor Yellow
}

# Get Obsidian vault path from user
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$defaultVault = "$env:USERPROFILE\Documents\Obsidian"
Write-Host ""
Write-Host "Enter your Obsidian vault path" -ForegroundColor Yellow
Write-Host "(Press Enter for default: $defaultVault)" -ForegroundColor Gray
$vaultPath = Read-Host "Vault path"

if ([string]::IsNullOrWhiteSpace($vaultPath)) {
    $vaultPath = $defaultVault
}

# Ensure vault path exists
if (-not (Test-Path $vaultPath)) {
    Write-Host "  Creating vault directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $vaultPath -Force | Out-Null
}

# Create Lecture Notes folders
$notesFolder = Join-Path $vaultPath "Lecture Notes"
$imagesFolder = Join-Path $vaultPath "Lecture Notes\images"

if (-not (Test-Path $notesFolder)) {
    New-Item -ItemType Directory -Path $notesFolder -Force | Out-Null
    Write-Host "  ✓ Created: $notesFolder" -ForegroundColor Green
}

if (-not (Test-Path $imagesFolder)) {
    New-Item -ItemType Directory -Path $imagesFolder -Force | Out-Null
    Write-Host "  ✓ Created: $imagesFolder" -ForegroundColor Green
}

# Generate Claude Desktop config
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Claude Desktop Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$serverPathEscaped = $serverDest.Replace('\', '\\')
$vaultPathEscaped = $vaultPath.Replace('\', '\\')

$claudeConfig = @"
{
  "mcpServers": {
    "youtube-notes": {
      "command": "python",
      "args": [
        "$serverPathEscaped"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "$vaultPathEscaped"
      }
    }
  }
}
"@

Write-Host ""
Write-Host "Add this to your Claude Desktop config:" -ForegroundColor Yellow
Write-Host "(Settings > Developer > Edit Config)" -ForegroundColor Gray
Write-Host ""
Write-Host $claudeConfig -ForegroundColor White
Write-Host ""

# Save config to file for reference
$configFile = Join-Path $mcpDir "claude_config_snippet.json"
$claudeConfig | Out-File -FilePath $configFile -Encoding utf8
Write-Host "Config saved to: $configFile" -ForegroundColor Gray

# Final instructions
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Open Claude Desktop" -ForegroundColor White
Write-Host "2. Go to Settings > Developer > Edit Config" -ForegroundColor White
Write-Host "3. Add the configuration shown above" -ForegroundColor White
Write-Host "4. Restart Claude Desktop" -ForegroundColor White
Write-Host ""
Write-Host "Then you can say:" -ForegroundColor Yellow
Write-Host '  "Process this lecture: [YouTube URL]' -ForegroundColor Cyan
Write-Host '   Timestamps: 5:30, 12:00, 25:00' -ForegroundColor Cyan
Write-Host '   Day 1"' -ForegroundColor Cyan
Write-Host ""
Write-Host "Works for any topic: Python, Video Editing, Math, etc!" -ForegroundColor Green
Write-Host ""

# Keep window open
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
