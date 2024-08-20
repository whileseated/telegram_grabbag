import random
from telethon import TelegramClient
import asyncio
from telethon.errors import UsernameNotOccupiedError, ChatIdInvalidError
from telethon.tl.functions.messages import DeleteMessagesRequest
from config_repost_vids import api_id, api_hash, phone_number, chat_title_or_username, message_id_file

async def repost_and_delete_messages():
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

        # Read the message IDs from the text file
        with open(message_id_file, 'r') as f:
            message_ids = [int(line.strip()) for line in f.readlines()]

        # Select 3 random message IDs
        if len(message_ids) < 3:
            print("Not enough message IDs in the file to select 3.")
            return
        selected_message_ids = random.sample(message_ids, 3)

        # Repost each selected message individually
        new_message_ids = []
        for message_id in selected_message_ids:
            message = await client.get_messages(chat, ids=message_id)
            if message:
                # Repost the message with the same content
                if message.media:
                    sent_message = await client.send_file(
                        chat, 
                        message.media, 
                        caption=message.message, 
                        parse_mode='html'  # Preserve HTML formatting
                    )
                else:
                    sent_message = await client.send_message(
                        chat, 
                        message.message, 
                        parse_mode='html'  # Preserve HTML formatting
                    )

                # Append the new message ID
                new_message_ids.append(sent_message.id)

        # Delete the original messages
        await client(DeleteMessagesRequest(id=selected_message_ids))

        # Update the text file: remove deleted IDs and add new ones
        remaining_message_ids = [mid for mid in message_ids if mid not in selected_message_ids]
        remaining_message_ids.extend(new_message_ids)

        # Write the updated IDs back to the file
        with open(message_id_file, 'w') as f:
            for mid in remaining_message_ids:
                f.write(f"{mid}\n")

    except ChatIdInvalidError:
        print("The provided chat title or username is invalid or not accessible. Please verify it.")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(repost_and_delete_messages())
