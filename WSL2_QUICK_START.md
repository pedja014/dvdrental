# WSL2 Quick Start Guide

## 🚀 Quick Commands

### Open WSL2
```bash
# From Windows PowerShell or CMD
wsl

# Navigate to project
cd /mnt/e/dvdrental
```

### First Time Setup
```bash
# Make sure Docker is running
sudo service docker start

# Build and start containers
docker compose up --build

# Wait 3-5 minutes for:
# - Database download and restore
# - Django migrations
# - Static files collection
```

### Daily Use
```bash
# Start Docker service (if not running)
sudo service docker start

# Start API in background
docker compose up -d

# View logs
docker compose logs -f

# Stop (when done)
docker compose down
```

## 📍 Access Points

From Windows browser:
- **Swagger UI**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/

**Login:**
- Username: `admin`
- Password: `admin123`

## 🔧 Common Commands

```bash
# Check container status
docker compose ps

# Restart services
docker compose restart

# View only web logs
docker compose logs -f web

# Access Django shell
docker compose exec web python manage.py shell

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Access database directly
docker compose exec db psql -U postgres -d dvdrental
```

## 🔄 Rebuild After Changes

```bash
# Stop containers
docker compose down

# Rebuild and start
docker compose up --build
```

## 🆘 Troubleshooting

### Docker not running
```bash
sudo service docker start
```

### Port already in use
```bash
# Find what's using port 8000
sudo netstat -tlnp | grep 8000

# Or change port in docker-compose.yml
```

### Reset everything
```bash
# WARNING: Deletes all data
docker compose down -v
docker compose up --build
```

### View detailed logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs web
docker compose logs db

# Follow logs in real-time
docker compose logs -f
```

## 📂 File Paths

| Location | Path in WSL2 |
|----------|--------------|
| Project directory | `/mnt/e/dvdrental` |
| Windows E: drive | `/mnt/e/` |
| Windows C: drive | `/mnt/c/` |

## 💡 Pro Tips

### Auto-start Docker
Add to `~/.bashrc`:
```bash
# Auto-start Docker if not running
if ! sudo service docker status > /dev/null 2>&1; then
    sudo service docker start > /dev/null 2>&1
fi
```

### Quick alias
Add to `~/.bashrc`:
```bash
alias dvd='cd /mnt/e/dvdrental'
alias dstart='cd /mnt/e/dvdrental && docker compose up -d'
alias dstop='cd /mnt/e/dvdrental && docker compose down'
alias dlogs='cd /mnt/e/dvdrental && docker compose logs -f'
```

Then just use:
```bash
dvd      # Go to project
dstart   # Start API
dlogs    # View logs
dstop    # Stop API
```

## 📖 More Help

- Full documentation: `README.md`
- WSL2 setup: `WINDOWS_GUIDE.md`
- Quick start: `START_HERE.md`

## ✅ Quick Health Check

```bash
# Check everything is working
docker compose ps                    # Should show 2 containers running
curl http://localhost:8000/api/      # Should return JSON
```

---

**Need help?** Check `WINDOWS_GUIDE.md` for detailed WSL2 setup and troubleshooting!

