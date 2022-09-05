import re
import requests
import json

from bs4 import BeautifulSoup as bs


hackerone_query = {"operationName":"HacktivityPageQuery","variables":{"querystring":"","where":{"report":{"disclosed_at":{"_is_null":False}}},"orderBy":None,"secureOrderBy":{"latest_disclosable_activity_at":{"_direction":"DESC"}},"count":25,"maxShownVoters":10},"query":"query HacktivityPageQuery($querystring: String, $orderBy: HacktivityItemOrderInput, $secureOrderBy: FiltersHacktivityItemFilterOrder, $where: FiltersHacktivityItemFilterInput, $count: Int, $cursor: String, $maxShownVoters: Int) {\n  me {\n    id\n    __typename\n  }\n  hacktivity_items(\n    first: $count\n    after: $cursor\n    query: $querystring\n    order_by: $orderBy\n    secure_order_by: $secureOrderBy\n    where: $where\n  ) {\n    ...HacktivityList\n    __typename\n  }\n}\n\nfragment HacktivityList on HacktivityItemConnection {\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  edges {\n    node {\n      ... on HacktivityItemInterface {\n        id\n        databaseId: _id\n        __typename\n      }\n      __typename\n    }\n    ...HacktivityItem\n    __typename\n  }\n  __typename\n}\n\nfragment HacktivityItem on HacktivityItemUnionEdge {\n  node {\n    ... on HacktivityItemInterface {\n      id\n      type: __typename\n    }\n    ... on Undisclosed {\n      id\n      ...HacktivityItemUndisclosed\n      __typename\n    }\n    ... on Disclosed {\n      id\n      ...HacktivityItemDisclosed\n      __typename\n    }\n    ... on HackerPublished {\n      id\n      ...HacktivityItemHackerPublished\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HacktivityItemUndisclosed on Undisclosed {\n  id\n  votes {\n    total_count\n    __typename\n  }\n  voters: votes(last: $maxShownVoters) {\n    edges {\n      node {\n        id\n        user {\n          id\n          username\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  upvoted: upvoted_by_current_user\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    id\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  requires_view_privilege\n  total_awarded_amount\n  currency\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n\nfragment UserLinkWithMiniProfile on User {\n  id\n  username\n  __typename\n}\n\nfragment HacktivityItemDisclosed on Disclosed {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  votes {\n    total_count\n    __typename\n  }\n  voters: votes(last: $maxShownVoters) {\n    edges {\n      node {\n        id\n        user {\n          id\n          username\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  upvoted: upvoted_by_current_user\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    id\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  report {\n    id\n    databaseId: _id\n    title\n    substate\n    url\n    __typename\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  total_awarded_amount\n  severity_rating\n  currency\n  __typename\n}\n\nfragment HacktivityItemHackerPublished on HackerPublished {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  votes {\n    total_count\n    __typename\n  }\n  voters: votes(last: $maxShownVoters) {\n    edges {\n      node {\n        id\n        user {\n          id\n          username\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  upvoted: upvoted_by_current_user\n  team {\n    id\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  report {\n    id\n    url\n    title\n    substate\n    __typename\n  }\n  latest_disclosable_activity_at\n  severity_rating\n  __typename\n}\n"}


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


def parse_legalhackers():
    url = 'http://legalhackers.com/'
    data = requests.get(url).content
    articles = bs(data, "lxml").find_all('section')[2].article.ol.find_all('li')
    return [{i.text: url + str(i.a.attrs['href'])} for i in articles]


def parse_hackerone():
    result = []
    # post_data = json.dumps(hackerone_query)
    headers = {
        'Content-Type': 'application/json',
        'x-csrf-token': 'ZCcJmm5R+HoLgDNHStZGp/45Yt/hNft+N7UTDX6lh8RdP/Xv/qbJQB09hrkhYhq8fulQDS2lV7aXg0Y17jJCOA==',
        'Cookie': 'h1_device_id=eef37823-48b5-42e1-b243-6e7fc08428f1; optimizelyEndUserId=oeu1660730260777r0.01829525761365991; _gcl_au=1.1.1104333941.1660730262; _ga=GA1.2.624690036.1660730262; _mkto_trk=id:168-NAU-732&token:_mch-hackerone.com-1660730262445-81314; _gid=GA1.2.832040327.1662356812; AMP_MKTG_b7cba2c14c=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5oYWNrZXJvbmUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5oYWNrZXJvbmUuY29tJTIyJTdE; _dd_s=rum=0&expire=1662357716723; __Host-session=azVmMkZlNnpGV1lYaGhaMXZCMmpJbkdEbXg2Znl3VTFraXdrOVZmZ09uRjdmbm1kSlBNNGkyaDBSUTRNS3FoQm1qTTMzMUNHYkhpZ0hVYkMyMDVHVGdmOWdCL1RGa29RNHJQQi9mb3k4KytUTlVBcFhNQmlrMEVhalFiTWNIdm5CODI1VnFmWDhtcXllVEhEUzBTRzJoeG9UTDBLUzAxc3FvU1VvSzVrbEZKcGRlbCtGNUF1REEzT0d2dkNPbXUyaFg2MmJTQnRlaWNCck9uendEZUx1ejhDNVNyWE9OdHN6M2srdzJHemRTZENxMFdBdXUrdXdmM2w3alZocWFiMEdVVmFjNGswcmNBYlNMcytiVHpyL2wzV3FmWVFJanNzQS9Qem5YMjJHRDQ9LS1sdE13Q3NGSy9oY2N0WDR0b3dlK0dBPT0%3D--f1a03aa60891d922e8f4318a3b0423bf067b5a88; AMP_b7cba2c14c=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMjQzZDhlYzgyLWYzMTgtNDM3NS04NjFlLWUzZmMyMGY4ZDY4ZCUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNjYyMzU2ODE3MTAwJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTY2MjM1NjgxMTY1OCUyQyUyMnVzZXJJZCUyMiUzQW51bGwlN0Q='
    }
    data = requests.post('https://hackerone.com/graphql', json=hackerone_query, headers=headers).json()
    for value in data['data']['hacktivity_items']['edges']:
        if isinstance(value, dict):
            item = value
            if item['node']['total_awarded_amount']:
                item['node']['report']['title'] = '[${}] {}: {}'.format(item['node']['total_awarded_amount'],
                                                                  item['node']['team']['name'], 
                                                                  item['node']['report']['title'])
            else:
                item['node']['report']['title'] = '{}: {}'.format(item['node']['team']['name'], 
                                                                  item['node']['report']['title'])
            result.append(item['node']['report'])

    return result


def parse_php_bugs():
    data = requests.get(
        'https://bugs.php.net/search.php?limit=30&order_by=id&direction=DESC&cmd=display&status=Open&bug_type=All'
    ).content
    html = bs(data, 'html.parser')
    tr = html.find_all('tr', attrs={'valign': 'top'})
    ret = []
    for i in tr:
        td = i.find_all('td')
        if td[4].text != 'Bug':
            continue

        data = {
            'id': td[0].text,
            'url': td[0].a.attrs['href'],
            'date': td[1].text,
            'package': td[3].text,
            'php_version': td[6].text,
            'os': td[7].text,
            'title': td[8].text
        }
        ret.append(data)

    return ret
