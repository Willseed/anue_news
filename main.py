import html
import json
import os
import re
import requests

from datetime import datetime


def get_newslist_info(page: int = 1 , limit: int = 30) -> list | None:
    """
    Retrieves a list of news information from the Cnyes API.

    Args:
        page (int, optional): The page number of the news list. Defaults to 1.
        limit (int, optional): The maximum number of news items to retrieve. Defaults to 30.

    Returns:
        list | None: A list of news information if the request is successful, otherwise None.

    """
    r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/tw_stock_news?page={page}&limit={limit}")
    if r.status_code != requests.codes.ok:
        print('requeste failed', r.status_code)
        return None
    newslist_info = r.json()['items']['data']
    return newslist_info

def clean_news_content(text: str) -> str:
    """
    Clean the news content by removing HTML tags and unescaping HTML entities.

    Args:
        text (str): The news content to be cleaned.

    Returns:
        str: The cleaned news content.

    """
    content = html.unescape(text)
    content = re.sub(r'<[^>]+>', '', content)
    return content

def unix2datetime(unix_time: float) -> str:
    """
    Converts a Unix timestamp to a formatted datetime string.
    
    Args:
        unix_time (float): The Unix timestamp to convert.
        
    Returns:
        str: The formatted datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    for news in get_newslist_info():
        base_url = 'https://m.cnyes.com/news/id/'

        news_dict = {
            'source_url': os.path.join(base_url, str(news['newsId'])),
            'time': unix2datetime(news['publishAt']),
            'title': news['title'],
            'content': clean_news_content(news['content']),
            'keyword': news['keyword'],
        }
        news_json = json.dumps(news_dict, ensure_ascii=False)
        print(news_json)
        break
