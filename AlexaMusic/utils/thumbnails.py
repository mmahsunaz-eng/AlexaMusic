# Copyright (C) 2025 by Onlyforacha Project
# Modified from Alexa_Help @ Github, <https://github.com/TheTeamAlexa>
# All rights reserved. © Onlyforacha © Acha

"""
Onlyforacha X Bot Thumbnail Generator
Customized version with neon glow style and logo integration.
"""

import os
import re
import textwrap
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


def draw_glow_text(draw, text, position, font, glow_color, text_color, glow_radius=4):
    # simple glow effect by drawing blurred layers behind text
    x, y = position
    for offset in range(glow_radius, 0, -1):
        draw.text((x - offset, y), text, font=font, fill=glow_color)
        draw.text((x + offset, y), text, font=font, fill=glow_color)
        draw.text((x, y - offset), text, font=font, fill=glow_color)
        draw.text((x, y + offset), text, font=font, fill=glow_color)
    draw.text(position, text, font=font, fill=text_color)


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            title = re.sub(r"\W+", " ", result.get("title", "Unknown Title")).title()
            duration = result.get("duration", "Unknown Mins")
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                        await f.write(await resp.read())

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")

        # blur background
        background = image2.filter(ImageFilter.GaussianBlur(15))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        # crop and paste logo thumbnail
        Xcenter, Ycenter = youtube.width / 2, youtube.height / 2
        logo_crop = youtube.crop((Xcenter - 250, Ycenter - 250, Xcenter + 250, Ycenter + 250))
        logo_crop.thumbnail((520, 520), Image.LANCZOS)
        logo_crop = ImageOps.expand(logo_crop, border=15, fill="white")
        background.paste(logo_crop, (50, 100))

        draw = ImageDraw.Draw(background)
        font_small = ImageFont.truetype("assets/font2.ttf", 40)
        font_big = ImageFont.truetype("assets/font2.ttf", 70)
        font_info = ImageFont.truetype("assets/font2.ttf", 30)
        name_font = ImageFont.truetype("assets/font.ttf", 35)

        # glow colors
        glow_color = (255, 0, 255)
        text_color = (255, 255, 255)

        # logo Onlyforacha
        logo_path = "AlexaMusic/utils/file_00000000e5e462088641d9a6402214ca.png"
        if os.path.exists(logo_path):
            bot_logo = Image.open(logo_path).convert("RGBA")
            bot_logo.thumbnail((250, 250), Image.LANCZOS)
            background.paste(bot_logo, (1000, 30), bot_logo)

        # header name
        draw_glow_text(draw, "Onlyforacha X Bot", (30, 20), name_font, glow_color, text_color)

        # now playing text
        draw_glow_text(draw, "NOW PLAYING", (600, 150), font_big, glow_color, text_color)

        # title text wrapping
        for i, line in enumerate(textwrap.wrap(title, width=30)):
            draw_glow_text(draw, line, (600, 280 + (i * 60)), font_small, glow_color, text_color)

        # video details
        draw.text((600, 450), f"Views : {views}", fill=text_color, font=font_info)
        draw.text((600, 500), f"Duration : {duration}", fill=text_color, font=font_info)
        draw.text((600, 550), "Owner : Acha", fill=text_color, font=font_info)

        os.remove(f"cache/thumb{videoid}.png")
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception:
        return YOUTUBE_IMG_URL


async def gen_qthumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            title = re.sub(r"\W+", " ", result.get("title", "Unknown Title")).title()
            duration = result.get("duration", "Unknown Mins")
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                        await f.write(await resp.read())

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")

        background = image2.filter(ImageFilter.GaussianBlur(15))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        Xcenter, Ycenter = youtube.width / 2, youtube.height / 2
        logo_crop = youtube.crop((Xcenter - 250, Ycenter - 250, Xcenter + 250, Ycenter + 250))
        logo_crop.thumbnail((520, 520), Image.LANCZOS)
        logo_crop = ImageOps.expand(logo_crop, border=15, fill="white")
        background.paste(logo_crop, (50, 100))

        draw = ImageDraw.Draw(background)
        font_small = ImageFont.truetype("assets/font2.ttf", 40)
        font_big = ImageFont.truetype("assets/font2.ttf", 65)
        font_info = ImageFont.truetype("assets/font2.ttf", 30)
        name_font = ImageFont.truetype("assets/font.ttf", 35)

        glow_color = (255, 0, 255)
        text_color = (255, 255, 255)

        logo_path = "AlexaMusic/utils/file_00000000e5e462088641d9a6402214ca.png"
        if os.path.exists(logo_path):
            bot_logo = Image.open(logo_path).convert("RGBA")
            bot_logo.thumbnail((250, 250), Image.LANCZOS)
            background.paste(bot_logo, (1000, 30), bot_logo)

        draw_glow_text(draw, "Onlyforacha X Bot", (30, 20), name_font, glow_color, text_color)
        draw_glow_text(draw, "ADDED TO QUEUE", (600, 150), font_big, glow_color, text_color)

        for i, line in enumerate(textwrap.wrap(title, width=30)):
            draw_glow_text(draw, line, (600, 280 + (i * 60)), font_small, glow_color, text_color)

        draw.text((600, 450), f"Views : {views}", fill=text_color, font=font_info)
        draw.text((600, 500), f"Duration : {duration}", fill=text_color, font=font_info)
        draw.text((600, 550), "Owner : Acha", fill=text_color, font=font_info)

        os.remove(f"cache/thumb{videoid}.png")
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception:
        return YOUTUBE_IMG_URL
