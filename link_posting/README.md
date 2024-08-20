
# Telegram Link Posting Script

This script automatically posts a link from a text file to a Telegram channel every time it's run. Once the link is successfully posted, it is moved from the source text file to a "posted" text file, ensuring no duplicates are posted.

## Features

- **Automated Posting**: The script reads one link from a text file (`links_to_post.txt`) and posts it to a specified Telegram channel.
- **File Management**: Successfully posted links are removed from the source file and added to `posted_links.txt` to prevent reposting.
- **Telethon Integration**: Uses the `telethon` library to interact with Telegram.

## Prerequisites

1. **Python 3.x**: Ensure Python is installed on your machine. You can download it from [python.org](https://www.python.org/).

2. **Telethon Library**: Install the required Python library using pip:

   ```bash
   pip install telethon
   ```

3. **Telegram API Credentials**: You need to set up a Telegram application to get your `api_id` and `api_hash`. You can obtain these from the [Telegram API](https://my.telegram.org/).

## Setup

1. **Clone or Download the Script**: Download the script files to your local machine.

2. **Configure API Credentials**:
   - Open the `config.py` file.
   - Add your Telegram API credentials (i.e., `api_id`, `api_hash`, and other necessary configurations).
   - Example:

     ```python
     api_id = 'YOUR_API_ID'
     api_hash = 'YOUR_API_HASH'
     chat_title_or_username = 'the name of your channel'
     ```

3. **Prepare the Text Files**:
   - `links_to_post.txt`: Add the links you want to post, each on a new line. For example:
     ```
https://www.youtube.com/watch?v=hEbUlDq11gI
https://www.youtube.com/watch?v=moDgB0KFdPk
     ```
   - `posted_links.txt`: This file will automatically be updated with successfully posted links. Do not manually edit this file.

## Usage

1. **Run the Script**:
   - To post a link, simply run the main script:
   
     ```bash
     python post_link_to_telegram.py
     ```

2. **Automation**: You can automate this process by setting up a cron job (Linux/Mac) or Task Scheduler (Windows) to run the script at regular intervals.

## How It Works

- **Step 1**: The script reads the first link from `links_to_post.txt`.
- **Step 2**: It posts the link to your configured Telegram channel.
- **Step 3**: If the link is successfully posted, it is removed from `links_to_post.txt` and added to `posted_links.txt`.
- **Step 4**: If an error occurs (e.g., network issues), the link remains in `links_to_post.txt` and will be retried the next time the script runs.

## Notes

- Ensure that the Telegram account used by the script has the necessary permissions to post in the target channel.
- This script does not handle duplicate links within `links_to_post.txt`. Ensure that each link is unique.

## Troubleshooting

- **Authentication Issues**: Double-check that your `api_id` and `api_hash` are correct and that your account has access to the specified channel.
- **Missing Dependencies**: Make sure the `telethon` library is installed correctly.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
