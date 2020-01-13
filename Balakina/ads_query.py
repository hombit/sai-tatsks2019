#!/usr/bin/env python3
import ads
import datetime
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams
import calendar
import os
import math

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


def make_plot(dt_list, save):
    x = np.array(dt_list)
    df = pd.DataFrame({'x': x.astype('datetime64')})
    fig, ax = plt.subplots()
    group = df.groupby([df['x'].dt.year, df['x'].dt.month]).count()
    str_index = ['{month} {year}'.format(month=calendar.month_abbr[key[1]], year=key[0]) for key in group.index]
    group.plot(kind='bar', color='#4e79a7', ax=ax, legend=False)
    fig.subplots_adjust(left=.15, bottom=.25, right=.95, top=.95)
    plt.xlabel('Date')
    plt.ylabel('Number of papers')
    ax.set_xticklabels(str_index)
    plt.setp(ax.get_xticklabels(), rotation=55)
    if save is True:
        plt.savefig('Trends.png')
    else:
        plt.show()


def read_apikey():
    try:
        ads.config.token = os.environ['ADS_DEV_KEY']
    except KeyError:
        try:
            with open('./apikey', 'r') as f:
                ads.config.token = f.read().strip()
        except OSError:
            print('No token, exiting')
            exit(1)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', type=str,
                        help='Keyword to search NASA ADS')
    parser.add_argument('-d', '--days', default=365, type=int,
                        help='Max days to search since today (backwards, default 365)')
    parser.add_argument('-s', '--save', default=False, action='store_true',
                        help='Draw the plot or save it as file.png')

    return parser


def append_next(q, l):
    for paper in q:
        l.append(datetime.datetime.strptime(paper.pubdate.replace('-00-', '-01-'), '%Y-%m-00'))


def main():
    read_apikey()
    args = parser().parse_args()
    dt_list = []
    now = datetime.datetime.now()
    dt1 = (now - datetime.timedelta(days=args.days)).strftime('%Y-%m')
    dt2 = now.strftime('%Y-%m')
    q = ads.SearchQuery(q='(abs:"{keyword}" or title:"{keyword}") '
                        'database:astronomy property:refereed pubdate:[{dt1} TO {dt2}]'.format(keyword=args.keyword, dt1=dt1, dt2=dt2),
                        fl=['id', 'bibcode', 'title', 'citation_count', 'pubdate'], sort='pubdate desc', rows=2000, max_pages=1)
    q.execute()
    num_found = q.response.numFound
    need_pages = math.ceil(num_found / 2000)
    if need_pages > 1:
        q = ads.SearchQuery(q='(abs:"{keyword}" or title:"{keyword}") '
                            'database:astronomy property:refereed pubdate:[{dt1} TO {dt2}]'.format(keyword=args.keyword, dt1=dt1, dt2=dt2),
                            fl=['id', 'bibcode', 'title', 'citation_count', 'pubdate'], sort='pubdate desc', rows=2000, max_pages=need_pages)

    append_next(q, dt_list)
    make_plot(dt_list, args.save)


if __name__ == "__main__":
    main()
