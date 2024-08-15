import logging
from urllib.parse import urlparse

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.i18n import gettext as _
from aiohttp import ClientSession

import settings
from utils import get, post


router = Router()


@router.message(Command('start'))
async def start(message: Message):
    return await message.answer(_('Hello bro, send me a link to tiktok video'))


@router.message()
async def download(message: Message, bot: Bot):
    'Uploads video by tiktok link'

    url = message.text or ''
    result = urlparse(url)

    if 'tiktok.com' not in result.netloc:
        return await message.answer(
            _('Sorry bro! Its not correct link. Try again.')
        )

    loading = await message.answer(
        _('Please wait, the video is being fetched.')
    )

    async with ClientSession() as session:
        body = await post(
            url=settings.SECRET_URL,
            data={'url': url},
            session=session
        )

        try:
            mp4_url = body['data']['mp4']
            thumbnail_url = body['data']['video_img']
        except (KeyError, TypeError):
            logging.critical(
                'Unexpected body structure. Body: %s' % body
            )
            return await message.answer(_('Someting wrong, try again later'))

        mp4 = await get(mp4_url, session)
        thumbnail = await get(thumbnail_url, session)

        await bot.send_video(
            message.chat.id,
            thumbnail=BufferedInputFile(thumbnail, 'thumbnail.jpeg'),
            video=BufferedInputFile(mp4, 'video.mp4'),
            width=1080,
            height=1920,
            caption=_('Done'),
        )
        await loading.delete()
