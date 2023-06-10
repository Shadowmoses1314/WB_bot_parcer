# WB_bot_parcer


**README**

Это парсер-бот, который позволяет найти место выдачи и страницу товара по его артикулу и запросу.

**Технологии**

- asyncio
- selenium
- beautifulsoup4
- aiogram


**Запуск бота**

1. Склонируйте репозиторий:

   ```shell
   git clone https://github.com/Shadowmoses1314/WB_bot_parcer.git
   ```

2. Создайте виртуальное окружение и активируйте его:

   ```shell
   python -m venv env
   source env/bin/activate
   ```

3. Установите зависимости из файла `requirements.txt`:

   ```shell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` и добавьте следующие переменные окружения:

   ```
   TOKEN=токен_вашего_бота
   CHROMEDRIVER_PATH=./chromedriver
   ```

   Замените `токен_вашего_бота` на токен, полученный от BotFather в Telegram. Убедитесь, что вы также установили ChromeDriver (драйвер Chrome) и указали его путь в переменной `CHROMEDRIVER_PATH`.

5. Сохраните файл `.env`.

6. Запустите бот:

   ```shell
   python main.py
   ```

Запустите бот /start. Теперь вы можете использовать бота для поиска места выдачи и страницы товара по его артикулу и запросу.
P.S. Развёртывание через Docker находится в разработке 
