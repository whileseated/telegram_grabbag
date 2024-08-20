# Telegram Grab Bag
A folderized collection of scripts and bots for Telegram.

A few of these were repositories of their own. I thought it would make the most sense to combine in one spot. Each folder can be thought of as its own standalone project.

**message_reposting** - Scripts that capture message ids for every post in a particular channel that has a video. Those message ids are output to a text file. The text file is then used as a simple log from which another script reposts three (or any number) of messages to the top of your channel, while deleting their earlier reference.

**link_posting** - A script that posts a link (or url) to a channel. Can be automated or set-up with docker or a cron job. Links are kept in a text file, and once posted, they're moved to a "posted links" text file. These scripts do not require a bot, and can interact directly with a channel. Works amazingly well with a long list of youtube videos.

**rss_reader_bot** - A simple RSS reader that can subscribe to, check, and delete subscribed feeds. Works well in docker for months at a time.