import requests
import json
import re


MATCH_DATA = re.compile('topics:\[(.*)\],fetch:\{')


def parse_zsxq_public():
    groups = [
        '88512188158852',
        '555848225184',
        '2212251881',
        '28518424185521',
    ]

    result = []
    for group in groups:
        url = 'https://public.zsxq.com/groups/{}.html'.format(group)
        resp = requests.get(url, verify=False).text

        ret = MATCH_DATA.findall(resp)[0]
        print(ret)
        data = json.loads('[{}]'.format(ret))
        print(data)

        raise SystemExit
        if not resp['succeeded'] and resp['code'] == 1059:
            resp = requests.get(url, verify=False).json()

        if resp['succeeded']:
            for topic in resp['resp_data']['topics']:
                if topic['type'] == 'talk':
                    text = u''

                    if 'text' in topic['talk']:
                        text += topic['talk']['text']

                    if 'files' in topic['talk']:
                        fn = [i['name'] for i in topic['talk']['files']]
                        text += u'<br>Attachments: {}'.format(u', '.join(fn))

                    result.append({
                        'group': topic['group']['name'],
                        'author': topic['talk']['owner']['name'],
                        'text': text,
                        'topic_id': topic['topic_id'],
                        'create_time': topic['create_time']
                    })

    result = sorted(result, key=lambda k: k['create_time'])[::-1]
    return result
