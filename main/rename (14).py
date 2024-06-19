
import os
import time, datetime
import shutil
import zipfile
import tarfile
import requests
from pyrogram.types import Message
from pyrogram.types import Document, Video
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import MessageNotModified
from config import DOWNLOAD_LOCATION, CAPTION
from main.utils import progress_message, humanbytes
import subprocess
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from config import GROUP, AUTH_USERS, ADMIN
from main.utils import heroku_restart
import aiohttp
from pyrogram.errors import RPCError, FloodWait

import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)


# Global dictionary to store user settings

user_settings = {}

# Initialize global settings variables
METADATA_ENABLED = True 
PHOTO_ATTACH_ENABLED = True
MULTITASK_ENABLED = True
RENAME_ENABLED = True
REMOVETAGS_ENABLED = True
CHANGE_INDEX_ENABLED = True 
  

# Command handler to start the interaction (only in admin)
@Client.on_message(filters.command("bsettings") & filters.chat(ADMIN))
async def bot_settings_command(_, msg):
    await display_bot_settings_inline(msg)


# Inline function to display user settings with inline buttons
async def display_bot_settings_inline(msg):
    global METADATA_ENABLED, PHOTO_ATTACH_ENABLED, MULTITASK_ENABLED, RENAME_ENABLED, REMOVETAGS_ENABLED, CHANGE_INDEX_ENABLED

    metadata_status = "✅ Enabled" if METADATA_ENABLED else "❌ Disabled"
    photo_attach_status = "✅ Enabled" if PHOTO_ATTACH_ENABLED else "❌ Disabled"
    multitask_status = "✅ Enabled" if MULTITASK_ENABLED else "❌ Disabled"
    rename_status = "✅ Enabled" if RENAME_ENABLED else "❌ Disabled"
    removealltags_status = "✅ Enabled" if REMOVETAGS_ENABLED else "❌ Disabled"
    change_index_status = "✅ Enabled" if CHANGE_INDEX_ENABLED else "❌ Disabled"
    
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("💠", callback_data="sunrises24_bot_updates")],            
            [InlineKeyboardButton(f"{rename_status} Change Rename 📝", callback_data="toggle_rename")],
            [InlineKeyboardButton(f"{removealltags_status} Remove All Tags 📛", callback_data="toggle_removealltags")],
            [InlineKeyboardButton(f"{metadata_status} Change Metadata ☄️", callback_data="toggle_metadata")],            
            [InlineKeyboardButton(f"{change_index_status} Change Index ♻️", callback_data="toggle_change_index")],
            [InlineKeyboardButton(f"{photo_attach_status} Attach Photo 🖼️", callback_data="toggle_photo_attach")],                        
            [InlineKeyboardButton(f"{multitask_status} Multi task 📑", callback_data="toggle_multitask")],            
            [InlineKeyboardButton("Close ❌", callback_data="del")],
            [InlineKeyboardButton("💠", callback_data="sunrises24_bot_updates")]
        ]
    )

    await msg.reply_text("Use inline buttons to manage your settings:", reply_markup=keyboard)


#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
@Client.on_callback_query(filters.regex("del"))
async def closed(bot, msg):
    try:
        await msg.message.delete()
    except:
        return

# Callback query handlers

@Client.on_callback_query(filters.regex("^toggle_rename$"))
async def toggle_rename_callback(_, callback_query):
    global RENAME_ENABLED

    RENAME_ENABLED = not RENAME_ENABLED
    await update_settings_message(callback_query.message)

@Client.on_callback_query(filters.regex("^toggle_removealltags$"))
async def toggle_removealltags_callback(_, callback_query):
    global REMOVETAGS_ENABLED

    REMOVETAGS_ENABLED = not REMOVETAGS_ENABLED
    await update_settings_message(callback_query.message)

@Client.on_callback_query(filters.regex("^toggle_metadata$"))
async def toggle_metadata_callback(_, callback_query):
    global METADATA_ENABLED

    METADATA_ENABLED = not METADATA_ENABLED
    await update_settings_message(callback_query.message)


@Client.on_callback_query(filters.regex("^toggle_photo_attach$"))
async def toggle_photo_attach_callback(_, callback_query):
    global PHOTO_ATTACH_ENABLED

    PHOTO_ATTACH_ENABLED = not PHOTO_ATTACH_ENABLED
    await update_settings_message(callback_query.message)


@Client.on_callback_query(filters.regex("^toggle_multitask$"))
async def toggle_multitask_callback(_, callback_query):
    global MULTITASK_ENABLED

    MULTITASK_ENABLED = not MULTITASK_ENABLED
    await update_settings_message(callback_query.message)

@Client.on_callback_query(filters.regex("^toggle_change_index$"))
async def toggle_change_index_callback(_, callback_query):
    global CHANGE_INDEX_ENABLED

    CHANGE_INDEX_ENABLED = not CHANGE_INDEX_ENABLED
    await update_settings_message(callback_query.message)
    
# Callback query handler for the "sunrises24_bot_updates" button
@Client.on_callback_query(filters.regex("^sunrises24_bot_updates$"))
async def sunrises24_bot_updates_callback(_, callback_query):
    await callback_query.answer("MADE BY @SUNRISES24BOTUPDATES ❤️", show_alert=True)    


async def update_settings_message(message):
    global METADATA_ENABLED, PHOTO_ATTACH_ENABLED, MULTITASK_ENABLED, RENAME_ENABLED, REMOVETAGS_ENABLED, CHANGE_INDEX_ENABLED

    metadata_status = "✅ Enabled" if METADATA_ENABLED else "❌ Disabled"
    photo_attach_status = "✅ Enabled" if PHOTO_ATTACH_ENABLED else "❌ Disabled"
    multitask_status = "✅ Enabled" if MULTITASK_ENABLED else "❌ Disabled"
    rename_status = "✅ Enabled" if RENAME_ENABLED else "❌ Disabled"
    removealltags_status = "✅ Enabled" if REMOVETAGS_ENABLED else "❌ Disabled"
    change_index_status = "✅ Enabled" if CHANGE_INDEX_ENABLED else "❌ Disabled"
      
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("💠", callback_data="sunrises24_bot_updates")],            
            [InlineKeyboardButton(f"{rename_status} Change Rename 📝", callback_data="toggle_rename")],
            [InlineKeyboardButton(f"{removealltags_status} Remove All Tags 📛", callback_data="toggle_removealltags")],
            [InlineKeyboardButton(f"{metadata_status} Change Metadata ☄️", callback_data="toggle_metadata")],            
            [InlineKeyboardButton(f"{change_index_status} Change Index ♻️", callback_data="toggle_change_index")],
            [InlineKeyboardButton(f"{photo_attach_status} Attach Photo 🖼️", callback_data="toggle_photo_attach")],                        
            [InlineKeyboardButton(f"{multitask_status} Multi task 📑", callback_data="toggle_multitask")],            
            [InlineKeyboardButton("Close ❌", callback_data="del")],
            [InlineKeyboardButton("💠", callback_data="sunrises24_bot_updates")]
        ]
    )

    await message.edit_text("Use inline buttons to manage your settings:", reply_markup=keyboard)



@Client.on_message(filters.command("usersettings") & filters.group)
async def display_user_settings(client, msg):
    logging.info(f"Command /usersettings received from user {msg.from_user.id} in chat {msg.chat.id}")
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💠", callback_data="sunrises24_bot_updates")],
        [InlineKeyboardButton("Thumbnail Settings 📄", callback_data="thumbnail_settings")],
        [InlineKeyboardButton("Preview Metadata ✨", callback_data="preview_metadata")],
        [InlineKeyboardButton("Attach Photo 📎", callback_data="attach_photo"), 
         InlineKeyboardButton("Preview Photo ✨", callback_data="preview_photo")],
        [InlineKeyboardButton("Preview Attach Photo task 🖼️", callback_data="preview_photo_attach_task")],
        [InlineKeyboardButton("Preview Multi task 📑", callback_data="preview_multitask")],
        [InlineKeyboardButton("Preview Rename task 📝", callback_data="preview_rename_task")],
        [InlineKeyboardButton("Preview Metadata task ☄️", callback_data="preview_metadata_task")],
        [InlineKeyboardButton("Preview Index task ♻️", callback_data="preview_change_index_task")],
        [InlineKeyboardButton("Preview Remove Tags task 📛", callback_data="preview_removetags_task")],      
        [InlineKeyboardButton("Close ❌", callback_data="del")]
    ])

    await msg.reply("User Settings", reply_markup=keyboard)



# Inline query handler for previewing metadata titles
@Client.on_callback_query(filters.regex("^preview_metadata$"))
async def inline_preview_metadata_callback(_, callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    titles = user_settings.get(user_id, {})
    if not titles or not any(titles.values()):
        await callback_query.message.reply_text("Metadata titles are not fully set. Please set all titles first.")
        return
    
    preview_text = f"Video Title: {titles.get('video_title', '')}\n" \
                   f"Audio Title: {titles.get('audio_title', '')}\n" \
                   f"Subtitle Title: {titles.get('subtitle_title', '')}"
    await callback_query.message.reply_text(f"Current Metadata Titles:\n\n{preview_text}")

# Inline query handler for attaching photo
@Client.on_callback_query(filters.regex("^attach_photo$"))
async def inline_attach_photo_callback(_, callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    user_settings[user_id] = user_settings.get(user_id, {})
    user_settings[user_id]["attach_photo"] = True
    await callback_query.message.edit_text("Please send a photo to be attached using the setphoto command.")


# Inline query handler for previewing attached photo
@Client.on_callback_query(filters.regex("^preview_photo$"))
async def inline_preview_photo_callback(client, callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    attachment_path = os.path.join(DOWNLOAD_LOCATION, f"attachment_{user_id}.jpg")
    
    if not os.path.exists(attachment_path):
        await callback_query.message.reply_text("No photo has been attached yet.")
        return
    
    await callback_query.message.reply_photo(photo=attachment_path, caption="Attached Photo")
# Inline query handler for previewing multitask status
@Client.on_callback_query(filters.regex("^preview_multitask$"))
async def inline_preview_multitask_callback(_, callback_query):
    await callback_query.answer()
    global MULTITASK_ENABLED
    status_text = "Multi task is enabled." if MULTITASK_ENABLED else "Multi task is disabled."
    await callback_query.message.reply_text(status_text)


# Inline query handler for previewing multitask status
@Client.on_callback_query(filters.regex("^preview_metadata_task$"))
async def inline_preview_metadata_task_callback(_, callback_query):
    await callback_query.answer()
    global METADATA_ENABLED
    status_text = "Metadata is enabled." if METADATA_ENABLED else "Metadata is disabled."
    await callback_query.message.reply_text(status_text)

# Inline query handler for previewing multitask status
@Client.on_callback_query(filters.regex("^preview_photo_attach_task$"))
async def inline_preview_photo_attach_task_callback(_, callback_query):
    await callback_query.answer()
    global PHOTO_ATTACH_ENABLED
    status_text = "Photo Attach is enabled." if PHOTO_ATTACH_ENABLED else "Photo Attach is disabled."
    await callback_query.message.reply_text(status_text)


# Inline query handler for previewing multitask status
@Client.on_callback_query(filters.regex("^preview_rename_task$"))
async def inline_preview_rename_task_callback(_, callback_query):
    await callback_query.answer()
    global RENAME_ENABLED
    status_text = "Rename is enabled." if RENAME_ENABLED else "Rename is disabled."
    await callback_query.message.reply_text(status_text)


# Inline query handler for previewing multitask status
@Client.on_callback_query(filters.regex("^preview_removetags_task$"))
async def inline_preview_removetags_task_callback(_, callback_query):
    await callback_query.answer()
    global REMOVETAGS_ENABLED
    status_text = "Remove Tags is enabled." if REMOVETAGS_ENABLED else "Remove Tags is disabled."
    await callback_query.message.reply_text(status_text)


# Inline query handler for previewing multitask status
@Client.on_callback_query(filters.regex("^preview_change_index_task$"))
async def inline_preview_change_index_task_callback(_, callback_query):
    await callback_query.answer()
    global CHANGE_INDEX_ENABLED
    status_text = "Change Index is enabled." if CHANGE_INDEX_ENABLED else "Change Index is disabled."
    await callback_query.message.reply_text(status_text)


@Client.on_callback_query(filters.regex("^back_to_settings$"))
async def back_to_settings_callback(client, callback_query: CallbackQuery):
    await display_user_settings(client, callback_query.message)


# Inline query handler for thumbnail settings
@Client.on_callback_query(filters.regex("^thumbnail_settings$"))
async def inline_thumbnail_settings(client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[            
            [InlineKeyboardButton("View Thumbnail", callback_data="view_thumbnail")],
            [InlineKeyboardButton("Delete Thumbnail", callback_data="delete_thumbnail")],
            [InlineKeyboardButton("Back to Settings", callback_data="back_to_settings")]
        ]
    )
    await callback_query.message.edit_text("Thumbnail Settings:", reply_markup=keyboard)



# Command to set a permanent thumbnail
@Client.on_message(filters.command("setthumbnail") & filters.group)
async def set_thumbnail_command(client, message):
    user_id = message.from_user.id
    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail_{user_id}.jpg"

    # Check if thumbnail already exists
    if os.path.isfile(thumbnail_path):
        await message.reply("You already have a permanent thumbnail set. Send a new photo to update it.")
    else:
        await message.reply("Send a photo to set as your permanent thumbnail.")

# Handler for setting the thumbnail
@Client.on_message(filters.photo & filters.group)
async def set_thumbnail_handler(client, message):
    user_id = message.from_user.id
    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail_{user_id}.jpg"

    # Check if thumbnail already exists
    if os.path.isfile(thumbnail_path):
        # Thumbnail exists, delete the old one
        os.remove(thumbnail_path)

    # Download the photo and save as thumbnail_{user_id}.jpg
    await client.download_media(message=message, file_name=thumbnail_path)
    await message.reply("Your permanent thumbnail is updated. If the bot is restarted, the new thumbnail will be preserved.")

# Command handler to view the current thumbnail
@Client.on_callback_query(filters.regex("^view_thumbnail$"))
async def view_thumbnail(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail_{user_id}.jpg"

    try:
        await callback_query.message.reply_photo(photo=thumbnail_path, caption="This is your current thumbnail")
    except Exception as e:
        logging.error(e)
        await callback_query.message.reply_text("You don't have any thumbnail.")

# Command handler to delete the current thumbnail
@Client.on_callback_query(filters.regex("^delete_thumbnail$"))
async def delete_thumbnail(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail_{user_id}.jpg"

    try:
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
            await callback_query.message.reply_text("Your thumbnail was removed ❌")
        else:
            await callback_query.message.reply_text("You don't have any thumbnail ‼️")
    except Exception as e:
        logging.error(e)
        await callback_query.message.reply_text("An error occurred while trying to remove your thumbnail. Please try again later.")


# Inline query handler to return to user settings
@Client.on_callback_query(filters.regex("^back_to_settings$"))
async def back_to_settings_callback(client, callback_query: CallbackQuery):
    await display_user_settings(client, callback_query.message)

# Command to set metadata titles
@Client.on_message(filters.command("setmetadata") & filters.group)
async def set_metadata_command(client, msg):
    global user_settings  # Ensure we're modifying the global user_settings

    # Extract titles from the command message
    if len(msg.command) < 2:
        await msg.reply_text("Invalid command format. Use: setmetadata video_title | audio_title | subtitle_title")
        return
    
    titles = msg.text.split(" ", 1)[1].split(" | ")
    if len(titles) != 3:
        await msg.reply_text("Invalid number of titles. Use: setmetadata video_title | audio_title | subtitle_title")
        return
    
    # Store the titles in user_settings
    user_id = msg.from_user.id
    user_settings[user_id] = {
        "video_title": titles[0].strip(),
        "audio_title": titles[1].strip(),
        "subtitle_title": titles[2].strip()
    }
    
    await msg.reply_text("Metadata titles set successfully.")




# RENAME
# Command handler for /rename command
@Client.on_message(filters.command("rename") & filters.group)
async def rename_file(bot, msg):
    global RENAME_ENABLED
    if not RENAME_ENABLED:
        return await msg.reply_text("The rename feature is currently disabled.")

    reply = msg.reply_to_message
    if len(msg.command) < 2 or not reply:
        return await msg.reply_text("Please Reply To A File, Video, or Audio With filename + .extension e.g., .mkv, .mp4, or .zip")
    
    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please Reply To A File, Video, or Audio With filename + .extension e.g., .mkv, .mp4, or .zip")
    
    new_name = msg.text.split(" ", 1)[1]
    sts = await msg.reply_text("🚀 Downloading... ⚡")
    c_time = time.time()
    downloaded = await reply.download(file_name=new_name, progress=progress_message, progress_args=("🚀 Download Started... ⚡️", sts, c_time)) 
    filesize = humanbytes(media.file_size)
    
    if CAPTION:
        try:
            cap = CAPTION.format(file_name=new_name, file_size=filesize)
        except Exception as e:            
            return await sts.edit(text=f"Your caption error: unexpected keyword ({e})")           
    else:
        cap = f"{new_name}\n\n🌟 Size: {filesize}"

    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail_{msg.from_user.id}.jpg"
    
    if os.path.exists(thumbnail_path):
        og_thumbnail = thumbnail_path
    else:
        try:
            og_thumbnail = await bot.download_media(media.thumbs[0].file_id, file_name=thumbnail_path)
        except Exception as e:
            logging.error(e)
            og_thumbnail = None

    await sts.edit("💠 Uploading... ⚡")
    c_time = time.time()
    try:
        await bot.send_document(msg.chat.id, document=downloaded, thumb=og_thumbnail, caption=cap, progress=progress_message, progress_args=("💠 Upload Started... ⚡", sts, c_time))        
    except Exception as e:  
        return await sts.edit(f"Error: {e}")                       
    try:
        os.remove(downloaded)
        if og_thumbnail and os.path.exists(og_thumbnail):
            os.remove(og_thumbnail)
    except Exception as e:
        logging.error(e)
    await sts.delete()

@Client.on_message(filters.command("rename"))
async def rename_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)
  


@Client.on_message(filters.command("multitask") & filters.group)
async def multitask_command(bot, msg):
    global MULTITASK_ENABLED

    if not MULTITASK_ENABLED:
        return await msg.reply_text("The multitask feature is currently disabled.")

    if len(msg.command) < 2:
        return await msg.reply_text("Please provide the required arguments\nFormat: `/multitask -m video_title | audio_title | subtitle_title -n new_filename.mkv`")

    command_text = " ".join(msg.command[1:]).strip()
    metadata = []
    new_filename = None

    # Extracting parameters
    if "-m" in command_text:
        metadata_part = command_text.split('-m')[1].split('-n')[0].strip()
        if '|' in metadata_part:
            metadata = list(map(str.strip, metadata_part.split('|')))
    
    if "-n" in command_text:
        try:
            new_filename_part = command_text.split('-n')[1].strip()
            if new_filename_part.lower().endswith(('.mkv', '.mp4', '.avi')):
                new_filename = new_filename_part
            else:
                raise ValueError("Invalid file extension. Please use a valid video file extension (e.g., .mkv, .mp4, .avi).")
        except IndexError:
            return await msg.reply_text("Please provide a valid filename with the -n option (e.g., `-n new_filename.mkv`).")
        except ValueError as ve:
            return await msg.reply_text(str(ve))

    if not metadata or not new_filename:
        return await msg.reply_text("Please provide all necessary arguments.\nFormat: `/multitask -m video_title | audio_title | subtitle_title -n new_filename.mkv`")

    reply = msg.reply_to_message
    if not reply:
        return await msg.reply_text("Please reply to a media file with the multitask command.")

    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please reply to a valid media file (audio, video, or document) with the multitask command.")

    sts = await msg.reply_text("🚀 Downloading media... ⚡")
    c_time = time.time()
    try:
        downloaded = await reply.download(progress=progress_message, progress_args=("🚀 Download Started... ⚡️", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error downloading media: {e}")
        return

    filesize = os.path.getsize(downloaded)
    filesize_human = humanbytes(filesize)

    video_title = metadata[0]
    audio_title = metadata[1]
    subtitle_title = metadata[2]

    cap = f"{new_filename}\n\n🌟 Size: {filesize_human}"

    thumbnail_path = f"{DOWNLOAD_LOCATION}/thumbnail_{msg.from_user.id}.jpg"
    
    if os.path.exists(thumbnail_path):
        og_thumbnail = thumbnail_path
    else:
        try:
            og_thumbnail = await bot.download_media(media.thumbs[0].file_id, file_name=thumbnail_path)
        except Exception as e:
            await sts.edit(f"Error downloading thumbnail: {e}")
            logging.error(e)
            og_thumbnail = None

    await sts.edit("💠 Changing metadata... ⚡")
    try:
        change_video_metadata(downloaded, video_title, audio_title, subtitle_title, new_filename)
    except Exception as e:
        await sts.edit(f"Error changing metadata: {e}")
        os.remove(downloaded)
        return

    await sts.edit("💠 Uploading cleaned file... ⚡")
    try:
        await bot.send_document(msg.chat.id, document=new_filename, thumb=og_thumbnail, caption=cap, progress=progress_message, progress_args=("💠 Upload Started... ⚡️", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error uploading cleaned file: {e}")
    finally:
        os.remove(downloaded)
        if og_thumbnail and os.path.exists(og_thumbnail):
            os.remove(og_thumbnail)
        await sts.delete()


@Client.on_message(filters.command("changemetadata") & filters.chat(GROUP))
async def change_metadata(bot, msg):
    global METADATA_ENABLED, user_settings

    if not METADATA_ENABLED:
        return await msg.reply_text("Metadata changing feature is currently disabled.")

    user_id = msg.from_user.id
    if user_id not in user_settings or not any(user_settings[user_id].values()):
        return await msg.reply_text("Metadata titles are not set. Please set metadata titles using `/setmetadata video_title audio_title subtitle_title`.")

    reply = msg.reply_to_message
    if not reply:
        return await msg.reply_text("Please reply to a media file with the metadata command\nFormat: `changemetadata -n filename.mkv`")

    if len(msg.command) < 3 or msg.command[1] != "-n":
        return await msg.reply_text("Please provide the filename with the `-n` flag\nFormat: `changemetadata -n filename.mkv`")

    # Join all parts of the command after the -n flag to handle filenames with spaces
    output_filename = " ".join(msg.command[2:]).strip()

    # Ensure output_filename has a valid extension
    if not output_filename.lower().endswith(('.mkv', '.mp4', '.avi')):
        return await msg.reply_text("Invalid file extension. Please use a valid video file extension (e.g., .mkv, .mp4, .avi).")

    video_title = user_settings[user_id]['video_title']
    audio_title = user_settings[user_id]['audio_title']
    subtitle_title = user_settings[user_id]['subtitle_title']

    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please reply to a valid media file (audio, video, or document) with the metadata command.")

    sts = await msg.reply_text("🚀 Downloading media... ⚡")
    c_time = time.time()
    try:
        downloaded = await reply.download(progress=progress_message, progress_args=("🚀 Download Started... ⚡️", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error downloading media: {e}")
        return

    output_file = os.path.join(DOWNLOAD_LOCATION, output_filename)

    await sts.edit("💠 Changing metadata... ⚡")
    try:
        change_video_metadata(downloaded, video_title, audio_title, subtitle_title, output_file)
    except Exception as e:
        await sts.edit(f"Error changing metadata: {e}")
        os.remove(downloaded)
        return

    filesize = os.path.getsize(output_file)
    filesize_human = humanbytes(filesize)
    cap = f"{output_filename}\n\n🌟 Size: {filesize_human}"

    await sts.edit("💠 Uploading... ⚡")
    c_time = time.time()
    try:
        await bot.send_document(msg.chat.id, document=output_file, caption=cap, progress=progress_message, progress_args=("💠 Upload Started... ⚡️", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error uploading: {e}")
    finally:
        os.remove(downloaded)
        os.remove(output_file)
        await sts.delete()


@Client.on_message(filters.command("changemetadata"))
async def metadata_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)  

# Command handler for attaching a photo
@Client.on_message(filters.command("attachphoto") & filters.group)
async def attach_photo(bot, msg):
    global PHOTO_ATTACH_ENABLED

    if not PHOTO_ATTACH_ENABLED:
        return await msg.reply_text("Photo attachment feature is currently disabled.")

    reply = msg.reply_to_message
    if not reply:
        return await msg.reply_text("Please reply to a media file with the attach photo command and specify the output filename\nFormat: `attachphoto -n filename.mkv`")

    if len(msg.command) < 2 or "-n" not in msg.text:
        return await msg.reply_text("Please provide the output filename using the `-n` flag\nFormat: `attachphoto -n filename.mkv`")

    command_text = " ".join(msg.command[1:]).strip()
    filename_part = command_text.split('-n', 1)[1].strip()
    output_filename = filename_part if filename_part else None

    if not output_filename:
        return await msg.reply_text("Please provide a valid filename\nFormat: `attachphoto -n filename.mkv`")

    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please reply to a valid media file (audio, video, or document) with the attach photo command.")

    sts = await msg.reply_text("🚀 Downloading media... ⚡")
    c_time = time.time()
    try:
        downloaded = await reply.download(progress=progress_message, progress_args=("🚀 Download Started... ⚡️", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error downloading media: {e}")
        return

    # Check if there is a previously set photo
    attachment_path =  f"{DOWNLOAD_LOCATION}/attachment_{msg.from_user.id}.jpg"
    if not os.path.exists(attachment_path):
        await sts.edit("Please send a photo to be attached using the `setphoto` command.")
        os.remove(downloaded)
        return

    output_file = os.path.join(DOWNLOAD_LOCATION, output_filename)

    await sts.edit("💠 Adding photo attachment... ⚡")
    try:
        add_photo_attachment(downloaded, attachment_path, output_file)
    except Exception as e:
        await sts.edit(f"Error adding photo attachment: {e}")
        os.remove(downloaded)
        return

    await sts.edit("🔼 Uploading modified file... ⚡")
    try:
        await bot.send_document(msg.chat.id, output_file, caption="Here is your file with the photo attachment.")
        await sts.delete()
    except Exception as e:
        await sts.edit(f"Error uploading modified file: {e}")
    finally:
        os.remove(downloaded)
        os.remove(output_file)

@Client.on_message(filters.command("attachphoto"))
async def attachphoto_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)
    
# Command handler for /removetags command
@Client.on_message(filters.command("removetags") & filters.group)
async def remove_tags(bot, msg):
    global REMOVETAGS_ENABLED
    if not REMOVETAGS_ENABLED:
        return await msg.reply_text("The removetags feature is currently disabled.")

    reply = msg.reply_to_message
    if not reply:
        return await msg.reply_text("Please reply to a media file with the removetags command.")

    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please reply to a valid media file (audio, video, or document) with the removetags command.")

    command_text = " ".join(msg.command[1:]).strip()
    new_filename = None

    # Extract new filename from command
    if "-n" in command_text:
        try:
            new_filename = command_text.split('-n')[1].strip()
        except IndexError:
            return await msg.reply_text("Please provide a valid filename with the -n option (e.g., `-n new_filename.mkv`).")

        # Check if new filename has a valid video file extension (.mkv, .mp4, .avi)
        valid_extensions = ('.mkv', '.mp4', '.avi')
        if not any(new_filename.lower().endswith(ext) for ext in valid_extensions):
            return await msg.reply_text("The new filename must include a valid extension (e.g., `.mkv`, `.mp4`, `.avi`).")

    sts = await msg.reply_text("🚀 Downloading media... ⚡")
    c_time = time.time()
    try:
        downloaded = await reply.download(progress=progress_message, progress_args=("🚀 Download Started... ⚡️", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error downloading media: {e}")
        return

    cleaned_file = os.path.join(DOWNLOAD_LOCATION, new_filename if new_filename else "cleaned_" + os.path.basename(downloaded))

    await sts.edit("💠 Removing all tags... ⚡")
    try:
        remove_all_tags(downloaded, cleaned_file)
    except Exception as e:
        await sts.edit(f"Error removing all tags: {e}")
        os.remove(downloaded)
        return

    file_thumb = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
    if not os.path.exists(file_thumb):
        try:
            file_thumb = await bot.download_media(media.thumbs[0].file_id)
        except Exception as e:
            print(e)
            file_thumb = None

    await sts.edit("🔼 Uploading cleaned file... ⚡")
    try:
        await bot.send_document(msg.chat.id, cleaned_file, thumb=file_thumb, caption="Here is your file with all tags removed.", progress=progress_message, progress_args=("🔼 Upload Started... ⚡️", sts, c_time))
        await sts.delete()
    except Exception as e:
        await sts.edit(f"Error uploading cleaned file: {e}")
    finally:
        os.remove(downloaded)
        os.remove(cleaned_file)
        if file_thumb and os.path.exists(file_thumb):
            os.remove(file_thumb)

@Client.on_message(filters.command("changeindex") & filters.chat(GROUP))
async def change_index(bot, msg):
    global CHANGE_INDEX_ENABLED

    if not CHANGE_INDEX_ENABLED:
        return await msg.reply_text("The changeindex feature is currently disabled.")

    reply = msg.reply_to_message
    if not reply:
        return await msg.reply_text("Please reply to a media file with the index command\nFormat: `/changeindex a-3 -n filename.mkv` (Audio)")

    if len(msg.command) < 3:
        return await msg.reply_text("Please provide the index command with a filename\nFormat: `/changeindex a-3 -n filename.mkv` (Audio)")

    index_cmd = None
    output_filename = None

    for i in range(1, len(msg.command)):
        if msg.command[i] == "-n":
            output_filename = " ".join(msg.command[i + 1:])  # Join all the parts after the flag
            break

    index_cmd = " ".join(msg.command[1:i])  # Get the index command before the flag

    if not output_filename:
        return await msg.reply_text("Please provide a filename using the `-n` flag.")

    if not index_cmd or not index_cmd.startswith("a-"):
        return await msg.reply_text("Invalid format. Use `/changeindex a-3 -n filename.mkv` for audio.")

    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please reply to a valid media file (audio, video, or document) with the index command.")

    sts = await msg.reply_text("🚀Downloading media...⚡")
    c_time = time.time()
    try:
        downloaded = await reply.download(progress=progress_message, progress_args=("Downloading", sts, c_time))
    except Exception as e:
        await sts.edit(f"Error downloading media: {e}")
        return

    output_file = os.path.join(DOWNLOAD_LOCATION, output_filename)

    index_params = index_cmd.split('-')
    stream_type = index_params[0]
    indexes = [int(i) - 1 for i in index_params[1:]]

    ffmpeg_cmd = ['ffmpeg', '-i', downloaded, '-map', '0:v']  # Always map video stream

    for idx in indexes:
        ffmpeg_cmd.extend(['-map', f'0:{stream_type}:{idx}'])

    # Copy all subtitle streams if they exist
    ffmpeg_cmd.extend(['-map', '0:s?'])

    ffmpeg_cmd.extend(['-c', 'copy', output_file, '-y'])

    await sts.edit("💠Changing indexing...⚡")
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        await sts.edit(f"❗FFmpeg error: {stderr.decode('utf-8')}")
        os.remove(downloaded)
        return

    # Thumbnail handling
    file_thumb = None
    if media.thumbs:
        try:
            file_thumb = await bot.download_media(media.thumbs[0].file_id, file_name=f"{DOWNLOAD_LOCATION}/thumbnail.jpg")
            print("Thumbnail downloaded successfully:", file_thumb)  # Debug print
        except Exception as e:
            print(f"Error downloading thumbnail: {e}")
            file_thumb = None

    filesize = os.path.getsize(output_file)
    filesize_human = humanbytes(filesize)
    cap = f"{output_filename}\n\n🌟Size: {filesize_human}"

    await sts.edit("💠Uploading...⚡")
    c_time = time.time()
    try:
        await bot.send_document(
            msg.chat.id, 
            document=output_file, 
            thumb=file_thumb, 
            caption=cap, 
            progress=progress_message, 
            progress_args=("Uploading", sts, c_time)
        )
        await sts.delete()
    except RPCError as e:
        await sts.edit(f"Upload failed: {e}")
    except TimeoutError as e:
        await sts.edit(f"Upload timed out: {e}")
    finally:
        try:
            if file_thumb:
                os.remove(file_thumb)
            os.remove(downloaded)
            os.remove(output_file)
        except Exception as e:
            print(f"Error deleting files: {e}")

def remove_all_tags(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-map', '0',
        '-map_metadata', '-1',  # This removes all metadata
        '-c', 'copy',
        output_path,
        '-y'
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {stderr.decode('utf-8')}")


@Client.on_message(filters.command("linktofile") & filters.chat(AUTH_USERS))
async def linktofile(bot, msg: Message):
    reply = msg.reply_to_message
    if len(msg.command) < 2 or not reply:
        return await msg.reply_text("Please Reply To A File, Video, Audio, or Link With filename + .extension (e.g., `.mkv`, `.mp4`, or `.zip`)")

    new_name = msg.text.split(" ", 1)[1]

    media = reply.document or reply.audio or reply.video
    if not media and not reply.text:
        return await msg.reply_text("Please Reply To A File, Video, Audio, or Link With filename + .extension (e.g., `.mkv`, `.mp4`, or `.zip`)")

    if reply.text and ("seedr" in reply.text or "workers" in reply.text):
        await handle_link_download(bot, msg, reply.text, new_name)
    else:
        if not media:
            return await msg.reply_text("Please Reply To A Valid File, Video, Audio, or Link With filename + .extension (e.g., `.mkv`, `.mp4`, or `.zip`)")

        og_media = getattr(reply, reply.media.value)
        sts = await msg.reply_text("🚀 Downloading...")
        c_time = time.time()
        try:
            downloaded = await reply.download(file_name=new_name, progress=progress_message, progress_args=("🚀 Download Started...", sts, c_time))
        except RPCError as e:
            return await sts.edit(f"Download failed: {e}")

        filesize = humanbytes(og_media.file_size)

        if CAPTION:
            try:
                cap = CAPTION.format(file_name=new_name, file_size=filesize)
            except Exception as e:
                return await sts.edit(text=f"Your caption has an error: unexpected keyword ●> ({e})")
        else:
            cap = f"{new_name}\n\n🌟 Size: {filesize}"

        # Thumbnail handling
        file_thumb = None
        if og_media.thumbs:
            try:
                file_thumb = await bot.download_media(og_media.thumbs[0].file_id, file_name=f"{DOWNLOAD_LOCATION}/{new_name}_thumb.jpg")
            except Exception as e:
                print(f"Error downloading thumbnail: {e}")
                file_thumb = None

        await sts.edit("💠 Uploading...")
        c_time = time.time()
        try:
            await bot.send_document(
                msg.chat.id, 
                document=downloaded, 
                thumb=file_thumb, 
                caption=cap, 
                progress=progress_message, 
                progress_args=("💠 Upload Started...", sts, c_time)
            )
        except RPCError as e:
            await sts.edit(f"Upload failed: {e}")
        except TimeoutError as e:
            await sts.edit(f"Upload timed out: {e}")
        finally:
            try:
                if file_thumb:
                    os.remove(file_thumb)
                os.remove(downloaded)
            except Exception as e:
                print(f"Error deleting files: {e}")
            await sts.delete()
          
async def handle_link_download(bot, msg: Message, link: str, new_name: str):
    sts = await msg.reply_text("🚀 Downloading from link...")
    c_time = time.time()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status == 200:
                    with open(new_name, 'wb') as f:
                        f.write(await resp.read())
                else:
                    await sts.edit(f"Failed to download file from link. Status code: {resp.status}")
                    return
    except Exception as e:
        await sts.edit(f"Error during download: {e}")
        return

    if not os.path.exists(new_name):
        await sts.edit("File not found after download. Please check the link and try again.")
        return

    filesize = os.path.getsize(new_name)
    filesize = humanbytes(filesize)

    if CAPTION:
        try:
            cap = CAPTION.format(file_name=new_name, file_size=filesize)
        except Exception as e:
            await sts.edit(text=f"Your caption has an error: unexpected keyword ●> ({e})")
            return
    else:
        cap = f"{new_name}\n\n🌟 Size: {filesize}"

    await sts.edit("💠 Uploading...")
    c_time = time.time()
    try:
        await bot.send_document(msg.chat.id, document=new_name, caption=cap, progress=progress_message, progress_args=("💠 Upload Started...", sts, c_time))
    except RPCError as e:
        await sts.edit(f"Upload failed: {e}")
    except TimeoutError as e:
        await sts.edit(f"Upload timed out: {e}")
    finally:
        try:
            os.remove(new_name)
        except Exception as e:
            print(f"Error deleting file: {e}")
        await sts.delete()

            

 
 # Define restart_app command
@Client.on_message(filters.command("restart") & filters.chat(GROUP))
async def restart_app(bot, msg):
    if not f'{msg.from_user.id}' == f'{int(AUTH_USERS)}':
        return await msg.reply_text("Only authorized user can restart!")

    result = await heroku_restart()
    if result is None:
        return await msg.reply_text("You have not filled `HEROKU_API` and `HEROKU_APP_NAME` vars.")
    elif result is False:
        return await msg.reply_text("An error occurred!")
    elif result is True:
        return await msg.reply_text("Restarting app, wait for a minute.")
        



@Client.on_message(filters.command("changeindex"))
async def changeindex_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)
    
def change_video_metadata(input_path, video_title, audio_title, subtitle_title, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-metadata', f'title={video_title}',
        '-metadata:s:v', f'title={video_title}',
        '-metadata:s:a', f'title={audio_title}',
        '-metadata:s:s', f'title={subtitle_title}',
        '-map', '0:v?',
        '-map', '0:a?',
        '-map', '0:s?',
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-c:s', 'copy',
        output_path,
        '-y'
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {stderr.decode('utf-8')}")


            


    
 # Sample Video Generation Function
def generate_sample_video(input_path, duration, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-t', str(duration),
        '-c:v', 'copy',
        '-c:a', 'copy',
        output_path,
        '-y'
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {stderr.decode('utf-8')}")

# Sample Video Handler
@Client.on_message(filters.command(["samplevideo150", "samplevideo120", "samplevideo90", "samplevideo60", "samplevideo30"]) & filters.chat(GROUP))
async def sample_video(bot, msg):
    durations = {
        "samplevideo150": 150,
        "samplevideo120": 120,
        "samplevideo90": 90,
        "samplevideo60": 60,
        "samplevideo30": 30
    }
    duration = durations.get(msg.command[0], 0)
    if duration == 0:
        return await msg.reply_text("Invalid command")

    if not msg.reply_to_message:
        return await msg.reply_text("Please reply to a valid video file or document.")

    media = msg.reply_to_message.video or msg.reply_to_message.document
    if not media:
        return await msg.reply_text("Please reply to a valid video file or document.")

    sts = await msg.reply_text("🚀Downloading media...⚡")
    c_time = time.time()
    input_path = await bot.download_media(media, progress=progress_message, progress_args=("🚀Downloading media...⚡️", sts, c_time))
    output_file = os.path.join(DOWNLOAD_LOCATION, f"sample_video_{duration}s.mp4")

    await sts.edit("🚀Processing sample video...⚡")
    try:
        generate_sample_video(input_path, duration, output_file)
    except Exception as e:
        await sts.edit(f"Error generating sample video: {e}")
        os.remove(input_path)
        return

    filesize = os.path.getsize(output_file)
    filesize_human = humanbytes(filesize)
    cap = f"{os.path.basename(output_file)}\n\n🌟Size: {filesize_human}"

    await sts.edit("💠Uploading sample video...⚡")
    c_time = time.time()
    try:
        await bot.send_document(msg.chat.id, document=output_file, caption=cap, progress=progress_message, progress_args=("💠Upload Started.....", sts, c_time))
    except Exception as e:
        return await sts.edit(f"Error {e}")

    os.remove(input_path)
    os.remove(output_file)
    await sts.delete()       

@Client.on_message(filters.command(["samplevideo150", "samplevideo120", "samplevideo90", "samplevideo60", "samplevideo30"]))
async def samplevideo_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)     
    
# Screenshots by Number Handler
@Client.on_message(filters.command("screenshots") & filters.chat(GROUP))
async def screenshots(bot, msg):
    if len(msg.command) != 2:
        return await msg.reply_text("Please provide the number of screenshots to generate.")
    
    try:
        num_screenshots = int(msg.command[1])
        if num_screenshots <= 0:
            return await msg.reply_text("Number of screenshots must be a positive integer.")
    except ValueError:
        return await msg.reply_text("Please provide a valid number of screenshots.")

    if not msg.reply_to_message:
        return await msg.reply_text("Please reply to a valid video file or document.")
    
    media = msg.reply_to_message.video or msg.reply_to_message.document
    if not media:
        return await msg.reply_text("Please reply to a valid video file.")

    sts = await msg.reply_text("🚀Downloading media...⚡")
    c_time = time.time()
    input_path = await bot.download_media(media, progress=progress_message, progress_args=("🚀Downloading media...⚡️", sts, c_time))

    if not os.path.exists(input_path):
        await sts.edit(f"Error: The downloaded file does not exist.")
        return

    try:
        await sts.edit("🚀Reading video duration...⚡")
        command = [
            'ffprobe', '-i', input_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'
        ]
        duration_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        duration = float(duration_output.decode('utf-8').strip())
    except subprocess.CalledProcessError as e:
        await sts.edit(f"Error reading video duration: {e.output.decode('utf-8')}")
        os.remove(input_path)
        return
    except ValueError:
        await sts.edit("Error reading video duration: Unable to convert duration to float.")
        os.remove(input_path)
        return

    interval = duration / num_screenshots

    await sts.edit("🚀Generating screenshots... It's Take Time 5Min for 10 Screenshots⚡")
    screenshot_paths = []
    for i in range(num_screenshots):
        time_position = interval * i
        screenshot_path = os.path.join(DOWNLOAD_LOCATION, f"screenshot_{i}.jpg")
        command = [
            'ffmpeg', '-i', input_path, '-ss', str(time_position), '-vframes', '1', screenshot_path, '-y'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            await sts.edit(f"Error generating screenshot {i+1}: {stderr.decode('utf-8')}")
            os.remove(input_path)
            for path in screenshot_paths:
                os.remove(path)
            return
        screenshot_paths.append(screenshot_path)

    await sts.edit("💠Uploading screenshots...⚡")
    for i, screenshot_path in enumerate(screenshot_paths):
        try:
            await bot.send_photo(msg.chat.id, photo=screenshot_path)
        except Exception as e:
            await sts.edit(f"Error uploading screenshot {i+1}: {e}")
            os.remove(screenshot_path)

    os.remove(input_path)
    for screenshot_path in screenshot_paths:
        os.remove(screenshot_path)
    await sts.delete()

@Client.on_message(filters.command("screenshots"))
async def screenshots_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)     
    
# Function to unzip files
def unzip_file(file_path, extract_path):
    extracted_files = []
    try:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                extracted_files = zip_ref.namelist()
        # Add support for other archive formats here if needed
    except Exception as e:
        print(f"Error unzipping file: {e}")
    return extracted_files

# Recursive function to upload files
async def upload_files(bot, chat_id, directory, base_path=""):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            try:
                await bot.send_document(chat_id, document=item_path, caption=item)
            except Exception as e:
                print(f"Error uploading {item}: {e}")
        elif os.path.isdir(item_path):
            await upload_files(bot, chat_id, item_path, base_path=os.path.join(base_path, item))

# Unzip file command handler
@Client.on_message(filters.command("unzip") & filters.chat(GROUP))
async def unzip(bot, msg):
    if not msg.reply_to_message:
        return await msg.reply_text("Please reply to a zip file to unzip.")

    media = msg.reply_to_message.document
    if not media:
        return await msg.reply_text("Please reply to a valid zip file.")

    sts = await msg.reply_text("🚀Downloading file...⚡")
    c_time = time.time()
    input_path = await bot.download_media(media, progress
                                          =progress_message, progress_args=("🚀Downloading file...⚡️", sts, c_time))

    if not os.path.exists(input_path):
        await sts.edit(f"Error: The downloaded file does not exist.")
        return

    extract_path = os.path.join(DOWNLOAD_LOCATION, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    await sts.edit("🚀Unzipping file...⚡")
    extracted_files = unzip_file(input_path, extract_path)

    if extracted_files:
        await sts.edit(f"✅ File unzipped successfully. Uploading extracted files...⚡")
        await upload_files(bot, msg.chat.id, extract_path)
        await sts.edit(f"✅ All extracted files uploaded successfully.")
    else:
        await sts.edit(f"❌ Failed to unzip file.")

    os.remove(input_path)
    shutil.rmtree(extract_path)

@Client.on_message(filters.command("unzip"))
async def unzip_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)    


def add_photo_attachment(input_path, attachment_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-map', '0:v?',
        '-map', '0:a?',
        '-map', '0:s?',
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-c:s', 'copy',
        '-attach', attachment_path,
        '-metadata:s:t', 'mimetype=image/jpeg',
        output_path,
        '-y'
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {stderr.decode('utf-8')}")



# Handler for setting the photo with user ID
@Client.on_message(filters.command("setphoto"))
async def set_photo(bot, msg):
    reply = msg.reply_to_message
    if not reply or not reply.photo:
        return await msg.reply_text("Please reply to a photo with the set photo command")

    user_id = msg.from_user.id
    photo = reply.photo
    attachment_path = os.path.join(DOWNLOAD_LOCATION, f"attachment_{user_id}.jpg")
    try:
        await bot.download_media(photo, attachment_path)
        await msg.reply_text(f"Photo saved successfully as `{attachment_path}`.")
    except Exception as e:
        await msg.reply_text(f"Error saving photo: {e}")


"""
@Client.on_message(filters.command("setphoto"))
async def setphoto_private(client, message):
  buttons = [[
    InlineKeyboardButton("GROUP", url="https://t.me/INFINITYRENAME24GROUP")
  ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await message.reply_text(text=f"ʜᴇʏ {message.from_user.mention}\nTʜɪꜱ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ Wᴏʀᴋ Iɴ Mʏ Gʀᴏᴜᴘ", reply_markup=reply_markup)"""

if __name__ == '__main__':
    app = Client("my_bot", bot_token=BOT_TOKEN)
    app.run()