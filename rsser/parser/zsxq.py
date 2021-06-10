import requests


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.77 Safari/537.36 ',
    'Cookie': 'zsxq_access_token=74B953E3-4FDA-6D96-6D1A-5923896A2F18_D4F63B5DA201D049',
}


def parse_zsxq():
    groups = [
        '88512188158852',
        '555848225184',
        '2212251881',
        '28518424185521',
    ]

    result = []
    for group in groups:
        url = 'https://api.zsxq.com/v2/groups/{}/topics?scope=all&count=10'.format(group)
        resp = requests.get(url, headers=HEADERS, verify=False).json()

        if not resp['succeeded'] and resp['code'] == 1059:
            resp = requests.get(url, headers=HEADERS, verify=False).json()

        if resp['succeeded']:
            for topic in resp['resp_data']['topics']:
                if topic['type'] == 'talk':
                    result.append({
                        'group': topic['group']['name'],
                        'author': topic['talk']['owner']['name'],
                        'text': topic['talk']['text'],
                        'topic_id': topic['topic_id'],
                        'create_time': topic['create_time']
                    })

    result = sorted(result, key=lambda k: k['create_time'])[::-1]
    return result
