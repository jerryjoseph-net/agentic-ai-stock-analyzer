#!/bin/bash

# Post-deployment script to store Azure AI Foundry connection details in Key Vault
# This script retrieves connection information from existing Azure AI Foundry project

set -e

# Check required environment variables
if [[ -z "$AZURE_AI_FOUNDRY_PROJECT_NAME" || -z "$KEY_VAULT_NAME" || -z "$AI_FOUNDRY_RESOURCE_GROUP" || -z "$AZURE_AI_FOUNDRY_ENDPOINT" ]]; then
    echo "Error: Required environment variables not set"
    echo "Required: AZURE_AI_FOUNDRY_PROJECT_NAME, KEY_VAULT_NAME, AI_FOUNDRY_RESOURCE_GROUP, AZURE_AI_FOUNDRY_ENDPOINT"
    exit 1
fi

echo "Retrieving Azure AI Foundry project details and storing in Key Vault..."

AI_FOUNDRY_PROJECT=$(az ml workspace show \
    --name "$AZURE_AI_FOUNDRY_PROJECT_NAME" \
    --resource-group "$AI_FOUNDRY_RESOURCE_GROUP" \
    --query "name" \
    --output tsv)

if [[ -z "$AI_FOUNDRY_PROJECT" ]]; then
    echo "❌ Failed to access Azure AI Foundry project: $AZURE_AI_FOUNDRY_PROJECT_NAME"
    exit 1
fi

echo "✅ Azure AI Foundry project verified: $AI_FOUNDRY_PROJECT"

# Store the AI Foundry endpoint in Key Vault
az keyvault secret set \
    --vault-name "$KEY_VAULT_NAME" \
    --name "AZURE-AI-FOUNDRY-ENDPOINT" \
    --value "$AZURE_AI_FOUNDRY_ENDPOINT" \
    --output none

echo "✅ Azure AI Foundry endpoint stored in Key Vault successfully"

# Store the project name in Key Vault for reference
az keyvault secret set \
    --vault-name "$KEY_VAULT_NAME" \
    --name "AZURE-AI-FOUNDRY-PROJECT-NAME" \
    --value "$AZURE_AI_FOUNDRY_PROJECT_NAME" \
    --output none

echo "✅ Azure AI Foundry project name stored in Key Vault successfully"

# Verify both secrets were stored
echo "Verifying secret storage..."
ENDPOINT_EXISTS=$(az keyvault secret show \
    --vault-name "$KEY_VAULT_NAME" \
    --name "AZURE-AI-FOUNDRY-ENDPOINT" \
    --query "name" \
    --output tsv 2>/dev/null || echo "")

PROJECT_EXISTS=$(az keyvault secret show \
    --vault-name "$KEY_VAULT_NAME" \
    --name "AZURE-AI-FOUNDRY-PROJECT-NAME" \
    --query "name" \
    --output tsv 2>/dev/null || echo "")

if [[ "$ENDPOINT_EXISTS" == "AZURE-AI-FOUNDRY-ENDPOINT" && "$PROJECT_EXISTS" == "AZURE-AI-FOUNDRY-PROJECT-NAME" ]]; then
    echo "✅ Both endpoint and project name verification successful"
else
    echo "❌ Secret verification failed"
    exit 1
fi

echo "Post-deployment configuration completed successfully"