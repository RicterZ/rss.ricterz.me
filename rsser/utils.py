import os
import json

from rsser.constants import DB, DB_PATH


def init_db(tables):
    if not os.path.exists(DB_PATH):
        for table in tables:
            DB.query('''
                create table {} (
                    id int(4) primary key not null,
                    data longtext default null
                );
            '''.format(table))
            DB.insert(table, id=1, data=None)


def save_data(data, table_name):
    print("UPDATE_TABLE %s" % table_name)
    DB.update(table_name, where='id=1', data=json.dumps(data))
