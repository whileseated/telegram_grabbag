
# Telegram Video Message Reposting Script

This project consists of two Python scripts that automate the process of collecting video message IDs from a Telegram chat and reposting a selected number of those videos to the top of a channel. The scripts use the Telethon library to interact with Telegram's API.

## Requirements

- Python 3.x
- Telethon library

You can install the required dependencies using pip:

```bash
pip install telethon
```

## Setup

Before running the scripts, you'll need to obtain the following from Telegram:

- **api_id**: Your Telegram API ID
- **api_hash**: Your Telegram API hash
- **phone_number**: The phone number associated with your Telegram account
- **chat_title_or_username**: The title or username of the Telegram chat from which you want to collect video messages

You can get the API credentials by creating a new application in the [Telegram Developer Portal](https://my.telegram.org/apps).

## Scripts Overview

### 1. `get_message_ids.py`

This script collects the message IDs of all video messages from a specific Telegram chat and writes them to a text file (`message_ids.txt`).

**Usage:**

```bash
python3 get_message_ids.py > message_ids.txt
```

The script will connect to the specified chat and extract all the message IDs that contain video content. The output will be redirected to the `message_ids.txt` file.

### 2. `repost_three_messages_to_video_channel.py`

Once you have the `message_ids.txt` file, this script will randomly select three video messages from the list and repost them to the top of the channel. It will also delete the previously posted video messages and update the `message_ids.txt` file with the new message IDs.

**Usage:**

```bash
python3 repost_three_messages_to_video_channel.py
```

The script performs the following actions:
- Randomly selects three video message IDs from `message_ids.txt`.
- Reposts the selected video messages to the top of the specified channel.
- Deletes the old video messages and updates `message_ids.txt` with the new message IDs.

## Configuration

You will need to configure the following variables in both scripts:

- `api_id`: Your Telegram API ID
- `api_hash`: Your Telegram API hash
- `phone_number`: Your Telegram phone number
- `chat_title_or_username`: The chat title or username where the script will collect video messages from

These values should be set directly in the scripts before running them.

## Example

1. First, run the `get_message_ids.py` script to collect video message IDs:

```bash
python3 get_message_ids.py > message_ids.txt
```

2. After generating the `message_ids.txt` file, run the `repost_three_messages_to_video_channel.py` script to repost the selected video messages:

```bash
python3 repost_three_messages_to_video_channel.py
```

## Troubleshooting

- **Authentication errors**: Make sure your `api_id`, `api_hash`, and `phone_number` are correct.
- **Invalid chat title or username**: Double-check that the `chat_title_or_username` matches the exact title or username of the chat.
- **Telethon errors**: If you encounter errors from the Telethon library, ensure that you have the latest version installed.

## License

This project is licensed under the MIT License.

