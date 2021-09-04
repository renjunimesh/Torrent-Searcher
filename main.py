# (c) @AbirHasan2005 & Jigar Varma & Hemanta Pokharel & Akib Hridoy

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from configs import Config
from tool import SearchYTS, SearchAnime, Search1337x, SearchPirateBay

TorrentBot = Client(session_name=Config.SESSION_NAME, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
DEFAULT_SEARCH_MARKUP = [
                    [InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐘𝐓𝐒", switch_inline_query_current_chat="!yts "),
                     InlineKeyboardButton("𝐆𝐨 𝐈𝐧𝐥𝐢𝐧𝐞", switch_inline_query="!yts ")],
                    [InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐓𝐡𝐞𝐏𝐢𝐫𝐚𝐭𝐞𝐁𝐚𝐲", switch_inline_query_current_chat="!pb "),
                     InlineKeyboardButton("𝐆𝐨 𝐈𝐧𝐥𝐢𝐧𝐞", switch_inline_query="!pb ")],
                    [InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝟏𝟑𝟑𝟕𝐱", switch_inline_query_current_chat=""),
                     InlineKeyboardButton("𝐆𝐨 𝐈𝐧𝐥𝐢𝐧𝐞", switch_inline_query="")],
                    [InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐀𝐧𝐢𝐦𝐞", switch_inline_query_current_chat="!a "),
                     InlineKeyboardButton("𝐆𝐎 𝐈𝐧𝐥𝐢𝐧𝐞", switch_inline_query_current_chat="!a ")],
                    [InlineKeyboardButton("⭕ 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ⭕", url="https://t.me/TeleRoidGroup"),
                     InlineKeyboardButton("⭕ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ⭕", url="https://t.me/TeleRoid14")],
                    [InlineKeyboardButton("👤 𝐇𝐞𝐥𝐩 👤", callback_data="")]
                ]


@TorrentBot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    try:
        await message.reply_text(
            text=Config.HOME_TEXT,
            disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
        )
    except FloodWait as e:
        print(f"[{Config.SESSION_NAME}] - Sleeping for {e.x}s")
        await asyncio.sleep(e.x)
        await start_handler(_, message)


@TorrentBot.on_inline_query()
async def inline_handlers(_, inline: InlineQuery):
    search_ts = inline.query
    answers = []
    if search_ts == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search Something ...",
                description="Search For Torrents ...",
                input_message_content=InputTextMessageContent(
                    message_text="Search for Torrents from Inline!",
                    parse_mode="Markdown"
                ),
                reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
            )
        )
    elif search_ts.startswith("!pb"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!pb [text]",
                    description="Search For Torrent in ThePirateBay ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!pb [text]`\n\nSearch ThePirateBay Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pb ")]])
                )
            )
        else:
            torrentList = await SearchPirateBay(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found in ThePirateBay!",
                        description=f"Can't find torrents for {query} in ThePirateBay !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Torrents Found For `{query}` in ThePirateBay !!",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pb ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                                             f"**𝐍𝐚𝐦𝐞:** `{torrentList[i]['Seeders']}`\n"
                                             f"**𝐒𝐢𝐳𝐞:** `{torrentList[i]['Size']}`\n"
                                             f"**𝐒𝐞𝐞𝐝𝐞𝐫𝐬:** `{torrentList[i]['Seeders']}`\n"
                                             f"**𝐋𝐞𝐞𝐜𝐡𝐞𝐫𝐬:** `{torrentList[i]['Leechers']}`\n"
                                             f"**𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐫:** `{torrentList[i]['Uploader']}`\n"
                                             f"**𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐨𝐧 {torrentList[i]['Date']}**\n\n"
                                             f"**𝐌𝐚𝐠𝐧𝐞𝐭:**\n`{torrentList[i]['Magnet']}`\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="!pb ")]])
                        )
                    )
    elif search_ts.startswith("!yts"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!yts [text]",
                    description="Search For Torrent in YTS ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!yts [text]`\n\nSearch YTS Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="!yts ")]])
                )
            )
        else:
            torrentList = await SearchYTS(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found!",
                        description=f"Can't find YTS torrents for {query} !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No YTS Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="!yts ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    dl_links = "- " + "\n\n- ".join(torrentList[i]['Downloads'])
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Language: {torrentList[i]['Language']}\nLikes: {torrentList[i]['Likes']}, Rating: {torrentList[i]['Rating']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**𝐆𝐞𝐧𝐫𝐞:** `{torrentList[i]['Genre']}`\n"
                                             f"**𝐍𝐚𝐦𝐞:** `{torrentList[i]['Name']}`\n"
                                             f"**𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞:** `{torrentList[i]['Language']}`\n"
                                             f"**𝐋𝐢𝐤𝐞𝐬:** `{torrentList[i]['Likes']}`\n"
                                             f"**𝐑𝐚𝐭𝐢𝐧𝐠:** `{torrentList[i]['Rating']}`\n"
                                             f"**𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** `{torrentList[i]['Runtime']}`\n"
                                             f"**𝐑𝐞𝐥𝐞𝐚𝐬𝐞𝐝 𝐨𝐧 {torrentList[i]['ReleaseDate']}**\n\n"
                                             f"**𝐓𝐨𝐫𝐫𝐞𝐧𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 Links:**\n{dl_links}\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
    elif search_ts.startswith("!a"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!a [text]",
                    description="Search For Torrents for Anime ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!a [text]`\n\nSearch Anime Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!a ")]])
                )
            )
        else:
            torrentList = await SearchAnime(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Anime Torrents Found!",
                        description=f"Can't find Anime torrents for {query} !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Anime Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="!a ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeder']}, Leechers: {torrentList[i]['Leecher']}\nSize: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**𝐂𝐚𝐭𝐞𝐠𝐨𝐫𝐲:** `{torrentList[i]['Category']}`\n"
                                             f"**𝐍𝐚𝐦𝐞:** `{torrentList[i]['Name']}`\n"
                                             f"**𝐒𝐞𝐞𝐝𝐞𝐫𝐬:** `{torrentList[i]['Seeder']}`\n"
                                             f"**𝐋𝐞𝐞𝐜𝐡𝐞𝐫𝐬:** `{torrentList[i]['Leecher']}`\n"
                                             f"**𝐒𝐢𝐳𝐞:** `{torrentList[i]['Size']}`\n"
                                             f"**𝐔𝐩𝐥𝐨𝐚𝐝 𝐃𝐚𝐭𝐞:** `{torrentList[i]['Date']}`\n\n"
                                             f"**𝐌𝐚𝐠𝐧𝐞𝐭:** \n`{torrentList[i]['Magnet']}`\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="!a ")]]
                            )
                        )
                    )
    else:
        torrentList = await Search1337x(search_ts)
        if not torrentList:
            answers.append(
                InlineQueryResultArticle(
                    title="No Torrents Found!",
                    description=f"Can't find torrents for {search_ts} !!",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No Torrents Found For `{search_ts}`",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="")]])
                )
            )
        else:
            for i in range(len(torrentList)):
                answers.append(
                    InlineQueryResultArticle(
                        title=f"{torrentList[i]['Name']}",
                        description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}, Downloads: {torrentList[i]['Downloads']}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"**𝐂𝐚𝐭𝐞𝐠𝐨𝐫𝐲:** `{torrentList[i]['Category']}`\n"
                                         f"**𝐍𝐚𝐦𝐞:** `{torrentList[i]['Name']}`\n"
                                         f"**𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞:** `{torrentList[i]['Language']}`\n"
                                         f"**𝐒𝐞𝐞𝐝𝐞𝐫𝐬:** `{torrentList[i]['Seeders']}`\n"
                                         f"**𝐋𝐞𝐞𝐜𝐡𝐞𝐫𝐬:** `{torrentList[i]['Leechers']}`\n"
                                         f"**𝐒𝐢𝐳𝐞:** `{torrentList[i]['Size']}`\n"
                                         f"**𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐬:** `{torrentList[i]['Downloads']}`\n"
                                         f"__𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲 {torrentList[i]['UploadedBy']}__\n"
                                         f"__𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 {torrentList[i]['DateUploaded']}__\n"
                                         f"__𝐋𝐚𝐬𝐭 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 {torrentList[i]['LastChecked']}__\n\n"
                                         f"**𝐌𝐚𝐠𝐧𝐞𝐭:**\n`{torrentList[i]['Magnet']}`\n\nPowered By @TheTeleRoid",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("𝐒𝐞𝐚𝐫𝐜𝐡 𝐀𝐠𝐚𝐢𝐧", switch_inline_query_current_chat="")]]
                        ),
                        thumb_url=torrentList[i]['Poster']
                    )
                )
    try:
        await inline.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.SESSION_NAME}] - Answered Successfully - {inline.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.SESSION_NAME}] - Failed to Answer - {inline.from_user.first_name} - Sleeping for 5s")
        await asyncio.sleep(5)
        try:
            await inline.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out!",
                switch_pm_parameter="start",
            )
        except QueryIdInvalid:
            print(f"[{Config.SESSION_NAME}] - Failed to Answer Error - {inline.from_user.first_name} - Sleeping for 5s")
            await asyncio.sleep(5)


TorrentBot.run()
