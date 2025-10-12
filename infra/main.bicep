// Main Bicep template for Azure AI Foundry agent deployment
// This template provisions the core infrastructure for deploying the stock agent to Azure AI Foundry

targetScope = 'subscription'

@description('Environment name (used for resource naming)')
param environmentName string

// AI Foundry constants
var aiFoundryProjectName = 'experiment-jerryjoseph-0023'
var aiFoundryResourceGroup = 'rg-experiment-jerryjoseph-0023'

// Constants and calculated values
var applicationName = 'stockanalyzer'
var location = 'swedencentral'
var resourceGroupName = '${environmentName}-${applicationName}-rg'
var keyVaultName = '${environmentName}-${applicationName}-kv'
var appInsightsName = '${environmentName}-${applicationName}-ai'
var logAnalyticsName = '${environmentName}-${applicationName}-la'
var managedIdentityName = '${environmentName}-${applicationName}-id'

// Common tags for all resources
var commonTags = {
  environment: environmentName
  project: 'agentic-ai-stock-analyzer'
  analyzer: applicationName
  'naming-convention': '${environmentName}-${applicationName}-<service>'
}

// Create resource group for new resources
resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: commonTags
}

// Deploy managed identity into the resource group
module managedIdentityModule 'modules/managedidentity.bicep' = {
  name: 'managedidentity-deployment'
  scope: resourceGroup
  params: {
    managedIdentityName: managedIdentityName
    location: location
    tags: commonTags
  }
}

// Deploy monitoring resources into the resource group
module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring-deployment'
  scope: resourceGroup
  params: {
    appInsightsName: appInsightsName
    logAnalyticsName: logAnalyticsName
    location: location
    tags: commonTags
  }
}

// Deploy Key Vault into the resource group
module keyVault 'modules/keyvault.bicep' = {
  name: 'keyvault-deployment'
  scope: resourceGroup
  params: {
    keyVaultName: keyVaultName
    location: location
    managedIdentityPrincipalId: managedIdentityModule.outputs.managedIdentityPrincipalId
    tags: commonTags
  }
}

// Reference Azure AI Foundry project (validates existence)
module aiFoundry 'modules/aifoundry.bicep' = {
  name: 'aifoundry-reference'
  scope: az.resourceGroup(aiFoundryResourceGroup)
  params: {
    aiFoundryProjectName: aiFoundryProjectName
    aiFoundryResourceGroup: aiFoundryResourceGroup
  }
}

// Store configuration secrets in Key Vault using AI Foundry
module secrets 'modules/secrets.bicep' = {
  name: 'secrets-deployment'
  scope: resourceGroup
  params: {
    keyVaultName: keyVault.outputs.keyVaultName
    aiFoundryEndpoint: aiFoundry.outputs.aiFoundryEndpoint
  }
}

// Outputs - now includes AI Foundry project references
output RESOURCE_GROUP_ID string = resourceGroup.id
output RESOURCE_GROUP_NAME string = resourceGroup.name
output AZURE_AI_FOUNDRY_ENDPOINT string = aiFoundry.outputs.aiFoundryEndpoint
output AZURE_AI_FOUNDRY_PROJECT_NAME string = aiFoundry.outputs.aiFoundryProjectName
output KEY_VAULT_NAME string = keyVault.outputs.keyVaultName
output KEY_VAULT_URI string = keyVault.outputs.keyVaultUri
output MANAGED_IDENTITY_CLIENT_ID string = managedIdentityModule.outputs.managedIdentityClientId
output MANAGED_IDENTITY_PRINCIPAL_ID string = managedIdentityModule.outputs.managedIdentityPrincipalId
output APPLICATION_INSIGHTS_CONNECTION_STRING string = monitoring.outputs.appInsightsConnectionString
output APPLICATION_INSIGHTS_INSTRUMENTATION_KEY string = monitoring.outputs.appInsightsInstrumentationKey
output LOG_ANALYTICS_WORKSPACE_ID string = monitoring.outputs.logAnalyticsId
