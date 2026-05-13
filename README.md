# AI Travel Itinerary Planner

An intelligent travel planning application powered by Claude AI and real-time web search. Enter your destination and preferences, and the agent generates a detailed day-by-day itinerary tailored to your travel style.

## How It Works

The app uses a [ReAct](https://arxiv.org/abs/2210.03629) (Reason + Act) agent built on LangGraph:

1. User submits travel parameters via the Streamlit UI
2. The `TravelPlanner` constructs a detailed prompt with user preferences
3. Claude Sonnet 4.6 reasons over the request and invokes search tools (Tavily, Serper) to gather current travel information
4. The agent synthesizes the research into a structured, day-by-day itinerary
5. Results are displayed in the web UI

## Features

- Day-by-day itineraries with activities, dining, and travel tips
- Real-time web search for up-to-date recommendations
- Configurable pace (slow/moderate/fast), budget style, and interests
- Observability via Logfire tracing
- Log aggregation with ELK Stack (Elasticsearch, Logstash, Kibana, Filebeat)
- Docker and Kubernetes ready

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude Sonnet 4.6 (Anthropic) |
| Agent Framework | LangGraph + LangChain |
| Web UI | Streamlit |
| Search | Tavily Search API, Google Serper API |
| Observability | Logfire |
| Logging | ELK Stack (on Kubernetes) |
| Containerization | Docker + Kubernetes |

## Prerequisites

- Python 3.11+
- API keys: [Anthropic](https://console.anthropic.com), [Tavily](https://tavily.com), [Serper](https://serper.dev), [Logfire](https://logfire.pydantic.dev)

## Local Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd "AI Travel Itinerary"

# 2. Create and activate a virtual environment
python3 -m venv travenv
source travenv/bin/activate

# 3. Install the package
pip install -e .

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in your API keys
```

**.env file:**
```
ANTHROPIC_API_KEY=your_anthropic_key
TAVILY_API_KEY=your_tavily_key
SERPER_API_KEY=your_serper_key
LOGFIRE_TOKEN=your_logfire_token
```

```bash
# 5. Run the app
streamlit run app.py
# Opens at http://localhost:8501
```

## Docker

```bash
# Build
docker build -t ai-travel-itinerary:latest .

# Run
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY="..." \
  -e TAVILY_API_KEY="..." \
  -e SERPER_API_KEY="..." \
  -e LOGFIRE_TOKEN="..." \
  ai-travel-itinerary:latest
```

## Kubernetes

```bash
# Deploy the application
kubectl apply -f k8s-deployment.yaml

# Deploy ELK Stack for log aggregation
kubectl apply -f elasticsearch.yaml
kubectl apply -f logstash.yaml
kubectl apply -f filebeat.yaml
kubectl apply -f kibana.yaml

# Access Kibana dashboard
# http://<node-ip>:30601
```

Log flow: **App → Filebeat → Logstash → Elasticsearch → Kibana**

## Project Structure

```
.
├── app.py                    # Streamlit entry point
├── src/
│   ├── agents/
│   │   └── travel_agent.py   # ReAct agent (Claude Sonnet 4.6 + tools)
│   ├── core/
│   │   └── planner.py        # TravelPlanner orchestrator
│   ├── tools/
│   │   ├── tavily_tool.py    # Tavily search tool
│   │   └── serper_tool.py    # Serper search tool
│   ├── models/
│   │   └── travel_models.py  # Pydantic models (Activity, DayPlan, TravelPlan)
│   ├── config/
│   │   └── config.py         # API key loading
│   └── utils/
│       ├── logger.py         # Daily log files
│       ├── tavily_helper.py  # Tavily wrapper with Logfire tracing
│       └── custom_exception.py
├── tests/
│   ├── eval_dataset.py       # Test cases (Paris, Tokyo, Mumbai, Kerala)
│   ├── create_gold_data.py   # Gold standard generation
│   └── gold_standard.json    # Evaluation baseline
├── k8s-deployment.yaml
├── elasticsearch.yaml
├── logstash.yaml
├── filebeat.yaml
├── kibana.yaml
├── Dockerfile
└── requirements.txt
```

## Evaluation

The `tests/` directory contains an evaluation framework using DeepEval:

```bash
# Generate gold standard data
python tests/create_gold_data.py

# Run evaluation against test cases (Paris, Tokyo, Mumbai, Kerala)
python tests/evaluate_trips.py
```

## Configuration Notes

- **Model temperature**: 0.3 (deterministic, consistent itineraries)
- **Search results**: Up to 5 per Tavily query
- **Content truncation**: 800 characters per result to manage token usage
- **Logs**: Written daily to `logs/log_YYYY-MM-DD.log`
