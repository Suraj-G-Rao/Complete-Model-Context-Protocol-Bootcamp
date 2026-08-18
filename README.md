<div align="center">

# 🤖 Complete Model Context Protocol (MCP) Bootcamp

### *From Zero to Production — Build Real-World AI Agents with MCP*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-MCP-FF6B35?style=for-the-badge&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

> **A hands-on, project-based bootcamp covering everything you need to master the Model Context Protocol — from fundamentals to full-stack production-ready AI agents.**

<br/>

[🚀 Get Started](#-getting-started) • [📚 Modules](#-course-modules) • [🛠️ Tech Stack](#️-tech-stack) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 What is Model Context Protocol (MCP)?

**Model Context Protocol (MCP)** is an open standard introduced by Anthropic that defines how AI models communicate with external tools, data sources, and services. Think of it as the **"USB standard for AI"** — it provides a universal plug-and-play interface that lets any LLM connect to any tool or data source without custom integrations.

### Why MCP Matters

| Without MCP | With MCP |
|---|---|
| Custom integration code for every tool | Universal protocol — write once, connect anywhere |
| Tightly coupled LLM + tool logic | Clean separation of concerns |
| Hard to swap AI providers | Swap Claude, Gemini, GPT easily |
| No standard discovery mechanism | Automatic tool discovery & capability advertising |

---

## 📚 Course Modules

This bootcamp is structured as **16 progressive modules**, each building on the last — from core concepts to production-ready, multi-agent systems.

---

### 📖 01 — Introduction to MCP

> **Foundation** | Conceptual Overview

Understand the architecture of MCP from the ground up. This module covers:
- What MCP is and the problem it solves
- The MCP **Client ↔ Server** communication model
- Transport layers: **stdio** vs **SSE** (Server-Sent Events)
- MCP primitives: **Tools**, **Resources**, and **Prompts**
- How MCP differs from traditional REST API integrations

📄 Includes a comprehensive PDF reference guide.

---

### 🖥️ 02 — Build MCP Server with Claude Desktop

> **Beginner** | Python · FastMCP · Claude Desktop

Build your first real MCP server and connect it directly to **Claude Desktop**. This module walks through:
- Setting up a Python MCP server using `FastMCP`
- Building a **Terminal Server** — let Claude execute shell commands on your machine
- Configuring `claude_desktop_config.json` for local MCP server registration
- Understanding the stdio transport layer in practice

```python
# Your first MCP tool
@mcp.tool()
async def run_command(command: str) -> str:
    """Run a terminal command inside the workspace directory."""
    ...
```

📁 `terminal_server/` · `claude_desktop_config.json`

---

### 🖱️ 03 — Cursor IDE MCP Server Setup

> **Beginner** | Python · FastMCP · Cursor IDE

Connect your MCP server to **Cursor IDE** and supercharge your coding workflow:
- Registering MCP servers inside Cursor's settings
- Reusing the terminal server pattern with Cursor's AI assistant
- Understanding how IDEs consume MCP tools natively
- Best practices for scoping tools to development workflows

📁 `terminal_server/src/`

---

### 💎 04 — Build Your Own MCP Client using Google Gemini API

> **Intermediate** | Python · Google Gemini API · Custom MCP Client

Move beyond Claude Desktop — build a **fully custom MCP client** powered by the **Google Gemini API**:
- Implementing the MCP client protocol from scratch
- Connecting to any MCP server programmatically
- Integrating **Gemini's function calling** with MCP tool schemas
- Building a conversational loop that routes tool calls through MCP
- Managing session lifecycle and tool result passing

📁 `mcp-client/client.py`

---

### 🐳 05 — How to Build a Docker MCP Server

> **Intermediate** | Docker · Python · Containerization

Package and deploy your MCP server as a **Docker container** for portability and reproducibility:
- Writing a production-ready `Dockerfile` for an MCP server
- Configuring Claude Desktop to connect to a **containerized MCP server**
- Managing environment variables and volumes in Docker
- WSL2 setup for Windows users running Docker-based MCP servers

```dockerfile
# Containerized MCP server
FROM python:3.11-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "terminal_server.py"]
```

📁 `terminal_server/` · `Dockerfile` · `claude_desktop_config.json`

---

### 🦜 06 — LangChain MCP Client using LangChain MCP Adapters

> **Intermediate** | LangChain · Python · MCP Adapters

Integrate MCP tools into the **LangChain** ecosystem using official MCP adapters:
- Using `langchain-mcp-adapters` to wrap MCP tools as LangChain tools
- Building a **ReAct agent** that reasons over MCP-powered capabilities
- Connecting to multiple MCP servers simultaneously from a LangChain chain
- Streaming agent responses with tool invocations

```python
from langchain_mcp_adapters.tools import load_mcp_tools
tools = await load_mcp_tools(session)
agent = create_react_agent(model, tools)
```

📁 `mcp-clients/lanchain_mcp_client.py`

---

### 🔗 07 — MCP Client with Multiple Server Support

> **Intermediate** | Python · LangChain · Multi-Server Architecture

Scale your MCP setup by connecting a **single client to multiple servers**:
- Loading server configurations from a `config.json` file
- Managing concurrent connections to multiple MCP servers
- Tool namespace management to avoid naming collisions
- Building robust error handling for multi-server environments
- Dynamic server discovery and tool aggregation

```json
{
  "servers": {
    "terminal": { "command": "python", "args": ["server.py"] },
    "weather": { "command": "python", "args": ["weather_server.py"] }
  }
}
```

📁 `mcp-client/langchain_mcp_client_wconfig.py` · `config.json`

---

### 📡 08 — MCP Server and Client using SSE

> **Intermediate** | Python · SSE Transport · HTTP

Switch from stdio to **Server-Sent Events (SSE)** transport for network-based MCP communication:
- Building an HTTP-based MCP server with SSE streaming
- Writing an MCP client that connects over HTTP instead of stdio
- When to use SSE vs stdio transport
- Deploying SSE-based MCP servers behind a reverse proxy
- Docker deployment of SSE-based servers

📁 `servers/terminal_server/sse_server/` · `clients/mcp_client/`

---

### 🌦️ 09 — Real-Time Weather Agent using MCP and MCP Inspector

> **Intermediate** | Python · FastMCP · External APIs · MCP Inspector

Build a production-style **real-time weather agent** and debug it with the official MCP Inspector tool:
- Integrating a live weather API as an MCP tool
- Structuring tools in a modular `tools/` package
- Using the **MCP Inspector** to visually test and debug your server
- Best practices for API key management in MCP tools

```python
@mcp.tool()
async def get_weather(city: str) -> dict:
    """Fetch real-time weather data for a given city."""
    ...
```

📁 `tools/weather.py` · `main.py`

---

### 💼 10 — Real-Time Job Recommendation System

> **Advanced** | Python · FastMCP · LangChain · Streamlit · Job APIs

A full-stack **AI-powered job recommendation agent** built on MCP:
- MCP server exposing live job listing APIs as tools
- LangChain agent that understands user profiles and recommends relevant jobs
- **Streamlit** frontend for an interactive user experience
- Structured output parsing and ranking logic
- Clean separation between MCP server (`mcp_server.py`) and agent logic (`app.py`)

📁 `app.py` · `mcp_server.py` · `src/job_api.py` · `src/helper.py`

---

### 📖 11 — StoryForge Agent

> **Advanced** | Python · FastMCP · LangChain · Streamlit · Generative AI

An end-to-end **AI creative writing agent** that generates rich, structured stories:
- MCP server with story-generation tools (plot, characters, dialogue)
- Multi-step agent pipeline: outline → draft → refine
- **Streamlit** web interface for interactive story creation
- Demonstrates long-form content generation with MCP tools
- Extensible tool design for adding new creative capabilities

📁 `app.py` · `mcp_server.py` · `main.py`

---

### 🏥 12 — Clinisight — Clinical AI Assistant

> **Advanced** | Python · FastMCP · PubMed API · LangChain · Medical NLP

A specialized **clinical intelligence agent** for medical research and symptom analysis:
- MCP tools for PubMed article retrieval and summarization
- Symptom extraction from natural language clinical notes
- AI-powered differential diagnosis suggestions
- Integration with biomedical literature APIs
- Jupyter notebook for exploratory clinical data analysis

```
Tools: symptom_extractor · pubmed_search · summarize_article · differential_diagnosis
```

📁 `functions/` · `mcp_tool.py` · `app.py` · `demo.ipynb`

---

### 🤖 13 — ADK Multi-Agent Demo

> **Advanced** | Google ADK · Multi-Agent Systems

Explore **Google's Agent Development Kit (ADK)** for orchestrating multiple specialized agents:
- Building a multi-agent system where agents collaborate on tasks
- Agent-to-agent communication patterns
- Orchestration strategies: sequential, parallel, and hierarchical
- Integrating ADK agents with external MCP tools

📁 `muli_agent/agent.py`

---

### ✈️ 14 — TripMate-AI

> **Advanced** | Python · Flask · LangChain · Flight APIs · Tavily Search

A full-stack **AI travel planning assistant** with a beautiful web interface:
- Flask web application with custom HTML/CSS/JS frontend
- Real-time flight search integration
- Tavily search tools for destination research
- Multi-turn conversational travel planning
- Dockerized for easy deployment

📁 `app.py` · `backend.py` · `tools/` · `templates/` · `static/` · `Dockerfile`

---

### ✈️🔌 15 — TripMate-AI Using MCP

> **Advanced** | Python · MCP · Flask · Custom Weather MCP Server

The **MCP-powered evolution of TripMate-AI** — refactored to use MCP as the tool integration layer:
- Custom **Weather MCP Server** (`custom_weather_mcp_server.py`)
- MCP Client managing server connections from the backend
- Decoupled architecture: frontend → Flask → MCP Client → MCP Servers
- Demonstrates real-world migration from direct API calls to MCP
- Full Docker support for production deployment

```
Architecture: Browser → Flask App → MCP Client → [Weather MCP Server, Flight Tools, Search Tools]
```

📁 `mcp_client.py` · `custom_weather_mcp_server.py` · `backend.py` · `Dockerfile`

---

### ✍️ 16 — AgentWriter-AI

> **Advanced** | Python · LangChain · Google Gemini · DALL-E · Flask

A sophisticated **AI blog writing agent** with image generation capabilities:
- Multi-stage writing pipeline: research → outline → draft → polish
- **DALL-E image generation** integrated into blog posts
- Web scraping and Tavily research for factual grounding
- Beautiful **Flask web frontend** for article creation
- Jupyter notebooks documenting each stage of agent evolution

```
Pipeline: Topic → Research → Outline → Draft → Image Generation → Final Blog Post
```

📁 `app.py` · `backend.py` · `notebooks/` · `static/` · `templates/`

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **AI / LLM** | Google Gemini API, Anthropic Claude, OpenAI GPT |
| **MCP Framework** | `mcp`, `FastMCP`, `langchain-mcp-adapters` |
| **Agent Frameworks** | LangChain, LangGraph, Google ADK |
| **Web Frameworks** | Flask, Streamlit |
| **Containerization** | Docker, Docker Compose |
| **Package Management** | `uv`, `pip` |
| **External APIs** | OpenWeatherMap, Tavily Search, PubMed, Job APIs |
| **Transport Layers** | stdio, SSE (Server-Sent Events) |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.11+**
- **Git**
- **Docker** (for containerized projects)
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

### Clone the Repository

```bash
git clone https://github.com/Suraj-G-Rao/Complete-Model-Context-Protocol-MCP-.git
cd Complete-Model-Context-Protocol-MCP-
```

### Setting Up a Project

Each module is self-contained. Navigate to any folder and follow these steps:

**Using `uv` (recommended):**
```bash
cd "04-Build Your Own MCP Client using Google Gemini API/mcp-client"
uv sync
cp .env.example .env   # Add your API keys
uv run python client.py
```

**Using `pip`:**
```bash
cd "04-Build Your Own MCP Client using Google Gemini API/mcp-client"
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
python client.py
```

### Environment Variables

Each project that requires API keys includes a `.env.example` file. Common variables:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

---

## 📂 Repository Structure

```
Complete-Model-Context-Protocol-MCP-/
│
├── 01-Introduction to MCP/               # 📖 MCP concepts & PDF guide
├── 02-Build MCP Server with Claude Desktop/  # 🖥️ First MCP server + Claude Desktop
├── 03-Cursor IDE MCP Server Setup/       # 🖱️ MCP in Cursor IDE
├── 04-Build Your Own MCP Client.../      # 💎 Custom Gemini-powered MCP client
├── 05-How to build Docker MCP Server/    # 🐳 Dockerized MCP server
├── 06-Langchain MCP Client.../           # 🦜 LangChain + MCP adapters
├── 07-MCP Client with Multiple Server.../# 🔗 Multi-server MCP client
├── 08-MCP Server and Client using SSE/   # 📡 SSE transport layer
├── 09-Real Time Weather Agent.../        # 🌦️ Weather agent + MCP Inspector
├── 10-Real Time Job Recommendation.../   # 💼 Full-stack job recommender
├── 11-StoryForge Agent/                  # 📖 AI creative writing agent
├── 12-Clinisight/                        # 🏥 Clinical AI assistant
├── 13-ADK demo/                          # 🤖 Google ADK multi-agent
├── 14-TripMate-AI/                       # ✈️ Travel planner web app
├── 15-TripMate-AI Using MCP/             # ✈️🔌 MCP-powered travel planner
├── 16-AgentWriter-AI/                    # ✍️ AI blog writing agent
│
├── .gitignore
└── README.md
```

---

## 🗺️ Learning Path

```
Beginner ─────────────────────────────────────────────────────► Advanced
   │                                                                  │
  [01]        [02] [03]       [04] [05]        [06] [07] [08]        │
 Concepts   First Server   Custom Client    LangChain & Docker        │
                │                │                  │                 │
               [09]            [10]       [11] [12] [13]     [14][15][16]
           Weather Agent   Job Rec.   Full-Stack Agents   Production Apps
```

---

## 🤝 Contributing

Contributions are welcome! If you find a bug, want to improve documentation, or add a new module:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⭐ If this bootcamp helped you, give it a star!

**Built with ❤️ to help developers master the future of AI tool integration**

</div>