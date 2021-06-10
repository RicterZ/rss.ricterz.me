"""
A crawler of RSS 
"""
from utils import init_db, save_data
from rsser.parser.legacy import *
from rsser.parser.zsxq import parse_zsxq


def main():
    update_dict = {
        'json_raw_data_hacktivity': parse_hackerone,
        'json_raw_data_nhentai': parse_nhentai,
        'json_raw_data_legalhackers': parse_legalhackers,
        'json_raw_data_php_bugs': parse_php_bugs,
    }

    update_dict = {
        'json_raw_data_zsxq': parse_zsxq,
    }
    init_db(update_dict.keys())

    for table, func in update_dict.items():
        save_data(func(), table)

    return 0


if __name__ == '__main__':
    exit(main())
