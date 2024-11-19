import re
import csv
from collections import Counter
from urllib.parse import urljoin

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time

base_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"


async def get_titles_from_page(url: str,
                               session: aiohttp.ClientSession
                               ) -> tuple[list[str], list[str]]:
    """
    Извлекает первую букву и названия животных со страницы.

    На вход:
    url (str): URL страницы, с которой извлекаются данные.
    session (aiohttp.ClientSession): Сессия для выполнения HTTP-запросов.

    Возвращает:
    tuple[list[str], list[str]]: Список первых букв и список названий животных.
    """
    async with session.get(url) as response:
        html = await response.text()
    pattern = (
        r'<li><a href="[^"]+" title="(?!Служебная|Категория:)([^"]+)">'
        r'[^<]+</a></li>'
    )
    titles = re.findall(pattern, html)
    first_letters = [title[0].upper() for title in titles]
    return first_letters, titles


async def get_next_page_url(soup: BeautifulSoup) -> str | None:
    """
    Находит ссылку на следующую страницу в категории.

    На вход:
    soup (BeautifulSoup): Разобранный HTML-код страницы.

    Возвращает:
    str | None: URL следующей страницы или None, если следующей страницы нет.
    """
    next_page = soup.find('a', string='Следующая страница')
    if next_page:
        return urljoin(base_url, next_page['href'])
    return None


async def parse_page(
    url: str,
    session: aiohttp.ClientSession
) -> tuple[list[str], list[str], BeautifulSoup]:
    """
    Получает и парсит страницу, извлекая данные о заголовках и первой букве.

    На вход:
    url (str): URL страницы для парсинга.
    session (aiohttp.ClientSession): Сессия для выполнения HTTP-запросов.

    Возвращает:
    tuple[list[str], list[str], BeautifulSoup]:
    Список первых букв, список заголовков и объект BeautifulSoup.
    """
    async with session.get(url) as response:
        html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    first_letters, titles = await get_titles_from_page(url, session)
    return first_letters, titles, soup


async def main() -> Counter:
    """
    Главная функция для сбора всех животных с последовательных html страниц.

    Возвращает:
    Counter: Словарь: ключи - первые буквы, значение - количество животных.
    Также проводит мониторинг времени исполнения.
    """
    url = base_url
    letter_count = Counter()
    all_titles = []
    total_start_time = time.time()
    async with aiohttp.ClientSession() as session:
        while url:
            start_time = time.time()
            first_letters, titles, soup = await parse_page(url, session)
            letter_count.update(first_letters)
            all_titles.extend(titles)
            url = await get_next_page_url(soup)
            end_time = time.time()
            print(f"Страница прошла за {end_time - start_time:.2f} секунд")
    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    print(f"\nОбщее время работы программы: {total_elapsed_time:.2f} секунд")
    return letter_count


letter_count = asyncio.run(main())

with open(
    'animals_by_letter.csv', 'w', newline='', encoding='utf-8'
)as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Буква', 'Количество'])
    for letter, count in letter_count.items():
        writer.writerow([letter, count])
