import os
from datetime import datetime

#app = r'"C:\Users\jim\Documents\Python_projects\Halterung Chim\alt\Probenhalterung Skript\Refactored\7za\7za.exe"'
app = '"C:/Apps/7za/7za.exe"'


def zip_files(url, fn):
    cmd = '{app} a -tzip {url}/{fn}.zip {url}/{fn}/*'.format(app=app, url=url, fn=fn)
    os.system(cmd)


def create_timestamp(url):
    tz_offset = utc_difference_in_hours()
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    fn_ts = '{}{}.timestamp'.format(ts, tz_offset)
    with open('{}/created_at_{}'.format(url, fn_ts), 'w+'):
        pass
    return

def get_timestamp():
    tz_offset = utc_difference_in_hours()
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return '{}{}'.format(ts, tz_offset)


def utc_difference_in_hours():
    seconds = (datetime.now()-datetime.utcnow()).total_seconds()
    if seconds < 0:
        prefix = '-'
        seconds = abs(seconds)
    else:
        prefix = '+'
    h = seconds // 3600
    m = (seconds % 3600) // 60
    offset = '{}{:02.0f}{:02.0f}'.format(prefix, h, m)
    return offset


if __name__ == '__main__':
    url = r'C:/Documents and Settings/FRT/Desktop/frt_script'
    fn = r'00546285.0000.post.itl'

    create_timestamp(url)
    zip_files(url, fn)

    print()
