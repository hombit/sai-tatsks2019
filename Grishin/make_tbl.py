"""
You need to have API key in ~/.ads/dev_key
This script uses ads python package: https://ads.readthedocs.io/en/latest/
Name of environment variable is ADS_DEV_KEY
You need to have ads package installed
"""

import ads
import datetime

def author_format(a_l):
	fs = ''
	if len(a_l) == 1:
		fs = a_l[0]
	if len(a_l) == 2:
		fs = a_l[0] + ' & ' + a_l[1]
	if len(a_l) > 2:
		fs = a_l[0] + ' et al.'
	return fs

def return_ads_sai(now):
	papers = ads.SearchQuery(q='aff: ("SAI MSU" or "Sternberg") pubdate:[%i-%i]' % (now.year, now.month), sort="citation_count")
	f = "\n".join('<tr><td>%s</td><td>%s</td></tr>' % (paper.title[0], author_format(paper.author)) for paper in papers)
	return f

if __name__ == '__main__':
	r = return_ads_sai(datetime.datetime.now())
	print(r)
