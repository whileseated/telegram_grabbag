from telethon import TelegramClient
import asyncio
from telethon.errors import UsernameNotOccupiedError, ChatIdInvalidError

# Replace these with your own values
api_id = ''
api_hash = ''
phone_number = ''
chat_title_or_username = ''  # Replace with chat title or name

async def get_video_message_ids():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone_number)

    try:
        # Attempt to get the entity by username
        try:
            chat = await client.get_entity(chat_title_or_username)
        except (UsernameNotOccupiedError, ValueError):
            # If username not found, attempt to find by title
            dialogs = await client.get_dialogs()

            chat = None
            for dialog in dialogs:
                if dialog.name == chat_title_or_username:
                    chat = dialog.entity
                    break

            if chat is None:
                print(f"Could not find a chat with the title: {chat_title_or_username}")
                return

        # Now we have the correct entity

        video_message_ids = []

        async for message in client.iter_messages(chat):
            if message.media and message.video:  # Check if the media is a video
                video_message_ids.append(message.id)

        # Print each video message ID on a new line
        for message_id in video_message_ids:
            print(message_id)

    except ChatIdInvalidError:
        print("The provided chat title or username is invalid or not accessible. Please verify it.")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_video_message_ids())
