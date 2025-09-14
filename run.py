#!/usr/bin/env python3
"""
Simple runner script for VK Cleaner.
This provides an alternative way to run the cleaner.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from vk_cleaner import main
    
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("\n\nOperation cancelled by user.")
    sys.exit(0)
except Exception as e:
    print(f"\nUnexpected error: {e}")
    print("Please check the logs for more details.")
    sys.exit(1)