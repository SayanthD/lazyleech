# lazyleech - Telegram bot primarily to leech from torrents and upload to Telegram
# Copyright (c) 2021 lazyleech developers <theblankx protonmail com, meliodas_bot protonmail com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import logging
import aiohttp
from io import BytesIO, StringIO
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv("config.env")

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
TESTMODE = os.environ.get('TESTMODE')
TESTMODE = TESTMODE and TESTMODE != '0'

EVERYONE_CHATS = os.environ.get('EVERYONE_CHATS')
EVERYONE_CHATS = list(map(int, EVERYONE_CHATS.split(' '))) if EVERYONE_CHATS else []
ADMIN_CHATS = os.environ.get('ADMIN_CHATS')
ADMIN_CHATS = list(map(int, ADMIN_CHATS.split(' '))) if ADMIN_CHATS else []
ALL_CHATS = EVERYONE_CHATS + ADMIN_CHATS
# LICHER_* variables are for @animebatchstash and similar, not required
LICHER_CHAT = os.environ.get('LICHER_CHAT', '')
try:
    LICHER_CHAT = int(LICHER_CHAT)
except ValueError:
    pass
LICHER_STICKER = os.environ.get('LICHER_STICKER')
LICHER_FOOTER = os.environ.get('LICHER_FOOTER', '').encode().decode('unicode_escape')
LICHER_PARSE_EPISODE = os.environ.get('LICHER_PARSE_EPISODE')
LICHER_PARSE_EPISODE = LICHER_PARSE_EPISODE and LICHER_PARSE_EPISODE != '0'

PROGRESS_UPDATE_DELAY = int(os.environ.get('PROGRESS_UPDATE_DELAY', 10))
MAGNET_TIMEOUT = int(os.environ.get('LEECH_TIMEOUT', 60))
LEECH_TIMEOUT = int(os.environ.get('LEECH_TIMEOUT', 300))
ARIA2_SECRET = os.environ.get('ARIA2_SECRET', '')
IGNORE_PADDING_FILE = os.environ.get('IGNORE_PADDING_FILE', '1')
IGNORE_PADDING_FILE = IGNORE_PADDING_FILE and IGNORE_PADDING_FILE != '0'

SOURCE_MESSAGE = '''
<a href="https://github.com/Lazy-Leecher/lazyleech">lazyleech - Telegram bot primarily to leech from torrents and upload to Telegram</a>
Copyright (c) 2021 lazyleech developers &lt;theblankx protonmail com, meliodas_bot protonmail com&gt;

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see &lt;https://www.gnu.org/licenses/&gt;.
'''

logging.basicConfig(level=logging.INFO)
app = Client('lazyleech', API_ID, API_HASH, plugins={'root': os.path.join(__package__, 'plugins')}, bot_token=BOT_TOKEN, test_mode=TESTMODE, sleep_threshold=30)
session = aiohttp.ClientSession()
help_dict = dict()
preserved_logs = []

class SendAsZipFlag:
    pass

class ForceDocumentFlag:
    pass

def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file
