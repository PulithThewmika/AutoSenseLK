#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
