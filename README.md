# Social Media Dashboard

A modern, full-stack analytics dashboard for social media management with real-time data visualization, post scheduling, and engagement tracking.

## Features

- 📊 **Real-time Analytics**: Interactive D3.js visualizations for engagement metrics
- 📅 **Content Scheduling**: Plan and schedule posts across multiple platforms
- 💬 **Engagement Tracking**: Monitor likes, comments, shares, and reach
- 🚀 **Performance Insights**: Track growth trends and audience demographics
- ⚡ **Redis Caching**: Fast data retrieval and real-time updates
- 🎨 **Modern UI**: Responsive design with Vue.js 3 and Tailwind CSS

## Tech Stack

- **Frontend**: Vue.js 3 (Composition API), Vite, Tailwind CSS, D3.js
- **Backend**: Python FastAPI, Redis, SQLite
- **Visualization**: D3.js for interactive charts
- **State Management**: Pinia
- **API**: RESTful API with WebSocket support

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- Redis server

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd social-media-dashboard
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Start Redis

```bash
# macOS (with Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Or run directly
redis-server
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
social-media-dashboard/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── database.py          # Database configuration
│   ├── redis_client.py      # Redis client setup
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/           # Page views
│   │   ├── stores/          # Pinia stores
│   │   ├── composables/     # Composition functions
│   │   ├── utils/           # Utility functions
│   │   └── assets/          # Static assets
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=sqlite:///./social_media.db
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=your-secret-key-here
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## Features Overview

### Dashboard
- Overview of key metrics across all platforms
- Real-time engagement statistics
- Growth trends visualization

### Analytics
- Interactive charts powered by D3.js
- Platform comparison
- Audience demographics
- Peak engagement times

### Scheduler
- Calendar view for scheduled posts
- Multi-platform posting
- Draft management
- Optimal posting time suggestions

### Engagement
- Recent interactions feed
- Response management
- Sentiment analysis
- Top performing content

## Development

### Backend Development

```bash
# Run tests
pytest

# Format code
black .

# Lint
flake8
```

### Frontend Development

```bash
# Run tests
npm run test

# Lint
npm run lint

# Build for production
npm run build
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
