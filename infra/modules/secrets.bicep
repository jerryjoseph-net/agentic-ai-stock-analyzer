// Secrets module for storing configuration in Key Vault
@description('Key Vault name')
param keyVaultName string

@description('Azure AI Foundry endpoint from existing project')
param aiFoundryEndpoint string

// Store Azure AI Foundry endpoint in Key Vault
resource aiFoundryEndpointSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  name: '${keyVaultName}/AZURE-AI-FOUNDRY-ENDPOINT'
  properties: {
    value: aiFoundryEndpoint
  }
}

// Output for verification
output endpointSecretName string = aiFoundryEndpointSecret.name
