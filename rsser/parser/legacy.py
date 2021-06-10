import re
import requests

from bs4 import BeautifulSoup as bs


hackerone_query = {
    "query": "query Hacktivity_page_QueryRelayQL($id_0:ID!,$first_1:Int!,$last_4:Int!,"
             "$secure_order_by_2:FiltersHacktivityItemFilterOrder!,"
             "$where_3:FiltersHacktivityItemFilterInput!,$size_5:ProfilePictureSizes!) {node(id:$id_0) "
             "{...Fc}} fragment F0 on HacktivityItemInterface {id,__typename} fragment F1 on "
             "HacktivityItemInterface {votes {total_count},_votes20kQZj:votes(last:$last_4) {edges {"
             "node {id,user {username,id}},cursor},pageInfo {hasNextPage,hasPreviousPage}},"
             "upvoted_by_current_user,id,__typename,...F0} fragment F2 on Undisclosed {id,"
             "reporter {username,id},team {handle,name,_profile_picture1Fh783:profile_picture("
             "size:$size_5),url,id},latest_disclosable_action,latest_disclosable_activity_at,"
             "requires_view_privilege,total_awarded_amount,currency} fragment F3 on Undisclosed {id,"
             "...F2} fragment F4 on Disclosed {id,reporter {username,id},team {handle,name,"
             "_profile_picture1Fh783:profile_picture(size:$size_5),url,id},report {title,substate,url,"
             "id},latest_disclosable_action,latest_disclosable_activity_at,total_awarded_amount,"
             "severity_rating,currency} fragment F5 on Disclosed {id,...F4} fragment F6 on "
             "HackerPublished {id,reporter {username,id},team {handle,name,"
             "_profile_picture1Fh783:profile_picture(size:$size_5),url,id},report {url,title,substate,"
             "id},latest_disclosable_activity_at,severity_rating} fragment F7 on HackerPublished {id,"
             "...F6} fragment F8 on Node {id,__typename} fragment F9 on HacktivityItemUnion {"
             "__typename,...F1,...F3,...F5,...F7,...F8} fragment Fa on HacktivityItemInterface {id,_id,"
             "__typename,...F9} fragment Fb on HacktivityItemConnection {total_count,pageInfo {"
             "hasNextPage,hasPreviousPage},edges {cursor,node {__typename,...Fa,...F8}}} fragment Fc on "
             "Query {_hacktivity_items2Uw4QA:hacktivity_items(first:$first_1,query:\"\","
             "secure_order_by:$secure_order_by_2,where:$where_3) {total_count,...Fb},id}",
    "variables": {
        "id_0": "Z2lkOi8vaGFja2Vyb25lL09iamVjdHM6OlF1ZXJ5L3N0YXRpYw==",
        "first_1": 25,
        "last_4": 10,
        "secure_order_by_2": {
            "latest_disclosable_activity_at": {"_direction": "DESC"}
        },
        "where_3": {
            "report": {"disclosed_at": {"_is_null": False}}
        },
        "size_5": "medium"
    }
}


def parse_nhentai():
    result = []
    response = requests.get("http://nhentai.net/language/chinese/").content

    html = bs(response, 'html.parser')
    doujinshi_search_result = html.find_all('div', attrs={'class': 'gallery'})
    for doujinshi in doujinshi_search_result:
        doujinshi_container = doujinshi.find('div', attrs={'class': 'caption'})
        title = doujinshi_container.text.strip()
        title = (title[:85] + '..') if len(title) > 85 else title
        id_ = re.search('/g/([0-9]+)/', doujinshi.a['href']).group(1)
        img = doujinshi.img.attrs['data-rsser']
        result.append({'id': id_, 'title': title, 'img': img})
    return result


def parse_legalhackers():
    url = 'http://legalhackers.com/'
    data = requests.get(url).content
    articles = bs(data, "lxml").find_all('section')[2].article.ol.find_all('li')
    return [{i.text: url + str(i.a.attrs['href'])} for i in articles]


def parse_hackerone():
    result = []
    data = requests.post('https://hackerone.com/graphql', json=hackerone_query).json()
    for _, value in data['data']['node'].items():
        if isinstance(value, dict):
            for item in value['edges']:
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
