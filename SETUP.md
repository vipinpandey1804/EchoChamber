# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm installed

## Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies (if not already installed)
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend will run on: `http://localhost:8000`

## Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies (already in package.json)
npm install

# Start development server
npm start
```

Frontend will run on: `http://localhost:3000`

## Environment Configuration

### Backend (.env) - Optional
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (.env) - Optional
```env
REACT_APP_API_URL=http://localhost:8000
```

## Quick Test

1. Open browser to `http://localhost:3000`
2. Game should load automatically
3. Use arrow keys to move
4. Collect yellow/cyan/blue/magenta power-ups
5. Reach green exit to win
6. Click "Next Level" to progress

## New Features to Test

✅ **Score System**: Watch score update in real-time
✅ **Power-Ups**: Collect glowing circles for abilities
✅ **Levels**: Progress through increasingly difficult mazes
✅ **Leaderboard**: View top scores after winning
✅ **Wall Hits**: Counter tracks collisions

## Troubleshooting

### Backend Issues
- **Port 8000 in use**: Change port with `python manage.py runserver 8001`
- **Migration errors**: Delete `db.sqlite3` and run migrations again
- **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in settings.py

### Frontend Issues
- **Port 3000 in use**: React will prompt to use different port
- **API connection failed**: Verify backend is running on port 8000
- **Build errors**: Delete `node_modules` and run `npm install` again

## Database Reset (if needed)

```bash
cd backend
rm db.sqlite3
rm -rf game/migrations/000*.py  # Keep __init__.py
python manage.py makemigrations
python manage.py migrate
```

## Play Instructions

### Controls
- **↑ ↓ ← →**: Move player
- **Space**: Jump 2 cells forward
- **Enter**: Create helpful echo

### Power-Ups
- **Yellow (⚡)**: Speed Boost - Move 2x faster
- **Cyan (🛡️)**: Phase Shield - Walk through walls
- **Blue (⏰)**: Time Freeze - Pause echoes
- **Magenta (🔮)**: Echo Vision - See future paths

### Scoring
- Base: 1000 points
- -1 per tick
- +10 per echo
- -5 per wall hit

### Win Condition
Reach the green glowing exit portal!

---

**Ready to play! 🎮**
