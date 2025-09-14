#!/usr/bin/env python3
"""
VK Cleaner - Delete all groups and communities in VK
This tool helps you leave/delete all groups and communities you're a member of.
"""

import sys
import time
import logging
from typing import List, Dict, Any

try:
    import vk_api
except ImportError:
    print("ERROR: vk_api library not found. Please install it with: pip install vk_api")
    sys.exit(1)

import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vk_cleaner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class VKCleaner:
    """VK Groups and Communities cleaner."""
    
    def __init__(self):
        """Initialize VK API session."""
        self.vk_session = None
        self.vk = None
        self.user_id = None
        
    def authenticate(self) -> bool:
        """Authenticate with VK API."""
        try:
            if config.VK_ACCESS_TOKEN:
                # Use access token if provided
                self.vk_session = vk_api.VkApi(token=config.VK_ACCESS_TOKEN)
                logger.info("Authenticating with access token...")
            elif config.VK_LOGIN and config.VK_PASSWORD:
                # Use login/password authentication
                self.vk_session = vk_api.VkApi(config.VK_LOGIN, config.VK_PASSWORD)
                logger.info("Authenticating with login/password...")
                self.vk_session.auth()
            else:
                logger.error("No authentication method provided. Please set VK_ACCESS_TOKEN or VK_LOGIN/VK_PASSWORD")
                return False
                
            self.vk = self.vk_session.get_api()
            
            # Get current user info to verify authentication
            user_info = self.vk.users.get()
            self.user_id = user_info[0]['id']
            logger.info(f"Successfully authenticated as user ID: {self.user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def get_user_groups(self) -> List[Dict[str, Any]]:
        """Get all groups the user is a member of."""
        try:
            logger.info("Fetching user groups...")
            groups = self.vk.groups.get(extended=1, fields='name,type,is_admin,is_member')
            logger.info(f"Found {groups['count']} groups")
            return groups['items']
        except Exception as e:
            logger.error(f"Failed to fetch groups: {e}")
            return []
    
    def leave_group(self, group_id: int, group_name: str) -> bool:
        """Leave a specific group."""
        try:
            if config.DRY_RUN:
                logger.info(f"[DRY RUN] Would leave group: {group_name} (ID: {group_id})")
                return True
            
            self.vk.groups.leave(group_id=group_id)
            logger.info(f"Successfully left group: {group_name} (ID: {group_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to leave group {group_name} (ID: {group_id}): {e}")
            return False
    
    def delete_all_groups(self) -> None:
        """Delete/leave all groups and communities."""
        if not self.authenticate():
            logger.error("Authentication failed. Cannot proceed.")
            return
        
        groups = self.get_user_groups()
        if not groups:
            logger.info("No groups found or failed to fetch groups.")
            return
        
        logger.info(f"Found {len(groups)} groups to process")
        
        # Display groups that will be processed
        print("\nGroups that will be left:")
        for group in groups:
            group_type = "Community" if group.get('type') == 'page' else "Group"
            admin_status = " (Admin)" if group.get('is_admin') else ""
            print(f"- {group['name']} ({group_type}){admin_status}")
        
        if config.REQUIRE_CONFIRMATION:
            if config.DRY_RUN:
                print(f"\n[DRY RUN MODE] This is a simulation - no groups will actually be left.")
            else:
                print(f"\n[LIVE MODE] This will actually leave {len(groups)} groups!")
            
            confirmation = input("\nDo you want to proceed? (yes/no): ").lower().strip()
            if confirmation not in ['yes', 'y']:
                logger.info("Operation cancelled by user.")
                return
        
        # Process groups
        successful = 0
        failed = 0
        
        for i, group in enumerate(groups, 1):
            group_id = group['id']
            group_name = group['name']
            
            logger.info(f"Processing {i}/{len(groups)}: {group_name}")
            
            if self.leave_group(group_id, group_name):
                successful += 1
            else:
                failed += 1
            
            # Rate limiting - wait between requests
            if i < len(groups):  # Don't wait after the last request
                time.sleep(0.5)  # 500ms delay between requests
        
        # Summary
        logger.info(f"\nOperation completed!")
        logger.info(f"Successfully processed: {successful}")
        logger.info(f"Failed: {failed}")
        
        if config.DRY_RUN:
            logger.info("This was a dry run - no actual changes were made.")
            logger.info("To perform actual deletion, set DRY_RUN = False in config.py")


def main():
    """Main function."""
    print("VK Cleaner - Delete all groups and communities")
    print("=" * 50)
    
    # Check configuration
    if not (config.VK_ACCESS_TOKEN or (config.VK_LOGIN and config.VK_PASSWORD)):
        print("ERROR: No authentication credentials found!")
        print("Please set one of the following environment variables:")
        print("- VK_ACCESS_TOKEN (recommended)")
        print("- VK_LOGIN and VK_PASSWORD")
        print("\nExample:")
        print("export VK_ACCESS_TOKEN='your_access_token_here'")
        sys.exit(1)
    
    cleaner = VKCleaner()
    cleaner.delete_all_groups()


if __name__ == "__main__":
    main()