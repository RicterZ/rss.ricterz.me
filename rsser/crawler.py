"""
A crawler of RSS 
"""
from rsser.utils import init_db, save_data
from rsser.parser.legacy import *
from rsser.parser.zsxq_public import parse_zsxq_public


def main():
    update_dict = {
        'json_raw_data_hacktivity': parse_hackerone,
        'json_raw_data_nhentai': parse_nhentai,
        'json_raw_data_legalhackers': parse_legalhackers,
        'json_raw_data_php_bugs': parse_php_bugs,
        'json_raw_data_zsxq': parse_zsxq_public,
    }

    init_db(update_dict.keys())

    for table, func in update_dict.items():
        try:
            save_data(func(), table)
        except Exception as e:
            print('Error: ' + str(e))
            continue

    return 0


if __name__ == '__main__':
    exit(main())
