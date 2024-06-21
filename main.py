import html
import json
import os
import re
import requests

from datetime import datetime


def get_newslist_info(page: int = 1 , limit: int = 30):
    """
    param page: page number
    param limit: how many news per page
    return newslist_info: newslist_info
    """
    r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/tw_stock_news?page={page}&limit={limit}")
    if r.status_code != requests.codes.ok:
        print('requeste failed', r.status_code)
        return None
    newslist_info = r.json()['items']['data']
    return newslist_info

def clean_news_content(text: str) -> str:
    content = html.unescape(text)
    content = re.sub(r'<[^>]+>', '', content)
    return content

def unix2datetime(unix_time):
    return datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

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
