# 🚀 Agentic AI Stock Analyzer

An intelligent stock analysis system built with Microsoft Agent Framework and Azure AI Foundry.

## 📋 Current Status - Milestone 1

✅ **Local Stock Price Agent** - Run locally, fetch stock prices using Azure AI Foundry model

## 🏗️ Architecture

- **Local Agent**: Microsoft Agent Framework running locally
- **AI Model**: o3-mini deployed in Azure AI Foundry for ticker extraction
- **Stock Data**: yfinance for real-time stock prices
- **Testing**: pytest with TDD approach

## 🚦 Prerequisites

1. **Python 3.8+**
2. **Azure AI Foundry Account** with deployed model
3. **Azure AI API Key** and endpoint

## ⚙️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/jerryjoseph-net/agentic-ai-stock-analyzer.git
cd agentic-ai-stock-analyzer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure AI Foundry details:
# AZURE_AI_ENDPOINT=https://your-project.aiservices.azure.com
# AZURE_AI_API_KEY=your_api_key_here
# AZURE_AI_MODEL_DEPLOYMENT=o3-mini
```

## 🎯 Usage


### Interactive Mode (Recommended)
```powershell
.venv\Scripts\python.exe src\main.py
```

### Single Query Mode (Recommended)
```powershell
.venv\Scripts\python.exe src\main.py "What's the price of Tesla?"
```

### Example Queries
- "What's the price of Tesla?"
- "How much is Apple stock?"
- "NVIDIA current price"
- "Microsoft shares today"

## 🧪 Testing

Run all tests directly using the virtual environment's Python executable:
```powershell
# Run all tests
.venv\Scripts\python.exe -m pytest tests/

# Run only unit tests (mocked dependencies)
.venv\Scripts\python.exe -m pytest tests/unit/

# Run only integration tests (component interaction)
.venv\Scripts\python.exe -m pytest tests/integration/

# Run with coverage
.venv\Scripts\python.exe -m pytest --cov=src tests/

# Run specific test file
.venv\Scripts\python.exe -m pytest tests/unit/test_stock_agent.py -v
```

## 📁 Project Structure

```
agentic-ai-stock-analyzer/
├── src/
│   ├── agents/
│   │   └── stock_agent.py          # 📈 Stock price fetching agent
│   ├── utils/
│   │   ├── config.py               # ⚙️ Configuration management
│   │   ├── api_clients.py          # 🌐 Azure AI client setup
│   │   └── exceptions.py           # 🚫 Custom exceptions
│   └── main.py                     # 🎯 CLI interface
├── tests/
│   ├── conftest.py                 # 🔧 Pytest configuration
│   ├── unit/                       # 🧪 Unit tests (mocked dependencies)
│   │   ├── __init__.py
│   │   └── test_stock_agent.py     # 📈 Stock agent unit tests
│   └── integration/                # � Integration tests (component interaction)
│       ├── __init__.py
│       ├── test_azure_integration.py  # 🤖 Azure AI integration tests
│       └── test_integration.py     # 🔄 General integration tests
├── requirements.txt                # 🐍 Dependencies
├── .env.example                    # 🔒 Environment template
└── IMPLEMENTATION_PLAN.md          # ⭐ Development roadmap
```

## 🔄 Development Workflow

This project follows strict development practices:

1. **Feature Branches**: `feature/feature-name`
2. **Test-Driven Development**: Write tests first
3. **Quality Gates**: All tests must pass before commits
4. **No direct commits to main**: Use feature branches and PRs

## 🎯 Current Milestone Features

- ✅ Microsoft Agent Framework integration
- ✅ Azure AI Foundry model connection
- ✅ Natural language ticker extraction
- ✅ Real-time stock price fetching
- ✅ CLI interface (interactive and single query)
- ✅ Comprehensive unit and integration testing
- ✅ Organized test structure (unit/integration folders)
- ✅ Error handling and logging

## 🔮 Next Milestones

- **Milestone 2**: Deploy agent to Azure AI Foundry
- **Milestone 3**: Multi-agent setup with currency conversion
- **Milestone 4**: RAG integration with personal watchlist
- **Milestone 5**: Reporting agent for summaries

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Azure AI Errors**: Check your .env configuration
3. **Stock Data Errors**: yfinance may have rate limits

### Getting Help

Check the logs for detailed error messages:
```powershell
.venv\Scripts\python.exe src\main.py 2>&1 | Tee-Object app.log
```

## 📄 License

MIT License