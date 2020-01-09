import web
import os
import jinja2 as jj
import urllib2
import json
import logging


urls = (
    '/feed', 'FeedHandler',
    '/zhihu_daily', 'FeedHandler',
    '/hacktivity', 'HacktivityFeedHandler',
    '/legalhackers', 'LegalHackersHandler',
    '/pixiv', 'PixivHandler',
    '/nhentai', 'nHentaiHandler',
    '/tuisec_paper', 'TuisecPaperHandler',
    '/php_bugs', 'PHPBugsHandler',
    '/(.*)', 'IndexHandler',
)


class IndexHandler(object):
    def GET(self, _):
        return self.render("index.html")

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class FeedHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        daily_data = db.select('json_raw_data', where='1', what='data')[0].data
        return self.render("feed.xml", data=json.loads(daily_data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class TuisecPaperHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        data = db.select('json_raw_data_tuisec', where='1', what='data')[0].data
        return self.render("feed_tuisec.xml", data=json.loads(data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class LegalHackersHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        data = db.select('json_raw_data_legalhackers', where='1', what='data')[0].data
        return self.render("feed_legalhackers.xml", data=json.loads(data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class HacktivityFeedHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        daily_data = db.select('json_raw_data_hacktivity', where='1', what='data')[0].data
        return self.render("feed_hacktivity.xml", data=json.loads(daily_data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class nHentaiHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        daily_data = db.select('json_raw_data_nhentai', where='1', what='data')[0].data
        print(json.loads(daily_data))
        return self.render("feed_nhentai.xml", data=json.loads(daily_data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class PHPBugsHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        daily_data = db.select('json_raw_data_php_bugs', where='1', what='data')[0].data
        return self.render("feed_php.xml", data=json.loads(daily_data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class PixivHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        daily_data = db.select('json_raw_data_pixiv', where='1', what='data')[0].data
        return self.render("feed_pixiv.xml", data=json.loads(daily_data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


# uWSGI
application = web.application(urls, globals()).wsgifunc()

app = web.application(urls,globals())
db = web.database(dbn='sqlite', db='rss.db3')
env = jj.Environment(loader=jj.FileSystemLoader('templates'), autoescape=True)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.propagate = False
    app.run()
