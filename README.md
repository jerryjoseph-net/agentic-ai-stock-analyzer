# 🚀 Agentic AI Stock Analyzer

An intelligent stock analysis system built with Microsoft Agent Framework and Azure AI Foundry, featuring Infrastructure as Code deployment and automated CI/CD pipelines.


## 📋 Current Features

- **Local Stock Price Agent**: Run locally, fetch stock prices using Azure AI Foundry model
- **Azure Infrastructure**: Bicep templates with standardized naming
- **CI/CD Pipeline**: Automated deployment and validation with GitHub Actions
- **Key Vault Integration**: Secure secret storage
- **Managed Identity**: Secure authentication for Azure resources
- **Application Insights & Log Analytics**: Monitoring and logging

For milestone details and roadmap, see [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)


## 🏗️ Architecture

### Local Development
- **Local Agent**: Microsoft Agent Framework running locally
- **AI Model**: o3-mini deployed in Azure AI Foundry for ticker extraction
- **Stock Data**: yfinance for real-time stock prices
- **Testing**: pytest with TDD approach

### Azure Infrastructure
- **Resource Groups**: Environment-specific with naming convention `<env>-stockanalyzer-rg`
- **Azure AI Foundry**: Existing project integration for model hosting
- **Key Vault**: Secure secret storage for API keys and endpoints
- **Managed Identity**: Secure authentication for Azure resources
- **Application Insights**: Performance monitoring and logging
- **CI/CD Pipeline**: Automated infrastructure deployment and validation


## 🚦 Prerequisites

### Local Development
1. **Python 3.8+**
2. **Azure AI Foundry Account** with deployed model
3. **Azure AI API Key** and endpoint

### Azure Deployment
1. **Azure Subscription** with appropriate permissions
2. **Azure CLI** installed and configured
3. **GitHub Repository** with secrets configured
4. **Existing Azure AI Foundry Project** (referenced in infrastructure)


## ⚙️ Setup

### Local Development Setup

#### 1. Clone Repository
```bash
git clone https://github.com/jerryjoseph-net/agentic-ai-stock-analyzer.git
cd agentic-ai-stock-analyzer
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure AI Foundry details:
# AZURE_AI_ENDPOINT=https://your-project.aiservices.azure.com
# AZURE_AI_API_KEY=your_api_key_here
# AZURE_AI_MODEL_DEPLOYMENT=o3-mini
```

### Azure Deployment Setup

#### 1. Configure GitHub Secrets
In your GitHub repository settings, add these secrets:
```
AZURE_CLIENT_ID=<your-service-principal-client-id>
AZURE_TENANT_ID=<your-azure-tenant-id>  
AZURE_SUBSCRIPTION_ID=<your-azure-subscription-id>
```

#### 2. Infrastructure Deployment
The CI/CD pipeline automatically deploys infrastructure when you push to main or feature branches:
- **Resource Group**: `test-stockanalyzer-rg` (follows naming convention)
- **Key Vault**: `test-stockanalyzer-kv` 
- **Application Insights**: `test-stockanalyzer-ai`
- **Log Analytics**: `test-stockanalyzer-la`
- **Managed Identity**: `test-stockanalyzer-id`

#### 3. Manual Infrastructure Deployment
```bash
# Login to Azure
az login

# Deploy infrastructure (subscription level)
az deployment sub create \
  --location swedencentral \
  --template-file infra/main.bicep \
  --parameters environmentName=test
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
# Run all tests (excluding live)
.venv\Scripts\python.exe -m pytest tests/

# Run all tests (including live)
.venv\Scripts\python.exe -m pytest tests/ --include-live

# Run only unit tests (mocked dependencies)
.venv\Scripts\python.exe -m pytest tests/unit/

# Run only integration tests (excluding live)
.venv\Scripts\python.exe -m pytest tests/integration/

# Run only integration tests (including live)
.venv\Scripts\python.exe -m pytest tests/integration/ --include-live

# Run with coverage
.venv\Scripts\python.exe -m pytest --cov=src tests/

# Run specific test file
.venv\Scripts\python.exe -m pytest tests/unit/test_stock_agent.py -v
```

## 📁 Project Structure

```
agentic-ai-stock-analyzer/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml                  # 🚀 CI/CD pipeline automation  
│   └── .copilot-instructions.md       # 🧠 Development guidelines
├── infra/                             # 🏗️ Infrastructure as Code
│   ├── main.bicep                     
│   ├── modules/
│   │   ├── aifoundry.bicep            
│   │   ├── keyvault.bicep             
│   │   ├── managedidentity.bicep      
│   │   ├── monitoring.bicep           
│   │   └── secrets.bicep              
├── scripts/
│   ├── post-deploy.sh                 # 🔧 Post-deployment configuration
│   └── post-deploy.ps1                # 🔧 PowerShell post-deployment
├── src/
│   ├── agents/                        # 🤖 Agent implementations
│   │   └── stock_agent.py             # 📈 Stock price fetching agent
│   ├── utils/
│   │   ├── config.py                  
│   │   ├── api_clients.py             
│   │   └── exceptions.py              
│   └── main.py                        # 🎯 Application entry point (CLI interface)
├── tests/
│   ├── conftest.py                    # 🔧 Pytest configuration
│   ├── unit/                          # 🧪 Unit tests (mocked dependencies)
│   │   ├── __init__.py
│   │   └── test_stock_agent.py        
│   ├── integration/                   # 🔗 Integration tests 
│   │   ├── __init__.py
│   │   ├── test_azure_integration.py  
│   │   ├── test_azure_live.py         
│   │   └── test_integration.py        
│   └── e2e/                           # 🎯 End-to-end tests
│       └── test_deployed_agent.py     
├── requirements.txt                   # 🐍 Python dependencies
├── pytest.ini                         # 🧪 Pytest configuration
├── .env.example                       # 🔒 Environment template
├── IMPLEMENTATION_PLAN.md             # ⭐ Development roadmap
└── README.md                          # 📖 Project documentation
```

## 🔄 Development Workflow

This project follows strict development practices:

1. **Feature Branches**: `feature/feature-name` (never commit directly to main)
2. **Test-Driven Development**: Write tests first, ensure >80% coverage
3. **Quality Gates**: All tests, linting, and type checking must pass
4. **Infrastructure as Code**: All Azure resources defined in Bicep templates
5. **Automated Deployment**: CI/CD pipeline handles infrastructure and application deployment
6. **Naming Conventions**: All resources follow `<env>-stockanalyzer-<service>` pattern

### CI/CD Pipeline Features
- **Code Quality**: pytest, coverage, flake8, mypy, security scanning
- **Infrastructure Validation**: Bicep template validation and what-if deployment
- **Automated Deployment**: Infrastructure deployment to test environment
- **Post-deployment Configuration**: Automatic secret management setup


## 🚀 Deployment

### Automated Deployment (Recommended)
Push to main or feature branches to trigger automated deployment:
```bash
git push origin feature/your-feature-name
```

The CI/CD pipeline will:
1. Run quality gates (tests, linting, type checking, security scanning)
2. Validate Bicep templates
3. Deploy infrastructure to Azure (test environment)
4. Configure secrets and post-deployment setup

### Manual Deployment
```bash
# Deploy infrastructure
az deployment sub create \
  --location swedencentral \
  --template-file infra/main.bicep \
  --parameters environmentName=test

# Run post-deployment configuration
./scripts/post-deploy.sh
```

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