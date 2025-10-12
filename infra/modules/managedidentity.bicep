// Managed Identity Bicep module
@description('Name of the managed identity')
param managedIdentityName string

@description('Location for the managed identity')
param location string

@description('Tags for the managed identity')
param tags object = {}

// Create managed identity for secure access
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: managedIdentityName
  location: location
  tags: tags
}

// Outputs
output managedIdentityId string = managedIdentity.id
output managedIdentityClientId string = managedIdentity.properties.clientId
output managedIdentityPrincipalId string = managedIdentity.properties.principalId
