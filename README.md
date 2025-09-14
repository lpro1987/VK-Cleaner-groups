# VK-Cleaner-groups

A Python tool to delete/leave all groups and communities in VKontakte (VK) social network.

## ⚠️ Warning

This tool will leave **ALL** groups and communities you are a member of. This action cannot be undone easily. Please use with caution and consider running in dry-run mode first.

## Features

- 🔒 **Safe by default**: Runs in dry-run mode by default
- 📝 **Detailed logging**: Logs all operations to file and console
- ✅ **Confirmation prompts**: Asks for confirmation before proceeding
- 🔄 **Rate limiting**: Respects VK API rate limits
- 📊 **Progress tracking**: Shows progress and summary statistics

## Installation

1. Clone this repository:
```bash
git clone https://github.com/lpro1987/VK-Cleaner-groups.git
cd VK-Cleaner-groups
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Method 1: Access Token (Recommended)

1. Go to [VK Developers](https://vk.com/apps?act=manage)
2. Create a new application or use existing one
3. Get your access token with `groups` permission
4. Set the environment variable:
```bash
export VK_ACCESS_TOKEN='your_access_token_here'
```

### Method 2: Login/Password

Set your VK credentials as environment variables:
```bash
export VK_LOGIN='your_vk_email_or_phone'
export VK_PASSWORD='your_vk_password'
```

## Usage

### Dry Run (Safe Mode)
First, run in dry-run mode to see what groups would be affected:
```bash
python vk_cleaner.py
```

This will show you all groups but won't actually leave them.

### Live Mode
To actually leave groups, edit `config.py` and set:
```python
DRY_RUN = False
```

Then run:
```bash
python vk_cleaner.py
```

## Configuration Options

Edit `config.py` to customize behavior:

- `DRY_RUN`: Set to `False` to actually delete groups (default: `True`)
- `REQUIRE_CONFIRMATION`: Ask for confirmation before proceeding (default: `True`)

## Safety Features

1. **Dry Run Mode**: By default, the tool runs in simulation mode
2. **Confirmation Prompts**: Always asks for user confirmation
3. **Detailed Logging**: All operations are logged to `vk_cleaner.log`
4. **Rate Limiting**: Respects VK API limits with delays between requests
5. **Error Handling**: Gracefully handles API errors and continues processing

## Output

The tool will:
1. List all groups you're a member of
2. Show which ones you're an admin of
3. Ask for confirmation
4. Process each group with progress updates
5. Provide a summary of successful/failed operations

## Logs

All operations are logged to `vk_cleaner.log` with timestamps for audit purposes.

## Troubleshooting

### Authentication Issues
- Make sure your access token has `groups` permission
- For login/password method, you might need to handle 2FA manually

### API Rate Limits
- The tool includes built-in delays between requests
- If you hit rate limits, the tool will log errors but continue

### Permissions
- You cannot leave groups where you're the only admin
- Some groups might have restrictions on leaving

## Disclaimer

This tool is provided as-is. The authors are not responsible for any unintended consequences of using this tool. Always test in dry-run mode first and make sure you understand what groups you'll be leaving.

## License

This project is open source and available under the MIT License.
