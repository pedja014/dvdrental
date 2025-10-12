# Windows Setup Guide - DVD Rental API

## 🪟 Running Docker on Windows Without GUI

You have several options to run this project on Windows using command line instead of Docker Desktop GUI.

## Option 1: Docker Desktop with Command Line (Recommended)

Docker Desktop is still required, but you can control everything from the command line.

### Installation

1. **Install Docker Desktop**:
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and complete the setup
   - Docker Desktop will start automatically

2. **Optional: Disable "Open Dashboard at startup"**:
   - Open Docker Desktop
   - Go to Settings → General
   - Uncheck "Start Docker Desktop when you log in"
   - Uncheck "Open Docker Dashboard at startup"

### Usage with Batch Scripts (Easiest)

We've created convenient batch scripts for you:

```batch
REM First time setup
setup.bat

REM Start the API
start.bat

REM Stop the API
stop.bat

REM View logs
logs.bat

REM Check status
status.bat

REM Restart
restart.bat

REM Reset everything (WARNING: deletes data)
reset.bat
```

### Usage with PowerShell (Recommended)

PowerShell provides better error handling and progress indicators:

```powershell
# First time setup
.\setup.ps1

# Or use docker-compose directly
docker-compose up --build -d
docker-compose logs -f
docker-compose down
```

### Usage from Command Prompt

```batch
REM First time setup
docker-compose up --build -d

REM View logs
docker-compose logs -f

REM Stop
docker-compose down

REM Restart
docker-compose restart

REM Status
docker-compose ps
```

## Option 2: WSL2 with Docker Engine (No Desktop GUI)

If you want to completely avoid Docker Desktop GUI, you can use WSL2.

### Installation

1. **Enable WSL2**:
   ```powershell
   # Run as Administrator
   wsl --install
   # Restart your computer
   ```

2. **Install Ubuntu from Microsoft Store**:
   - Open Microsoft Store
   - Search for "Ubuntu"
   - Install Ubuntu 22.04 LTS

3. **Install Docker Engine in WSL2**:
   ```bash
   # Inside Ubuntu/WSL2
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Add your user to docker group
   sudo usermod -aG docker $USER
   
   # Start Docker
   sudo service docker start
   ```

4. **Install Docker Compose**:
   ```bash
   sudo apt-get update
   sudo apt-get install docker-compose-plugin
   ```

5. **Navigate to your project**:
   ```bash
   # Your Windows drives are at /mnt/
   cd /mnt/e/dvdrental
   
   # Run the project
   docker-compose up --build
   ```

### Access from Windows

Your API will still be accessible from Windows at:
- http://localhost:8000/swagger/
- http://localhost:8000/api/

## Option 3: Rancher Desktop (Docker Desktop Alternative)

Rancher Desktop is a free, open-source alternative to Docker Desktop.

### Installation

1. Download from: https://rancherdesktop.io/
2. Install and select "dockerd (moby)" as the container runtime
3. Use the same commands as Docker Desktop

## Recommended Approach for Your Workflow

### For Quick Development

Use **Option 1** with the batch scripts:

```batch
REM One-time setup
setup.bat

REM Daily use
start.bat   # Start working
logs.bat    # View logs if needed
stop.bat    # When done
```

### For Production-Like Environment

Use **Option 2** (WSL2) for a Linux-like experience:

```bash
# Inside WSL2
cd /mnt/e/dvdrental
docker-compose up -d
docker-compose logs -f web
```

## Docker Commands Cheat Sheet

### Container Management
```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web
docker-compose logs -f db

# Check status
docker-compose ps
```

### Django Management
```bash
# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Access container shell
docker-compose exec web bash
docker-compose exec db psql -U postgres -d dvdrental
```

### Troubleshooting
```bash
# Rebuild containers
docker-compose up --build

# Remove everything and start fresh
docker-compose down -v
docker-compose up --build

# View container resource usage
docker stats

# Inspect container
docker-compose logs web
docker-compose exec web env
```

## Running Without Opening Docker Desktop

### Method 1: Task Scheduler (Windows)

Create a scheduled task to start Docker on boot without opening the GUI:

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start a program
5. Program: `"C:\Program Files\Docker\Docker\Docker Desktop.exe"`
6. Arguments: (leave empty)
7. Conditions: Uncheck "Start only if on AC power"

### Method 2: Startup Script

Create a VBScript to start Docker silently:

```vbscript
' Save as start_docker.vbs in Startup folder
CreateObject("Wscript.Shell").Run "C:\Program Files\Docker\Docker\Docker Desktop.exe", 0, False
```

Add to: `C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

## Environment Setup

### PowerShell Profile (Optional)

Add Docker commands to your PowerShell profile for easier access:

```powershell
# Edit profile
notepad $PROFILE

# Add these functions
function docker-start { docker-compose up -d }
function docker-stop { docker-compose down }
function docker-restart { docker-compose restart }
function docker-logs { docker-compose logs -f }
function docker-status { docker-compose ps }

# Save and reload
. $PROFILE
```

Now you can use:
```powershell
docker-start
docker-logs
docker-stop
```

## Performance Tips for Windows

1. **Use WSL2 backend** (in Docker Desktop settings)
2. **Exclude Docker from Antivirus** scans
3. **Allocate more resources** in Docker Desktop settings:
   - CPU: 4+ cores
   - Memory: 4+ GB
   - Disk: 60+ GB

4. **Store project in WSL2 filesystem** for better performance:
   ```bash
   # Move project to WSL2
   cp -r /mnt/e/dvdrental ~/dvdrental
   cd ~/dvdrental
   docker-compose up
   ```

## Verification

After setup, verify everything works:

```powershell
# Check Docker
docker --version
docker-compose --version

# Check containers
docker ps

# Test API
curl http://localhost:8000/api/

# Or open in browser
start http://localhost:8000/swagger/
```

## Quick Reference

| What you want | Command |
|---------------|---------|
| First time setup | `setup.bat` or `.\setup.ps1` |
| Start API | `start.bat` or `docker-compose up -d` |
| Stop API | `stop.bat` or `docker-compose down` |
| View logs | `logs.bat` or `docker-compose logs -f` |
| Restart API | `restart.bat` or `docker-compose restart` |
| Check status | `status.bat` or `docker-compose ps` |
| Reset everything | `reset.bat` or `docker-compose down -v` |

## Troubleshooting

### "Docker daemon is not running"
```powershell
# Start Docker Desktop manually
& "C:\Program Files\Docker\Docker\Docker Desktop.exe"
# Wait 30 seconds, then try again
```

### "Port 8000 is already in use"
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
# Change "8000:8000" to "8080:8000"
```

### "Cannot connect to database"
```powershell
# Reset everything
docker-compose down -v
docker-compose up --build
```

## Summary

**Best for Windows users**: Use **Option 1** with the provided batch scripts (`setup.bat`, `start.bat`, `stop.bat`). This gives you command-line control without completely removing Docker Desktop, which is the most compatible approach for Windows.

You don't need to interact with the Docker Desktop GUI at all - just let it run in the background and use the command line scripts!


