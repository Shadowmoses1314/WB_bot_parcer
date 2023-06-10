async def process_search_keywords(keyword):
    formatted_keyword = keyword.replace(" ", "%20")
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search={formatted_keyword}"
    return url
