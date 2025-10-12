// Reference Azure AI Foundry project
@description('Name of Azure AI Foundry project')
param aiFoundryProjectName string

@description('Resource group containing the Azure AI Foundry project')
param aiFoundryResourceGroup string

@description('Subscription ID containing the Azure AI Foundry project')
param aiFoundrySubscriptionId string = subscription().subscriptionId

// Reference the Azure AI Foundry project
resource aiFoundryProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' existing = {
  name: aiFoundryProjectName
  scope: resourceGroup(aiFoundrySubscriptionId, aiFoundryResourceGroup)
}

// Validate that the AI Foundry project exists and is accessible
// This will cause deployment to fail if the project doesn't exist or isn't accessible
var projectValidation = aiFoundryProject.id

// Output the project details
output aiFoundryProjectId string = aiFoundryProject.id
output aiFoundryProjectName string = aiFoundryProject.name
output aiFoundryEndpoint string = aiFoundryProject.properties.discoveryUrl
output aiFoundryLocation string = aiFoundryProject.location
output projectValidation string = projectValidation