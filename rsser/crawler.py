"""
A crawler of RSS 
"""
import traceback

from rsser.utils import init_db, save_data
from rsser.parser.legacy import parse_hackerone


def main():
    update_dict = {
        'json_raw_data_hacktivity': parse_hackerone,
        #'json_raw_data_nhentai': parse_nhentai,
    }

    init_db(update_dict.keys())

    for table, func in update_dict.items():
        try:
            save_data(func(), table)
        except Exception as e:
            traceback.print_exc()
            print('Error: ' + str(e))
            continue

    return 0


if __name__ == '__main__':
    exit(main())
