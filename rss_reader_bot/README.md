# Telegram RSS Bot

A straightforward, database-free RSS reader bot for Telegram, designed for easy tracking of your favorite RSS feeds.

## Features

- **No Database Required**: Uses a simple text file (`feeds.txt`) for managing subscriptions.
- **Easy Configuration**: Just a `config.txt` file for Telegram Token, Chat ID and your personal telegram ID.
- **Supports Common RSS Formats**: Compatible with most RSS/Atom feeds.
- **User-Friendly Commands**: Add, check, and remove feeds with intuitive Telegram bot commands.
- **Dockerized**: Runs in docker and writes outside of container so feeds.txt stays updated.
- **Private**: While all telegram bots are (by design) public, this particular bot is dedicated to one, single user. If anyone else tries to use the bot, they'll get a message denying access.

## Setup

### Prerequisites

- Python 3.x
- `python-telegram-bot` module (version 13.7)
- `feedparser` module

### Dockerless Installation

1. **Create a Telegram Bot**:
   - Use [@BotFather](https://t.me/botfather) to create a new Telegram bot. This will generate your Telegram Token.
   - Find your personal chat ID using [@userinfobot](https://t.me/userinfobot).

2. **Configuration File**:
   - Create a `config.txt` file.
   - Add your Telegram Token and your Chat ID on separate lines:

     ```
     your_telegram_token
     your_telegram_chat_id
     your_telegram_id (might be the same as the chat_id)
     ```

3. **Feeds File**:
   - Create a blank `feeds.txt` file for your RSS subscriptions.
   - When the bot adds a subscription (one per line), the feed information is formatted as follows: `RSS URL , NICKNAME , LAST POST URL` 

4. **Install Dependencies**:
   Run the following commands to install necessary Python modules:

    ```
    pip install python-telegram-bot==13.7
    pip install feedparser
    ```

### Docker Installation

   **Steps 1-3 above, plus**:
   - Build the Docker image like this:
   ```
   docker build -t name-of-your-docker-image .
   ```

   - Run the Docker container like this:
   ```
   docker run --restart=always --name name-of-your-docker-container -v /Users/location-of-your-repo-folder/:/app name-of-your-docker-image
   ```

### Running the Bot

Execute the script to start the bot:

```
python3 telegram_rss.py
```

Keep the script running to maintain the bot's functionality.

## Usage

Interact with the bot using these commands:

- **Add a Feed**: Simply paste an RSS/Atom feed URL into the chat.
- **Check Feeds**: Type `check` to review the latest posts from all subscribed feeds.
- **Remove a Feed**: Use `remove` and follow the UI picker to unsubscribe from a feed.

### Customizing Bot Commands

Configure additional bot commands through [@BotFather](https://t.me/botfather) to make them available in the bot's menu.

## Planned Features

- [ ] Automatic feed checks every 15 minutes.
- [ ] Start message for new users.
- [ ] Cancel option for each command.
- [ ] New command to display all subscribed feeds.
- [x] Dockerize it all.
- [x] Added auth-check so bot can be used by one user only.

## Demonstration

![Telegram RSS Bot in Action](telegram_rss.GIF)
