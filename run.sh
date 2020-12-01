#!/bin/bash

NO='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;96m'
YELLOW='\033[0;33m'

BOLD='\033[1m'


echo -e "${BLUE}${BOLD}Starting Log-Skeleton API server..."

python3.7 -m src.api.server