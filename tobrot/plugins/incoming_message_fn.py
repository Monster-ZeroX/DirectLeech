#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | Akshay C

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


import os
import requests

from tobrot import (
    DOWNLOAD_LOCATION
)


import time
import aria2p
import asyncio
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function, call_apropriate_function_g, aria_start
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.ytplaylist import yt_playlist_downg
from tobrot.helper_funcs.cloneHelper import CloneHelper
from tobrot.helper_funcs.download import download_tg
from tobrot.helper_funcs.upload_to_tg import upload_to_tg

async def incoming_purge_message_f(client, message):
    """/purge command"""
    i_m_sefg2 = await message.reply_text("Purging...", quote=True)
    if await AdminCheck(client, message.chat.id, message.from_user.id):
        aria_i_p = await aria_start()
        # Show All Downloads
        downloads = aria_i_p.get_downloads()
        for download in downloads:
            LOGGER.info(download.remove(force=True))
    await i_m_sefg2.delete()

async def incoming_message_f(client, message):
    """/leech command"""
    g_id = message.from_user.id
    credit = await message.reply_text(f"🧲 Leeching for you <a href='tg://user?id={g_id}'>🤕</a>", parse_mode="html")
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    is_unzip = False
    is_unrar = False
    is_untar = False
    if len(message.command) > 1:
        if message.command[1].lower() == "archive":
            is_zip = True
        elif message.command[1].lower() == "unzip":
            is_unzip = True
        elif message.command[1].lower() == "unrar":
            is_unrar = True
        elif message.command[1].lower() == "untar":
            is_untar = True
    # get link from the incoming message
    dl_url, cf_name, _, _ = await extract_link(message.reply_to_message, "LEECH")
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        # start the aria2c daemon
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        current_user_id = message.from_user.id
        # create an unique directory
        new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(time.time())
        )
        # create download directory, if not exist
        if not os.path.isdir(new_download_location):
            os.makedirs(new_download_location)
        await i_m_sefg.edit_text("trying to download")
        # try to download the "link"
        sagtus, err_message = await call_apropriate_function(
            aria_i_p,
            dl_url,
            new_download_location,
            i_m_sefg,
            is_zip,
            cf_name,
            is_unzip,
            is_unrar,
            is_untar,
            message
        )
        if not sagtus:
            # if FAILED, display the error message
            await i_m_sefg.edit_text(err_message)
    else:
        await i_m_sefg.edit_text(
            "**FCUK**! wat have you entered. \nPlease read /help \n"
            f"<b>API Error</b>: {cf_name}"
        )
#
async def incoming_gdrive_message_f(client, message):
    """/gleech command"""
    g_id = message.from_user.id
    credit = await message.reply_text(f"🧲 Leeching for you <a href='tg://user?id={g_id}'>🤕</a>", parse_mode="html")
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    is_unzip = False
    is_unrar = False
    is_untar = False
    if len(message.command) > 1:
        if message.command[1].lower() == "archive":
            is_zip = True
        elif message.command[1].lower() == "unzip":
            is_unzip = True
        elif message.command[1].lower() == "unrar":
            is_unrar = True
        elif message.command[1].lower() == "untar":
            is_untar = True
    # get link from the incoming message
    dl_url, cf_name, _, _ = await extract_link(message.reply_to_message, "GLEECH")
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        # start the aria2c daemon
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        current_user_id = message.from_user.id
        # create an unique directory
        new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(time.time())
        )
        # create download directory, if not exist
        if not os.path.isdir(new_download_location):
            os.makedirs(new_download_location)
        await i_m_sefg.edit_text("trying to download")
        # try to download the "link"
        await call_apropriate_function_g(
            aria_i_p,
            dl_url,
            new_download_location,
            i_m_sefg,
            is_zip,
            cf_name,
            is_unzip,
            is_unrar,
            is_untar,
            message
        )
    else:
        await i_m_sefg.edit_text(
            "**FCUK**! wat have you entered. \nPlease read /help \n"
            f"<b>API Error</b>: {cf_name}"
        )


async def incoming_youtube_dl_f(client, message):
    """ /ytdl command """
    g_id = message.from_user.id
    credit = await message.reply_text(f"💀 Downloading for you <a href='tg://user?id={g_id}'>🤕</a>", parse_mode="html")
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = await extract_link(
        message.reply_to_message, "YTDL"
    )
    LOGGER.info(dl_url)
    #if len(message.command) > 1:
        #if message.command[1] == "gdrive":
            #with open('blame_my_knowledge.txt', 'w+') as gg:
                #gg.write("I am noob and don't know what to do that's why I have did this")
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            cf_name,
            yt_dl_user_name,
            yt_dl_pass_word,
            user_working_dir
        )
        print(thumb_image)
        req = requests.get(f"{thumb_image}")
        gau_tam = f"{current_user_id}.jpg"
        open(gau_tam, 'wb').write(req.content)
        if thumb_image is not None:
            await message.reply_photo(
                #text_message,
                photo=gau_tam,
                quote=True,
                caption=text_message,
                reply_markup=reply_markup
            )
            await i_m_sefg.delete()
        else:
            await i_m_sefg.edit_text(
                text=text_message,
                reply_markup=reply_markup
            )
    else:
        await i_m_sefg.edit_text(
            "**FCUK**! wat have you entered. \nPlease read /help \n"
            f"<b>API Error</b>: {cf_name}"
        )
#playlist
async def g_yt_playlist(client, message):
    """ /pytdl command """
    #i_m_sefg = await message.reply_text("Processing...you should wait🤗", quote=True)
    usr_id = message.from_user.id
    G_DRIVE = False
    if len(message.command) > 1:
        if message.command[1] == "gdrive":
            G_DRIVE = True
    if 'youtube.com/playlist' in message.reply_to_message.text:
        i_m_sefg = await message.reply_text("Downloading...you should wait🤗", quote=True)
        await yt_playlist_downg(message.reply_to_message, i_m_sefg, G_DRIVE)
    
    else:
        await message.reply_text("Reply to youtube playlist link only 🙄")
        
 #
async def g_clonee(client, message):
    """ /gclone command """
    g_id = message.from_user.id
    if message.reply_to_message is not None:
        LOGGER.info(message.reply_to_message.text)
        gclone = CloneHelper(message)
        gclone.config()
        a, h = gclone.get_id()
        LOGGER.info(a)
        LOGGER.info(h)
        await gclone.gcl()
        await gclone.link_gen_size()
    else:
        await message.reply_text("You should reply to a message, which format should be [ID of Gdrive file/folder Name of the file/folder]\nOr read Github for detailled information")


async def rename_tg_file(client, message):
    usr_id = message.from_user.id
    if len(message.command) > 1:
        new_name = '/app/' + message.text.split(" ", maxsplit=1)[1].strip()
        file = await download_tg(client, message)
        try:
            if file:
                os.rename(file, new_name)
        except Exception as g_g:
            await message.reply_text("g_g")
        response = {}
        final_response = await upload_to_tg(
            message,
            new_name,
            usr_id,
            response
        )
        LOGGER.info(final_response)
        try:
            message_to_send = ""
            for key_f_res_se in final_response:
                local_file_name = key_f_res_se
                message_id = final_response[key_f_res_se]
                channel_id = str(message.chat.id)[4:]
                private_link = f"https://t.me/c/{channel_id}/{message_id}"
                message_to_send += "👉 <a href='"
                message_to_send += private_link
                message_to_send += "'>"
                message_to_send += local_file_name
                message_to_send += "</a>"
                message_to_send += "\n"
            if message_to_send != "":
                mention_req_user = f"<a href='tg://user?id={usr_id}'>Your Requested Files</a>\n\n"
                message_to_send = mention_req_user + message_to_send
                message_to_send = message_to_send + "\n\n" + "#uploads"
            else:
                message_to_send = "<i>FAILED</i> to upload files. 😞😞"
            await message.reply_text(
                text=message_to_send,
                quote=True,
                disable_web_page_preview=True
            )
        except Exception as pe:
            LOGGER.info(pe)

    else:
        await message.reply_text("Provide new name of the file with extension 😐")