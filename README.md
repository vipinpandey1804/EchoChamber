# 🎮 Echo Chamber Game

A full-stack maze game with real-time features, power-ups, and leaderboards built with Django and React.

## 🚀 Features

- **Interactive Maze Gameplay**: Navigate through challenging levels
- **Power-Up System**: Speed boost, phase shield, time freeze, and echo vision
- **Real-Time Scoring**: Dynamic score calculation with bonuses and penalties  
- **Progressive Levels**: Increasingly difficult mazes
- **Leaderboard**: Track top scores across all players
- **Echo Mechanics**: Create helpful echoes to guide your path

## 🛠️ Tech Stack

**Backend:**
- Django 4.2+
- Django REST Framework
- WebSocket support with Channels
- SQLite database

**Frontend:**
- React with TypeScript
- Real-time game rendering
- Responsive design

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm

### Backend Setup

```bash
cd backend
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 🎯 How to Play

### Controls
- **Arrow Keys**: Move player
- **Space**: Jump 2 cells forward
- **Enter**: Create helpful echo

### Power-Ups
- **⚡ Yellow**: Speed Boost - Move 2x faster
- **🛡️ Cyan**: Phase Shield - Walk through walls  
- **⏰ Blue**: Time Freeze - Pause echoes
- **🔮 Magenta**: Echo Vision - See future paths

### Scoring
- Start with 1000 points
- -1 point per game tick
- +10 points per echo created
- -5 points per wall collision
- Reach the green exit to win!

## 🏗️ Project Structure

```
game/
├── backend/           # Django API server
│   ├── api/          # API endpoints
│   ├── game/         # Game logic and models
│   ├── users/        # User management
│   └── core/         # Django settings
├── frontend/         # React application
│   ├── src/          # React components
│   └── public/       # Static assets
└── docs/            # Documentation
```

## 🔧 Environment Configuration

Copy `.env.example` files in both `backend/` and `frontend/` directories and configure as needed.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.