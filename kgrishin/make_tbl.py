"""
You need to have API key in ~/.ads/dev_key
This script uses ads python package: https://ads.readthedocs.io/en/latest/
Name of environment variable is ADS_DEV_KEY
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

def return_ads_sai():
	now = datetime.datetime.now()
	papers = ads.SearchQuery(q='aff: ("SAI MSU" or "Sternberg") pubdate:[%i-%i]' % (now.year, now.month), sort="citation_count")
	f = ""
	for paper in papers:
		f = f+ '<tr><td>%s</td><td>%s</td></tr>\n' % (paper.title[0], author_format(paper.author))
	return f

if __name__ == '__main__':
	r = return_ads_sai()
	print(r)
