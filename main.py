import html
import os
import pymongo
import re
import requests

from datetime import datetime

def save_to_mongodb(data: dict) -> None:
    """
    Save data to MongoDB.

    Args:
        data (dict): The data to be saved.

    Returns:
        None
    """
    myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    mycol.insert_one(data)

def get_newslist_info(page: int = 1 , limit: int = 30, start_date: str = '2024-01-01', end_date: str = '2024-01-01') -> list | None:
    """
    Retrieves a list of news information from the Cnyes API.

    Args:
        page (int, optional): The page number of the news list. Defaults to 1.
        limit (int, optional): The maximum number of news items to retrieve. Defaults to 30.

    Returns:
        list | None: A list of news information if the request is successful, otherwise None.

    """
    start_date = datetime2unix(f"{start_date} 00:00:00")
    end_date = datetime2unix(f"{end_date} 23:59:59")
    url = f"https://api.cnyes.com/media/api/v1/newslist/category/tw_stock_news?page={page}&limit={limit}&startAt={start_date}&endAt={end_date}"
    print(url)
    r = requests.get(url)
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

def datetime2unix(datetime_str: str) -> int:
    """
    Converts a formatted datetime string to a Unix timestamp.

    Args:
        datetime_str (str): The formatted datetime string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        float: The Unix timestamp.
    """
    return int(datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').timestamp())

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
        save_to_mongodb(news_dict)
