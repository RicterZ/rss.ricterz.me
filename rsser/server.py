import web
import json
import logging
import jinja2 as jj

from rsser.constants import DB, TEMPLATE


URLS = (
    '/hacktivity', 'HacktivityFeedHandler',
    '/legalhackers', 'LegalHackersHandler',
    '/nhentai', 'NHentaiHandler',
    '/php_bugs', 'PHPBugsHandler',
    '/zsxq', 'ZSXQHandler',
    '/(.*)', 'IndexHandler',
)

ENV = jj.Environment(loader=jj.FileSystemLoader(TEMPLATE), autoescape=True)


class BaseHandler(object):
    table = None
    template = None
    content_type = 'text/xml; charset=utf-8'

    def GET(self, *args):
        web.header('Content-Type', self.content_type)
        if self.table is not None:
            data = DB.select(self.table, where='1', what='data')[0].data
            print(data)
            return ENV.get_template(self.template).render(data=json.loads(data))
        else:
            return ENV.get_template(self.template).render()


class IndexHandler(BaseHandler):
    template = 'index.html'
    content_type = 'text/html'


class LegalHackersHandler(BaseHandler):
    table = 'json_raw_data_legalhackers'
    template = 'feed_legalhackers.xml'


class HacktivityFeedHandler(BaseHandler):
    table = 'json_raw_data_hacktivity'
    template = 'feed_hacktivity.xml'


class NHentaiHandler(BaseHandler):
    table = 'json_raw_data_nhentai'
    template = 'feed_nhentai.xml'


class PHPBugsHandler(BaseHandler):
    table = 'json_raw_data_php_bugs'
    template = 'feed_php.xml'


class ZSXQHandler(BaseHandler):
    table = 'json_raw_data_zsxq'
    template = 'feed_zsxq.xml'


if __name__ == "__main__":
    app = web.application(URLS, globals(), autoreload=False)

    logger = logging.getLogger()
    logger.propagate = False
    app.run()
