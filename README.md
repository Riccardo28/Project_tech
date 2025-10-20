# Tech News Hub

A modern, full-stack web application for aggregating technology news from Hacker News, Reddit communities (r/ExperiencedDevs, r/ArtificialIntelligence, r/LLMDevs, r/LocalLLaMA, r/automation, and architecture subreddits), and other tech sources.

![Tech News Hub](https://img.shields.io/badge/React-18.x-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg) ![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)

## Features

- 🔍 **Search Functionality** - Search through news articles by title or content
- 🏷️ **Category Filtering** - Filter by LLM Models, Automation Tools, Architecture, Hacker News, or Experienced Devs
- 📰 **Real-time News** - Fetches live data from Hacker News API and Reddit RSS feeds
- 💬 **Article Modal** - Click articles to view full content in a beautiful modal popup
- 🎨 **Modern Dark Theme** - Eye-friendly design with gradient accents
- 📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile
- ⚡ **Interactive UI** - Smooth transitions and hover effects

## Tech Stack

### Frontend
- **React 18** - Frontend framework
- **Lucide React** - Icon library
- **Tailwind CSS** - Styling
- **Vite** - Build tool

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client for API calls
- **feedparser** - RSS feed parsing

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python 3.9 or higher
- npm or yarn
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/tech-news-hub.git
cd Project_tech
```

2. Install frontend dependencies
```bash
npm install
```

3. Install backend dependencies
```bash
npm run backend:install
# Or manually:
cd backend && pip install -r requirements.txt
```

4. (Optional) Configure environment variables
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application

**Start both frontend and backend with one command:**
```bash
npm run dev
```

This will start:
- Frontend (React + Vite) on `http://localhost:5173`
- Backend (FastAPI) on `http://localhost:8000`

**Or run them separately:**

Frontend only:
```bash
npm run dev:frontend
```

Backend only:
```bash
npm run dev:backend
```

5. Open your browser and visit `http://localhost:5173`

## Project Structure

```
Project_tech/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/      # API endpoints
│   │   ├── core/            # Configuration
│   │   ├── models/          # Data models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── src/                      # React frontend
│   ├── components/
│   │   └── TechNewsHub.jsx  # Main component
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /` - API welcome message
- `GET /health` - Health check endpoint
- `GET /api/v1/hacker-news/` - Fetch Hacker News articles
  - Query params: `limit` (default: 20), `story_type` (topstories, newstories, beststories)
- `GET /api/v1/rss/` - Fetch RSS feed articles
  - Query params: `url` (RSS feed URL), `limit` (default: 20)
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Future Enhancements

- [ ] Real-time news aggregation from multiple sources
- [ ] User authentication and personalized feeds
- [ ] Bookmark/favorite articles
- [ ] Dark/light theme toggle
- [ ] RSS feed integration
- [ ] Social media sharing
- [ ] Comments and discussions
- [ ] Advanced filtering options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License


## Contact



## Acknowledgments

- [Lucide Icons](https://lucide.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React](https://react.dev/)