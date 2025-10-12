# Post-deployment script to store Azure AI Foundry connection details in Key Vault
# This script retrieves connection information from existing Azure AI Foundry project

param(
    [Parameter(Mandatory=$true)]
    [string]$AIFoundryProjectName,
    
    [Parameter(Mandatory=$true)]
    [string]$KeyVaultName,
    
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$true)]
    [string]$AIFoundryEndpoint
)

Write-Host "Retrieving Azure AI Foundry project details and storing in Key Vault..." -ForegroundColor Green

try {
    # Verify the AI Foundry project exists and is accessible
    $aiFoundryProject = az ml workspace show `
        --name $AIFoundryProjectName `
        --resource-group $ResourceGroup `
        --query "name" `
        --output tsv

    if (-not $aiFoundryProject) {
        throw "Failed to access Azure AI Foundry project: $AIFoundryProjectName"
    }

    Write-Host "✅ Azure AI Foundry project verified: $aiFoundryProject" -ForegroundColor Green

    # Store the AI Foundry endpoint in Key Vault
    az keyvault secret set `
        --vault-name $KeyVaultName `
        --name "AZURE-AI-FOUNDRY-ENDPOINT" `
        --value $AIFoundryEndpoint `
        --output none

    Write-Host "✅ Azure AI Foundry endpoint stored in Key Vault successfully" -ForegroundColor Green

    # Store the project name in Key Vault for reference
    az keyvault secret set `
        --vault-name $KeyVaultName `
        --name "AZURE-AI-FOUNDRY-PROJECT-NAME" `
        --value $AIFoundryProjectName `
        --output none

    Write-Host "✅ Azure AI Foundry project name stored in Key Vault successfully" -ForegroundColor Green

    # Verify both secrets were stored
    Write-Host "Verifying secret storage..." -ForegroundColor Yellow
    $endpointExists = az keyvault secret show `
        --vault-name $KeyVaultName `
        --name "AZURE-AI-FOUNDRY-ENDPOINT" `
        --query "name" `
        --output tsv 2>$null

    $projectExists = az keyvault secret show `
        --vault-name $KeyVaultName `
        --name "AZURE-AI-FOUNDRY-PROJECT-NAME" `
        --query "name" `
        --output tsv 2>$null

    if ($endpointExists -eq "AZURE-AI-FOUNDRY-ENDPOINT" -and $projectExists -eq "AZURE-AI-FOUNDRY-PROJECT-NAME") {
        Write-Host "✅ Both endpoint and project name verification successful" -ForegroundColor Green
    } else {
        throw "Secret verification failed"
    }

    Write-Host "Post-deployment configuration completed successfully" -ForegroundColor Green
}
catch {
    Write-Error "Post-deployment script failed: $($_.Exception.Message)"
    exit 1
}