import re
import requests
import json

from bs4 import BeautifulSoup as bs
from rsser.parser.data import h1data


def parse_nhentai():
    result = []
    response = requests.get("http://nhentai.net/language/chinese/", verify=False).content

    html = bs(response, 'html.parser')
    doujinshi_search_result = html.find_all('div', attrs={'class': 'gallery'})
    for doujinshi in doujinshi_search_result:
        doujinshi_container = doujinshi.find('div', attrs={'class': 'caption'})
        title = doujinshi_container.text.strip()
        title = (title[:85] + '..') if len(title) > 85 else title
        id_ = re.search('/g/([0-9]+)/', doujinshi.a['href']).group(1)
        img = doujinshi.img.attrs['data-src']
        result.append({'id': id_, 'title': title, 'img': img})
    return result


def parse_hackerone():
    result = []
    s = requests.Session()
    data = s.get('https://hackerone.com/hacktivity')
    cookie = data.headers['set-cookie']
    cookie = re.findall('(__Host-session=.*?;)', cookie)[0]
    csrf_token = re.findall('"csrf-token" content="(.*)"', data.text)[0]

    headers = {
        'Content-Type': 'application/json',
        'x-csrf-token': csrf_token,
        'cookie': cookie,
    }

    data = s.post('https://hackerone.com/graphql', json=h1data, headers=headers).json()
    for item in data['data']['search']['nodes']:
        if isinstance(item, dict):
            if item['total_awarded_amount']:
                if 'report' in item:
                    item['report']['title'] = '[${}] {}: {}'.format(item['total_awarded_amount'],
                            item['team']['name'], 
                            item['report']['title'])
            else:
                if 'report' in item:
                    item['report']['title'] = '{}: {}'.format(item['team']['name'], 
                                                              item['report']['title'])
            if 'report' in item:
                result.append(item['report'])

    return result

