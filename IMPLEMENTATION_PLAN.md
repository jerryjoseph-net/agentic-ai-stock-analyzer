# 📊 Agentic AI Stock Analyzer — Implementation Plan

This is the high-level implementation roadmap for the 
Agentic AI Stock Analyzer which uses Microsoft Agent Framework.

### 🔁 Progress Legend
- ⏹️ = Task not started
- ✅ = Task completed

> Update ⏹️ to ✅ as tasks are completed. This format is Copilot-readable for roadmap-aware suggestions.

---

## ⏹️ Milestone 1 — Local Stock Price Agent

> Goal: Build agent using Microsoft Agent Framework, run agent locally, fetch stock price using user input.

- ⏹️ Deploy a foundation model (e.g., GPT-4) in Azure AI Foundry
- ⏹️ Configure local agent (Python) to connect to AI Foundry model endpoint
- ⏹️ Accept user query: "What's the price of Tesla?"
- ⏹️ Use AI model to extract ticker or company name from input
- ⏹️ Call stock price API (e.g., `yfinance`, Twelve Data) via agent tools
- ⏹️ Return clean response with current stock price
- ⏹️ Agent runs locally but uses Azure AI Foundry model 

---

## ⏹️ Milestone 2 — Deploy Agent to Azure

> Goal: Move local agent to Azure AI Foundry (Agent Service)

- ⏹️ Package the stock agent code
- ⏹️ Deploy to Azure AI Foundry (single-agent)
- ⏹️ Configure environment + endpoint
- ⏹️ Test via Azure Playground or API
- ⏹️ Optional: expose via web or chat frontend

---

## ⏹️ Milestone 3 — Add Currency Agent + Multi-Agent Setup

> Goal: Convert to SEK using a separate Currency Agent via multi-agent orchestration.

- ⏹️ Build a standalone **Currency Agent** (USD→SEK)
- ⏹️ Register both Stock and Currency agents in Azure AI Foundry
- ⏹️ Enable task handoff between agents
- ⏹️ Test scenario:  
  “What’s the price of NVIDIA in SEK?” →  
  Stock Agent fetches USD price →  
  Currency Agent converts →  
  Combined response returned
- ⏹️ Add trace/logging for cross-agent debugging

---

## ⏹️ Milestone 4 — Add RAG with Watchlist as Grounding

> Goal: Use a personal stock watchlist for retrieval-augmented responses.

- ⏹️ Create `watchlist.json` with 10 stock entries
- ⏹️ Add embeddings using Azure AI Search or FAISS
- ⏹️ Integrate as RAG grounding data
- ⏹️ Agent should answer:
  - “What’s in my watchlist?”
  - “Show prices for all my watchlist stocks”
- ⏹️ Restrict retrieval scope to user’s own watchlist

---

## ⏹️ Milestone 5 — Reporting Agent (Optional)

> Goal: Automatically generate reports based on agent outputs.

- ⏹️ Add Report Agent that orchestrates others
- ⏹️ Collect prices (USD), conversions (SEK), and watchlist context
- ⏹️ Generate Markdown, JSON, or email summaries
- ⏹️ Support scheduled or manual triggering
- ⏹️ Add simple daily summary:  
  “Today’s performance summary for your watchlist”

---