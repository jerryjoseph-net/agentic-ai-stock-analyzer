
# Agentic AI Stock Analyzer Architecture

## Summary
Multi-agent system with an orchestrator agent coordinating stock and currency agents, integrating RAG (watchlist) and external APIs.

## Diagram
```
		      ┌─────────────────────────┐
		      │     User / Frontend     │
		      └────────────┬────────────┘
				           │
				           ▼
		    ┌─────────────────────────────┐
		    │    StockAnalyzerAgent       │
		    │  (acts as orchestrator)     │
		    │─────────────────────────────│
		    │ • Parse intent              │
		    │ • Call StockAgent,          │
		    │   CurrencyAgent, RAG        │
		    │ • Combine responses         │
		    │-----------------------------│
		    │ Tools:                      │
		    │ • Agent-to-Agent Calls      │
		    │ • Logging / Telemetry       │
		    └───┬─────────────────┬───────┘
			    │                 │
			    ▼                 ▼
	┌─────────────────┐      ┌────────────────┐
	│  StockAgent     │      │ CurrencyAgent  │
	│─────────────────│      │────────────────│
	│ • Extract ticker│      │ • Fetch rate   │
	│ • Get USD price │      │ • Convert amt  │
	│-----------------│      │----------------│
	│ Tools:          │      │ Tools:         │
	│ • yfinance API  │      │ • FX API       │
	│ • Ticker map    │      │ • Cache store  │
	│ • Regex / LLM   │      │ • Math engine  │
	└───────┬─────────┘      └──────┬─────────┘
		    │                       │
		    ▼                       ▼
	┌─────────────────┐      ┌────────────────┐
	│ yfinance / API  │      │ FX API (ECB,   │
	│  (live prices)  │      │ exchangerate)  │
	└─────────────────┘      └────────────────┘

			    ▲
			    │
		┌────────────────────────────┐
		│ Watchlist / RAG Service    │
		│ (Azure AI Search / FAISS)  │
		│ Tools: embeddings, vectors │
		└────────────────────────────┘
```
