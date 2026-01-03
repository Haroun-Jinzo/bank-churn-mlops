# 1. Generate a unique name
SP_NAME="sp-mlops-$(whoami)-$(date +%s)"
echo "Creating Service Principal: $SP_NAME"

# 2. Get your Subscription ID (if not already set)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# 3. Create the Service Principal with the unique name
az ad sp create-for-rbac \
  --name "$SP_NAME" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/rg-mlops \
  --sdk-auth