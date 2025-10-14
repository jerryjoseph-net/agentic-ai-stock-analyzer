
# Agentic AI Stock Analyzer Architecture

## Summary
Multi-agent system with an orchestrator agent coordinating stock agent and external APIs. More agents will be added.

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
		    │ • Call StockAgent           │
		    │-----------------------------│
		    │ Tools:                      │
		    │ • Agent-to-Agent Calls      │
		    └───┬─────────────────┬───────┘
			    │         
			    ▼         
	┌───────────────────┐   
	│  StockAgent       │   
	│───────────────────│   
	│ • Extract ticker  │   
	│ • Get USD price   │   
	│-------------------│   
	│ Tools:            │   
	│ • Extract ticker  │   
	│ • yfinance API    │   
	│ • Format response │   
	└───────┬───────────┘   
		    │             
		    ▼             
	┌─────────────────┐   
	│ yfinance / API  │   
	│  (live prices)  │   
	└─────────────────┘   

```
