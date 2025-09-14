#!/usr/bin/env python3
"""
Basic tests for VK Cleaner functionality.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from vk_cleaner import VKCleaner


class TestVKCleaner(unittest.TestCase):
    """Test cases for VKCleaner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cleaner = VKCleaner()
    
    def test_init(self):
        """Test VKCleaner initialization."""
        self.assertIsNone(self.cleaner.vk_session)
        self.assertIsNone(self.cleaner.vk)
        self.assertIsNone(self.cleaner.user_id)
    
    @patch('vk_cleaner.vk_api')
    def test_authenticate_with_token(self, mock_vk_api):
        """Test authentication with access token."""
        # Mock the VK API
        mock_session = Mock()
        mock_api = Mock()
        mock_vk_api.VkApi.return_value = mock_session
        mock_session.get_api.return_value = mock_api
        mock_api.users.get.return_value = [{'id': 12345}]
        
        # Set up config with token
        with patch.object(config, 'VK_ACCESS_TOKEN', 'test_token'):
            result = self.cleaner.authenticate()
        
        self.assertTrue(result)
        self.assertEqual(self.cleaner.user_id, 12345)
        mock_vk_api.VkApi.assert_called_with(token='test_token')
    
    @patch('vk_cleaner.vk_api')
    def test_authenticate_with_login_password(self, mock_vk_api):
        """Test authentication with login/password."""
        # Mock the VK API
        mock_session = Mock()
        mock_api = Mock()
        mock_vk_api.VkApi.return_value = mock_session
        mock_session.get_api.return_value = mock_api
        mock_api.users.get.return_value = [{'id': 12345}]
        
        # Set up config with login/password
        with patch.object(config, 'VK_ACCESS_TOKEN', None), \
             patch.object(config, 'VK_LOGIN', 'test_login'), \
             patch.object(config, 'VK_PASSWORD', 'test_password'):
            result = self.cleaner.authenticate()
        
        self.assertTrue(result)
        self.assertEqual(self.cleaner.user_id, 12345)
        mock_vk_api.VkApi.assert_called_with('test_login', 'test_password')
        mock_session.auth.assert_called_once()
    
    def test_authenticate_no_credentials(self):
        """Test authentication with no credentials."""
        with patch.object(config, 'VK_ACCESS_TOKEN', None), \
             patch.object(config, 'VK_LOGIN', None), \
             patch.object(config, 'VK_PASSWORD', None):
            result = self.cleaner.authenticate()
        
        self.assertFalse(result)
    
    def test_leave_group_dry_run(self):
        """Test leave_group in dry run mode."""
        with patch.object(config, 'DRY_RUN', True):
            result = self.cleaner.leave_group(123, 'Test Group')
        
        self.assertTrue(result)
    
    @patch('vk_cleaner.logger')
    def test_leave_group_live_mode(self, mock_logger):
        """Test leave_group in live mode."""
        # Mock VK API
        mock_vk = Mock()
        self.cleaner.vk = mock_vk
        
        with patch.object(config, 'DRY_RUN', False):
            result = self.cleaner.leave_group(123, 'Test Group')
        
        self.assertTrue(result)
        mock_vk.groups.leave.assert_called_with(group_id=123)
    
    def test_get_user_groups(self):
        """Test get_user_groups method."""
        # Mock VK API
        mock_vk = Mock()
        mock_vk.groups.get.return_value = {
            'count': 2,
            'items': [
                {'id': 1, 'name': 'Group 1', 'type': 'group'},
                {'id': 2, 'name': 'Group 2', 'type': 'page'}
            ]
        }
        self.cleaner.vk = mock_vk
        
        groups = self.cleaner.get_user_groups()
        
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]['name'], 'Group 1')
        self.assertEqual(groups[1]['name'], 'Group 2')


class TestConfig(unittest.TestCase):
    """Test configuration settings."""
    
    def test_default_config(self):
        """Test default configuration values."""
        self.assertTrue(config.DRY_RUN)  # Should be True by default for safety
        self.assertTrue(config.REQUIRE_CONFIRMATION)


if __name__ == '__main__':
    unittest.main()