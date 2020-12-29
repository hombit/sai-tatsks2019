# -*- coding: utf-8 -*-
"""Script to get list of articles written by SAI collaborators for the last month according to the ISTINA system
https://istina.msu.ru/organizations/department/275695/
"""

import requests
import re
import urllib
from bs4 import BeautifulSoup as bs
import lxml
from pprint import pprint
from datetime import datetime
import argparse



def get_date_current_month():
    """
    Function to get current month date YYYY.MM

    Returns
    -------
    int
        Year YYYY.
    int
        Month MM.
    """
    
    now = datetime.now()
    return now.year, now.month


def get_date_prev_month():
    """
    Function to get previous to the current month date YYYY.MM

    Returns
    -------
    int
        Year YYYY.
    int
        Month MM.
    """
    
    now = datetime.now()
    if now.month == 1:
        return now.year - 1, 12
    return now.year, now.month - 1


def doi2json(doi):
    """
    Return a json metadata for a given DOI.

    Parameters
    ----------
    doi : str
        web-link in format 'https://doi.org/...' or 'dx.doi.org/...'

    Returns
    -------
    str
        metada of the doi in json format.

    """

    headers = {'accept': 'application/vnd.citationstyles.csl+json'}
    r = requests.get(doi, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None

def get_pub_date(doi):
    """
    Function to get date of article's publication YYYY, MM.

    Parameters
    ----------
    doi : str
        web-link in format 'https://doi.org/...' or 'dx.doi.org/...'

    Returns
    -------
    int
        Year of publication YYYY.
    int
        Month of publication MM.

    """
    
    doi_json = doi2json(doi)
    try:
        date = doi_json['created']['date-parts'][0]
        return date[0], date[1]
    except KeyError:
        print('DOI is not found at doi.org. There is no date "created" at json metadata:')
        return None
    except TypeError:
        print('DOI is not found at doi.org. There is no json metadata:')
        return None

    
def check_if_article_is_new(doi):
    """
    Function to check if article is new (published in previous (or current) month)

    Parameters
    ----------
    doi : str
        web-link in format 'https://doi.org/...' or 'dx.doi.org/...'
    
    Returns
    -------
    tuple, bool
        True, False if the article is published in the current month and doi exists,
        False, True if the article is published in the previous month and doi exists,
        False, False else.

    """
    
    pub_date = get_pub_date(doi)
    in_current = pub_date == get_date_current_month() and pub_date is not None
    in_previous = pub_date == get_date_prev_month() and pub_date is not None
    return in_current, in_previous


def find_all_new_articles_from_author(href, current_month=True, prev_month=True):
    """
    Function to find new articles from current author, new articles may be: 
        from the current month, from the previous month or both.

    Parameters
    ----------
    href : str
        Web-link to author's page on ISTINA 'https://istina.msu.ru/profile/...'
        
    current_month : bool, optional
        if True, articles published in current month are taken into account. Default is True.
        
    prev_month : bool, optional
        if True, articles published in previous month are taken into account. Default is True.

    Returns
    -------
    articles : list
        List of new articles in format str reference to doi.org

    """
    
    request = requests.get(href)
    txt = request.text
    soup = bs(txt, features='lxml')
    articles_presoup = soup.find('h4', class_='activity_label')
    if articles_presoup is None: # если страничка на истине не имеет части со статьями, то искать нечего
        print('There is no actvity at this page:')
        return []
    articles_soup = articles_presoup.next_sibling.next_sibling # здесь .next_sibling = \n, а мне нужно следующее вложение после <h4>
    year_of_activity = articles_soup.find('ul', class_='activity')
    yr = year_of_activity.get('data-year')
    if yr is None:
        print('There is no articles at this page:')
        return []
    now_yr = get_date_current_month()
    if now_yr[1] == 1: # если текущий месяц - январь, проверяем статьи из текущего и предыдущего года
        if int(yr) < now_yr[0] - 1:
            print('There is no activity in the current or previous year:')
            return []
    elif int(yr) < now_yr[0]: # иначе проверяем статьи только из текущего года (или, возможно "будущего" - так бывает)
        print('There is no activity in the current year:')
        return []
    dois = articles_soup.find_all('a', string='DOI')
    articles = []
    for link in dois:
        doi = link.get('href')
        if doi is None: # у новых статей может не быть отмечен DOI, в таком случае мы проверяем следующую статью
            print('DOI is not found at ISTINA:')
            continue
        check = check_if_article_is_new(doi) # (!) здесь я предполагаю, что статьи на истине расположены строго по времени публикации
        if check[0] and current_month:
            articles.append(doi) # статья опубликована в данном месяце и нам это интересно
        elif check[1] and prev_month:
            articles.append(doi) # статья опубликована в предыдущем месяце и нам это интересно
        elif check[0] and not current_month:
            pass # если нас интересует выборка из предыдущего месяца, но не из текущего - надо проверить дату для следующей статьи в списке
        # elif check[1] and not prev_month: - не проверяем, так как статьи упорядочены по времени
        else:
            break # статья слишком старая - дальше искать новые статьи нет смысла
    return articles


def get_list_of_profiles(href):
    """
    Function to get web-links to the profiles in ISTINA system.

    Parameters
    ----------
    href : str
        Reference to the department workers page (single) from which the profiles should be found.

    Returns
    -------
    list
        List of web-links to the profiles from the department.

    """
    
    def find_profiles(href):
        return href and re.compile('/profile/').search(href)

    request = requests.get(href)
    txt = request.text
    soup = bs(txt, features='lxml')
    list_of_profiles = []
    for link in soup.find_all(href=find_profiles):
        cut_link = link.get('href')
        str_link = urllib.parse.urljoin('https://istina.msu.ru', cut_link)
        list_of_profiles.append(str_link)
    return list_of_profiles


def find_all_profiles(href, num_start=1, num_stop=1):
    """
    Function to get all web-links to the profiles in ISTINA system.

    Parameters
    ----------
    href : str
        Reference to the department page from which the profiles should be found.

    num_start : int, optional
        Number of the page, from which search of profiles starts. Default is 1.
        
    num_end : int, optional
        Number of the page, at which search of profiles stops. Default is 1.
    
    Returns
    -------
    profiles : list
        List of web-links to all the profiles from the department.

    """
    
    print('Collecting all profiles from the organization...')
    profiles = []
    i = num_start
    while True:
        profiles_ = get_list_of_profiles(f'{href}/workers/?&p={i}')
        if len(profiles_) == 0 or i > num_stop:
            break
        profiles += (profiles_)
        i += 1
    return profiles


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ref', default='https://istina.msu.ru/organizations/department/275695', type=str,
                        help='Reference to the department at ISTINA. Default is SAI')
    parser.add_argument('-a', '--num_start', default=1, type=int,
                        help='Number of starting search page at ISTINA')
    parser.add_argument('-b', '--num_stop', default=1, type=int,
                        help='Number of ending search page at ISTINA')
    parser.add_argument('-c', '--current', default=False, type=bool,
                        help='True if search for articles in current month. Default is False')
    parser.add_argument('-p', '--previous', default=True, type=bool,
                        help='True if search for articles in previous month. Default is True')
    return parser


def main():
    args = parser().parse_args()
    profiles = find_all_profiles(args.ref, num_start=args.num_start, num_stop=args.num_stop)
    print('Collecting all new articles from the organization...')
    all_articles = []
    for profile in profiles:
        articles = find_all_new_articles_from_author(profile, args.current, args.previous)
        print(f'Link: {profile}, articles: {articles}.')
        all_articles += articles
    all_articles = set(all_articles)
    pprint(all_articles)
    print(f'Number of found articles: {len(all_articles)}. Note that articles with incorrect DOI are neglected.')



if __name__ == '__main__':
    main()