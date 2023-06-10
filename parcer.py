import asyncio
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()


async def increment_page(data):
    url = data.get('url', '')
    parts = url.split('?')
    base_url = parts[0]
    query_params = parts[1] if len(parts) > 1 else ''
    params = dict(
        param.split('=') for param in query_params.split('&') if param)
    current_page = int(params.get('page', '1'))
    params['page'] = str(current_page + 1)
    new_url = base_url + '?' + '&'.join(
        f'{key}={value}' for key, value in params.items()
    )
    data['url'] = new_url
    return data


async def search_article_position(data, driver):
    url = data['url']
    target_article = data['article']
    driver.get(url)
    wait_time = 2

    while True:
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        actions = ActionChains(driver)
        actions.send_keys(Keys.END).perform()
        await asyncio.sleep(wait_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        wait_time -= 0.3
        if wait_time < 0.5:
            wait_time = 0.5

    elements = driver.find_elements(By.XPATH, "//*[@data-nm-id]")

    position = None
    for index, element in enumerate(elements, 1):
        attribute_value = element.get_attribute("data-nm-id")
        if attribute_value == target_article:
            position = index
            break

    return driver, position


async def search_article_position_with_pagination(data):
    driver_path = os.getenv('CHROMEDRIVER_PATH')
    driver = webdriver.Chrome(driver_path)

    start_time = time.time()
    position = None
    page_count = 0
    while position is None:
        page_count += 1
        driver, position = await search_article_position(data, driver)
        if position is not None or page_count >= 50:
            break
        data = await increment_page(data)

    driver.quit()

    end_time = time.time()
    execution_time = end_time - start_time
    if position is not None:
        return (
            f"Артикул {data['article']} находится на позиции {position} "
            f"в поиске на странице {page_count}."
            f"Время выполнения: {execution_time} сек."
        )
    else:
        return f"Артикул {data['article']} не найден в поиске"
