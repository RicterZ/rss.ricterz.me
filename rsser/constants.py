import os
import web


DB_PATH = os.path.join(os.path.dirname(__file__), '../data/rss.db3')
DB = web.database(dbn='sqlite', db=DB_PATH)

TEMPLATE = os.path.join(os.path.dirname(__file__), 'templates')
