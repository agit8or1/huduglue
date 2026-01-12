#!/bin/bash
#
# Fix malformed APP_MASTER_KEY in .env file
# This script regenerates a valid encryption key
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Fix APP_MASTER_KEY ===${NC}\n"

# Find .env file
if [ ! -f "$HOME/huduglue/.env" ]; then
    echo -e "${RED}Error: .env file not found at $HOME/huduglue/.env${NC}"
    echo "Please run this script from the correct location"
    exit 1
fi

cd "$HOME/huduglue"

echo -e "${GREEN}[1/5]${NC} Backing up current .env file..."
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
echo "      Backup created"

echo -e "\n${GREEN}[2/5]${NC} Checking current APP_MASTER_KEY..."
CURRENT_KEY=$(grep "^APP_MASTER_KEY=" .env | cut -d= -f2)
echo "      Current key length: ${#CURRENT_KEY} characters"

if [ ${#CURRENT_KEY} -eq 44 ]; then
    echo -e "${YELLOW}      Warning: Key appears to be correct length (44 chars)${NC}"
    echo "      This might be a different issue. Continuing anyway..."
fi

echo -e "\n${GREEN}[3/5]${NC} Generating new valid APP_MASTER_KEY..."
source venv/bin/activate
NEW_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
echo "      New key length: ${#NEW_KEY} characters"

if [ ${#NEW_KEY} -ne 44 ]; then
    echo -e "${RED}Error: Generated key has wrong length${NC}"
    exit 1
fi

echo -e "\n${GREEN}[4/5]${NC} Updating .env file..."
sed -i "s|^APP_MASTER_KEY=.*|APP_MASTER_KEY=${NEW_KEY}|" .env
echo "      .env file updated"

echo -e "\n${GREEN}[5/5]${NC} Restarting service..."
if sudo systemctl restart huduglue-gunicorn.service; then
    echo "      Service restarted successfully"
else
    echo -e "${YELLOW}      Warning: Could not restart service${NC}"
    echo "      You may need to restart manually: sudo systemctl restart huduglue-gunicorn.service"
fi

echo -e "\n${GREEN}✓ Fix completed!${NC}\n"
echo "Your APP_MASTER_KEY has been regenerated."
echo "The old .env file has been backed up with timestamp."
echo ""
echo -e "${YELLOW}⚠ Important:${NC}"
echo "If you had any encrypted data (passwords, API keys) before,"
echo "they cannot be decrypted with the new key."
echo "Since you just installed, this should not be an issue."
echo ""
