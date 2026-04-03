# Ruflo News Aggregator

A multi-agent news aggregator application that demonstrates the power of **Ruflo** swarm orchestration.

![Ruflo News Aggregator](https://img.shields.io/badge/Powered%20by-Ruflo-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **Multi-Agent Architecture**: 5 specialized agents working together autonomously
  - **Feeder**: Fetches news from multiple RSS/API sources
  - **Processor**: Extracts entities and classifies content
  - **Sentiment**: Analyzes article sentiment using TextBlob
  - **Summarizer**: Generates concise TL;DR summaries
  - **Publisher**: Formats and delivers results to UI

- **Real-time Processing**: Stream results as agents complete their tasks
- **Multi-source Support**: RSS feeds from TechCrunch, Reuters, Bloomberg, The Verge, Wired
- **Sentiment Analysis**: Positive/negative/neutral classification
- **Keyword Extraction**: Automatic entity and topic extraction
- **No External API Keys**: Uses free RSS feeds (optional NewsAPI support)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --reload

# Open browser
# http://localhost:8000
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    News Aggregator (FastAPI)                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│  │Feeder  │  │Processor│  │Sentiment│  │Summary │  │Publish │
│  └────┬───┘  └────┬───┘  └────┬────┘  └────┬───┘  └────┬───┘
│       │           │           │             │           │
│       └───────────┴───────────┴─────────────┴───────────┘
│                          │
│                  Coordinator (Swarm)
│
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/news` | POST | Aggregate news for a topic |
| `/api/news/{topic}` | GET | Get news for specific topic |
| `/api/status` | GET | Check swarm status |
| `/api/websocket` | WS | Real-time streaming |

### Example Request

```bash
curl -X POST http://localhost:8000/api/news \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI"}'
```

## How It Works

1. **User enters topic** → Swarm Coordinator activates
2. **Feeder agents** → Fetch from multiple RSS sources
3. **Processor agent** → Extract entities, classify content
4. **Sentiment agent** → Analyze article sentiment
5. **Summarizer agent** → Generate TL;DR summaries
6. **Publisher agent** → Format and deliver results

## Multi-Agent Demonstration

This application showcases **Ruflo's** core capabilities:

- ✅ **Autonomous collaboration**: Agents work without manual intervention
- ✅ **Task specialization**: Each agent has focused responsibilities
- ✅ **Parallel execution**: Feeders run concurrently
- ✅ **Pipeline orchestration**: Coordinator manages workflow
- ✅ **Streaming output**: Real-time progress updates

## Tech Stack

- **Backend**: FastAPI (Python)
- **Agents**: Ruflo multi-agent framework
- **News Sources**: RSS feeds (no API keys required)
- **Sentiment**: TextBlob
- **Frontend**: Vanilla HTML/JS

## License

MIT - See [LICENSE](LICENSE) file.
