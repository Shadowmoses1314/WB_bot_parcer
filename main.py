import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from functions import process_search_keywords
from parcer import search_article_position_with_pagination
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TOKEN')
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: dict):
    await message.answer("Привет! Введите поисковый запрос:")
    await SearchQueryState.search_query.set()


class SearchQueryState(StatesGroup):
    search_query = State()


@dp.message_handler(content_types=types.ContentType.TEXT,
                    state=SearchQueryState.search_query)
async def search_query_handler(message: types.Message, state: dict):
    async with state.proxy() as data:
        data['search_query'] = message.text
    processed_url = await process_search_keywords(message.text)
    await message.answer("Введите артикул товара:")
    await SearchProductState.product_article.set()
    async with state.proxy() as data:
        data['processed_url'] = processed_url


class SearchProductState(StatesGroup):
    product_article = State()


@dp.message_handler(content_types=types.ContentType.TEXT,
                    state=SearchProductState.product_article)
async def search_product_handler(message: types.Message, state: dict):
    product_article = message.text.strip()
    if not product_article.isdigit():
        await message.answer(
            "Неверный артикул. Введите поисковый запрос заново:")
        await SearchQueryState.search_query.set()
        return

    async with state.proxy() as data:
        processed_url = data['processed_url']
        result_dict = {
            'url': processed_url,
            'article': product_article
        }

    await message.answer("Подождите, идет поиск товара...")
    result = await search_article_position_with_pagination(result_dict)

    await message.answer(result)
    await state.finish()


async def main():
    try:
        await dp.start_polling()
    except KeyboardInterrupt:
        pass
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
