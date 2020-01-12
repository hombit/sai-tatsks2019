#!/usr/bin/env python3
import ads
import datetime
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams

rcParams['font.size'] = 14
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['xtick.top'] = True
rcParams['ytick.right'] = True
font = {'family': 'normal', 'size': 14}
rc('axes', linewidth=1)
rc('font', family='serif')
rc('font', serif='Times')
rc('legend', fontsize=14)
rc('xtick.major', size=0)
rc('ytick.major', size=5, width=1)
rc('xtick.minor', size=0)
rc('ytick.minor', size=3, width=1)

try:
    with open('./apikey', 'r') as f:
        ads.config.token = f.read().strip()
except OSError:
    print('No token, exiting')
    exit(1)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', type=str, default=False,
                        help='Keyword to search NASA ADS')
    parser.add_argument('-p', '--pages', default=3, type=int,
                        help='Max pages to seach, default 3. Uses API Key daily quota(max 5000/day)')
    parser.add_argument('-d', '--days', default=365, type=int,
                        help='Max days to search since today(backwards, default 365)')
    parser.add_argument("-v", "--verbosity", default=False, action='store_true',
                        help="increase output verbosity")
    return parser


def main():
    opts = parser().parse_args()
    if not opts.keyword:
        print('No keyword, exiting')
        exit(1)
    dt_list = []
    now = datetime.datetime.now()
    dt1 = (now - datetime.timedelta(days=opts.days)).strftime('%Y-%m')
    dt2 = now.strftime('%Y-%m')
    q = ads.SearchQuery(q='(abs:"{keyword}" or title:"{keyword}") '
                        'database:astronomy property:refereed pubdate:[{dt1} TO {dt2}]'.format(keyword=opts.keyword, dt1=dt1, dt2=dt2),
                        fl=['id', 'bibcode', 'title', 'citation_count', 'pubdate'], sort='pubdate desc', max_pages=opts.pages)
    for paper in q:
        if opts.verbosity:
            print(paper.title, paper.pubdate)
        dt_list.append(datetime.datetime.strptime(paper.pubdate.replace('-00-', '-01-'), '%Y-%m-00'))
    x = np.array(dt_list)
    df = pd.DataFrame({'x': x.astype('datetime64')})
    df.groupby([df['x'].dt.year, df['x'].dt.month]).count().plot(kind='bar', color='#4e79a7')
    ax = plt.axes()
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
    plt.xlabel('Month')
    plt.legend(loc='upper right')
    plt.show()


if __name__ == "__main__":
    main()
