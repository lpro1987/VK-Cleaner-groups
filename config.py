"""Configuration file for VK Cleaner."""

import os

# VK API Configuration
VK_APP_ID = os.getenv('VK_APP_ID')
VK_LOGIN = os.getenv('VK_LOGIN')
VK_PASSWORD = os.getenv('VK_PASSWORD')
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')

# Safety settings
DRY_RUN = True  # Set to False to actually delete groups
REQUIRE_CONFIRMATION = True  # Always ask for confirmation before deletion