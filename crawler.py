"""
A crawler of RSS 
"""
import sys
import re
import os
import web
import json
import requests

from pprint import pprint
from bs4 import BeautifulSoup as bs


hackerone_query = {"query":"query Hacktivity_page_QueryRelayQL($id_0:ID!,$first_1:Int!,$last_4:Int!,$secure_order_by_2:FiltersHacktivityItemFilterOrder!,$where_3:FiltersHacktivityItemFilterInput!,$size_5:ProfilePictureSizes!) {node(id:$id_0) {...Fc}} fragment F0 on HacktivityItemInterface {id,__typename} fragment F1 on HacktivityItemInterface {votes {total_count},_votes20kQZj:votes(last:$last_4) {edges {node {id,user {username,id}},cursor},pageInfo {hasNextPage,hasPreviousPage}},upvoted_by_current_user,id,__typename,...F0} fragment F2 on Undisclosed {id,reporter {username,id},team {handle,name,_profile_picture1Fh783:profile_picture(size:$size_5),url,id},latest_disclosable_action,latest_disclosable_activity_at,requires_view_privilege,total_awarded_amount,currency} fragment F3 on Undisclosed {id,...F2} fragment F4 on Disclosed {id,reporter {username,id},team {handle,name,_profile_picture1Fh783:profile_picture(size:$size_5),url,id},report {title,substate,url,id},latest_disclosable_action,latest_disclosable_activity_at,total_awarded_amount,severity_rating,currency} fragment F5 on Disclosed {id,...F4} fragment F6 on HackerPublished {id,reporter {username,id},team {handle,name,_profile_picture1Fh783:profile_picture(size:$size_5),url,id},report {url,title,substate,id},latest_disclosable_activity_at,severity_rating} fragment F7 on HackerPublished {id,...F6} fragment F8 on Node {id,__typename} fragment F9 on HacktivityItemUnion {__typename,...F1,...F3,...F5,...F7,...F8} fragment Fa on HacktivityItemInterface {id,_id,__typename,...F9} fragment Fb on HacktivityItemConnection {total_count,pageInfo {hasNextPage,hasPreviousPage},edges {cursor,node {__typename,...Fa,...F8}}} fragment Fc on Query {_hacktivity_items2Uw4QA:hacktivity_items(first:$first_1,query:\"\",secure_order_by:$secure_order_by_2,where:$where_3) {total_count,...Fb},id}","variables":{"id_0":"Z2lkOi8vaGFja2Vyb25lL09iamVjdHM6OlF1ZXJ5L3N0YXRpYw==","first_1":25,"last_4":10,"secure_order_by_2":{"latest_disclosable_activity_at":{"_direction":"DESC"}},"where_3":{"report":{"disclosed_at":{"_is_null":False}}},"size_5":"medium"}}


def parse_tuisec():
    result = []
    resp = requests.get('https://paper.tuisec.win/index.jsp', headers={'Cookie': 'UM_distinctid=15fd76221c4843-0224fde287ea9a-3b3e5906-1fa400-15fd76221c56de; __51cke__=; CF_Authorization=eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ3N2Q4ZmIwODVkYmFlM2Y1MTFiMWJkMGI5ZGMyMjcxZTU5ZWM1NjM0OGRiYmRlNDJlZDk0OWI4NDRlMWE0MmIiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOlsiZGE1YjAzYTQyMGE3ZGYxZjkwYzA1Yjg2YzNiZWE5NDczMzhlYmJkODkzMWY4ZjE5MTlkODkzYmRkODZlMTdhNyJdLCJlbWFpbCI6IlJpY3RlclpoZW5nQGdtYWlsLmNvbSIsImV4cCI6MTUxNjQ1MjY3MCwiaWF0IjoxNTEzODI0NjczLCJpc3MiOiJodHRwczovL3NlYy5jbG91ZGZsYXJlYWNjZXNzLmNvbSIsIm5vbmNlIjoiODg0MDFiZmI0YWJlNmU5ZmE3YWIzOTA4OTdjMzVkNWUwZTNmZWIzNGI0MWEwZjMzNjRkZDk1NWY5NWVkNTI4YSIsInN1YiI6ImNkZDI2ZmZjLWU3NDgtNDQ5ZC1iMDY1LTk5NTk2M2Q2YTU0MyJ9.FPp3elShRIJ9bNMDIjUgZE-nz7YfuNcUXGQGIuDdMep7l-Prp8MAT6VVRnh0UsT2rlbw6V1RpY-fSHdGi33qkGzxAuviYG3SHeAgZDpeByVJuRqCN1801acX92o2Nqfpc26-5l71BggxhhqPnYg4CX9_wThXZDlNs1s4DYGJ8himxrwEQnpsQ_Ktcc3kJ1QpZpy3g4MaKVkwwdnNs66vXu5TOs7corgEXm-wLAe7M4aNFAS51vp686PQlbCs4n-0fFMDnLsgJYkeBmCvBse79oWAv7NzADU5ko7WaiKPR3d0QLCRJxK4nQ1pCF5LazwH2CWMA5qUeSbkcCgUKdIiDQ; a5774_times=25; a5774_pages=2; __tins__19225774=%7B%22sid%22%3A%201514272134222%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201514273943905%7D; __51laig__=29'}).content
    html = bs(resp, 'html.parser').find_all('tr')
    for i in html:
        data = i.find_all('td')
        if not data:
            continue
        data = data[1].a
        if not data:
            continue
        result.append({data.attrs['href']: data.text.strip('\n')})
    return result


def parse_nhentai():
    result = []
    response = requests.get("http://nhentai.net/language/chinese/").content

    html =  bs(response, 'html.parser')
    doujinshi_search_result = html.find_all('div', attrs={'class': 'gallery'})
    for doujinshi in doujinshi_search_result:
        doujinshi_container = doujinshi.find('div', attrs={'class': 'caption'})
        title = doujinshi_container.text.strip()
        title = (title[:85] + '..') if len(title) > 85 else title
        id_ = re.search('/g/(\d+)/', doujinshi.a['href']).group(1)
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
    data = requests.post('https://hackerone.com/graphql', json=hackerone_query).json()
    for _, value in data['data']['node'].items():
        if isinstance(value, dict):
            for item in value['edges']:
                result.append(item['node']['report'])

    return result


def parse_zhihu():
    """Parse Zhihu Daily API to JSON data"""
    api_url = 'http://news-at.zhihu.com/api/1.2/news/latest'
    daily_data = request(api_url)
    news = daily_data['news']
    for new in news:
        new['content'] = request(new['url'])['body']
    return daily_data


def parse_pixiv():
    headers = {
        'Cookie': 'first_visit_datetime_pc=2018-12-31+03%3A44%3A02; p_ab_id=7; p_ab_id_2=8; p_ab_d_id=447414047; __utmz=235335808.1546195445.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.891193670.1546195445; privacy_policy_agreement=1; c_type=21; a_type=0; b_type=2; d_type=4; yuid_b=Ixl3FGE; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=female=1^6=user_id=10878445=1^9=p_ab_id=7=1^10=p_ab_id_2=8=1^11=lang=zh=1; PHPSESSID=10878445_1d0dfa84afa02acb01549cb92cce7f33; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_r=; limited_ads=%7B%22responsive%22%3A%22%22%7D; adr_id=UIfPpGsHPGsWxmA9bLzuZTyvk4iR2twgK1gEt2gUz14Uijgi; categorized_tags=1DJe5jv-kK~78lv_o5xOl~8NfvpmigcD~BU9SQkS-zU~EZQqoW9r8g~FH4iev6rlW~GX5cZxE2GY~IVwLyT8B6k~NqnXOnazer~O2wfZxfonb~OEXgaiEbRa~OT-C6ubi9i~PHQDP-ccQD~RFVdOq-YjA~RcahSSzeRf~b8b4-hqot7~cpt_Nk5mjc~gZWEWFTj-b~sr5scJlaNv~uQ8dUM2bls~ukwGkrxn11~y8GNntYHsi~yqXYmaGSd-; is_sensei_service_user=1; __utma=235335808.891193670.1546195445.1558098281.1558359726.13; __utmc=235335808; __utmt=1; _gid=GA1.2.1940095664.1558359727; _gat_UA-1830249-138=1; tags_sended=1; ki_t=1553911752939%3B1558359732810%3B1558359732810%3B2%3B3; OX_plg=pm; tag_view_ranking=uW5495Nhg-~RTJMXD26Ak~0xsDLqCEW6~Lt-oEicbBr~uusOs0ipBx~yTFlPOVybE~q3eUobDMJW~dx7ljrJnxj~-M6-exp-Ky~78lv_o5xOl~y8GNntYHsi~BU9SQkS-zU~PHQDP-ccQD~sr5scJlaNv~DriUjI1aUj~O2wfZxfonb~O1aut1etjj~SuVYClquvg~qtVr8SCFs5~PEWvBxU9pH~EZQqoW9r8g~D0nMcn6oGk~aZ_wa3k3Fm~Ie2c51_4Sp~gVfGX_rH_Y~EZT1Zmpy4z~a-yCMcqYxL~2R7RYffVfj~CrFcrMFJzz~Sb5ux1AvqY~5KjiIRTpOd~lkVl5xl4lr~LX3_ayvQX4~mVrhJAQecG~faHcYIP1U0~MM6RXH_rlN~TcgCqYbydo~RcahSSzeRf~R3lr4__Kr8~q303ip6Ui5~vSWEvTeZc6~cpt_Nk5mjc~AI_aJCDFn0~cKKaLdcqk_~Is0SiXyaWb~nt6svoJL0B~f2b1_0ENwh~IdzC1PvBEc~RFVdOq-YjA~mBRXRaBmhe~NIg4rAP1ON~4cMWGVjD1l~p1XwR3HRIK~hqHfTE09kK~p76wqGJbIo~lKmQRiaEov~PcPqnGz2CG~sFB6DB7I46~TlJgIsuHkr~HzwBO1IlpM~DnJ4nTRK-U~cofmB2mV_d~NDsKQx4TRT~xEQSXK1X9d~UkHlWglNkD~Ym87YYStOm~75zhzbk0bS~a0LQDEym3c~pEoq1JS-NB~GX5cZxE2GY~Ngz9KxUrJt~b_G3UDfpN0~yZf1XmIy-U~2acjSVohem~juumLY9DfB~7AKcijMMXr~UFCwdv4Vve~JXmGXDx4tL~b1s-xqez0Y~SX9Wrwyb4r~Txs9grkeRc~qKHPDN09e1~OgdypjrwdX~0M0zAeslDb~zUV1dBrslN~50qaEUZGRV~yqXYmaGSd-~0X7OEvtbz5~edV8CDd_6F~spPqEvHEF2~SqVgDNdq49~aKhT3n4RHZ~ujS7cIBGO-~LEmyJ-RN72~nVqUGgS_d7~5oPIfUbtd6~d9DFbt0poe~ZD1GYewUOF~0Sds1vVNKR~pdQ5s8in7B; __utmb=235335808.5.10.1558359726',
    }
    data = requests.get('https://www.pixiv.net/bookmark_new_illust.php', headers=headers, verify=False).content
    data = bs(data, 'lxml').find_all('div', attrs={'id': 'js-mount-point-latest-following'})[0]
    images = []
    for i in json.loads(data.attrs['data-items']):
        print(i['url'])
        name = os.path.basename(i['url'])
        image = requests.get(i['url'], headers={'Referer': 'https://www.pixiv.net/'}).content
        with open('./static/pixiv/' + name, 'wb') as f:
            f.write(image)

        images.append({
            'id': name.replace('_p0_master1200.jpg', ''),
            'src': '/static/pixiv/' + name,
            'title': i['illustTitle'],
            'auothr': i['userName'],
        })
    return images



def parse_php_bugs():
    data = requests.get('https://bugs.php.net/search.php?limit=30&order_by=id&direction=DESC&cmd=display&status=Open&bug_type=All').content
    html = bs(data, 'html.parser')
    tr = html.find_all('tr', attrs={'valign': 'top'})
    ret = []
    for i in tr:
        td = i.find_all('td')
        if td[4].text != 'Bug':
            continue

        data = {}
        data['id'] = td[0].text
        data['url'] = td[0].a.attrs['href']
        data['date'] = td[1].text
        data['package'] = td[3].text
        data['php_version'] = td[6].text
        data['os'] = td[7].text
        data['title'] = td[8].text
        ret.append(data)

    return ret


def request(url):
    """Resuest urls with headers"""
    request = requests.get(url, verify=False, headers={'User-Agent': 'curl/1.1', 'x-requested-with':'XMLHttpRequest', 'accept': 'application/json'})
    try:
	return request.json()
    except:
        return {}




def save_data(data, table):
    """Save data to the database"""
    print("UPDATE_TABLE %s" % table)
    db.update(table, where='id=1', data=json.dumps(data))


# Connent to the database.
db = web.database(dbn='sqlite', db='rss.db3')

# Create rss.db3 if it don't exist.
if not os.path.exists('./rss.db3'):
    db.query('''
        create table json_raw_data (
            id int(4) primary key not null,
            data longtext default null
        );
    ''')

    db.query('''
        create table json_raw_data_hacktivity (
            id int(4) primary key not null,
            data longtext default null
        );
    ''')

    db.query('''
        create table json_raw_data_legalhackers (
            id int(4) primary key not null,
            data longtext default null
        );
    ''')
    db.query('''
        create table json_raw_data_pixiv (
            id int(4) primary key not null,
            data longtext default null
        );
    ''')
    db.query('''
        create table json_raw_data_nhentai (
   	    id int(4) primary key not null,
            data longtext default null
	)
    ''')
    db.query('''
        create table json_raw_data_tuisec (
   	    id int(4) primary key not null,
            data longtext default null
	)
    ''')
    db.insert('json_raw_data', id=1, data=None)
    db.insert('json_raw_data_tuisec', id=1, data=None)
    db.insert('json_raw_data_pixiv', id=1, data=None)
    db.insert('json_raw_data_legalhackers', id=1, data=None)
    db.insert('json_raw_data_hacktivity', id=1, data=None)
    db.insert('json_raw_data_nhentai', id=1, data=None)


if __name__ == '__main__':
    data = parse_hackerone()
    save_data(data, 'json_raw_data_hacktivity')
    data = parse_nhentai()
    save_data(data, 'json_raw_data_nhentai')
    data = parse_pixiv()
    save_data(data, 'json_raw_data_pixiv')
    data = parse_tuisec()
    save_data(data, 'json_raw_data_tuisec')
    data = parse_legalhackers()
    save_data(data, 'json_raw_data_legalhackers')
    data = parse_php_bugs()
    save_data(data, 'json_raw_data_php_bugs')
    # data = parse_zhihu()
    # save_data(data, 'json_raw_data')
