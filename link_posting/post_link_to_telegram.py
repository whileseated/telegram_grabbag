from telethon import TelegramClient
import asyncio
from telethon.errors import UsernameNotOccupiedError, ChatIdInvalidError
from config import api_id, api_hash, phone_number, chat_title_or_username

async def post_links():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone_number)

    try:
        # Attempt to get the entity by username or title
        try:
            chat = await client.get_entity(chat_title_or_username)
        except (UsernameNotOccupiedError, ValueError):
            dialogs = await client.get_dialogs()

            chat = None
            for dialog in dialogs:
                if dialog.name == chat_title_or_username:
                    chat = dialog.entity
                    break

            if chat is None:
                print(f"Could not find a chat with the title: {chat_title_or_username}")
                return

        # Read the links from the text file
        with open('links_to_post.txt', 'r+') as f:
            links = f.readlines()

            if not links:
                print("No links available to post.")
                return

            # Get the first link to post
            link_to_post = links.pop(0).strip()

            # Post the link
            await client.send_message(chat, link_to_post)

            # Write back the remaining links to the file
            f.seek(0)
            f.writelines(links)
            f.truncate()

            # Log the posted link
            with open('posted_links.txt', 'a') as posted_file:
                posted_file.write(f"{link_to_post}\n")

            print(f"Successfully posted: {link_to_post}")

    except ChatIdInvalidError:
        print("The provided chat title or username is invalid or not accessible. Please verify it.")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post_links())
