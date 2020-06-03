#!/usr/bin/env python3

import argparse
from requests_html import HTMLSession
from prettytable import PrettyTable

def main(count, sortby, sort, url):
    session = HTMLSession()
    base_url = (
        f"https://www.imdb.com/search/title/?groups={count}"
        f"&sort={sortby},{sort}"
    )
    column_names = ['Movie', 'Genre', 'Rating']

    try:
        htmlSource = session.get(base_url)
    except Exception as e:
        print(e)

    print(htmlSource.html.find('title', first=True).text)

    if url:
        column_names.append('Url')

    x = PrettyTable()
    x.field_names = column_names
    x.align['Movie'] = "l"
    x.align['Genre'] = "l"

    main = htmlSource.html.find('div.lister-list', first=True)
    for m in main.find('div.lister-item-content'):
        row_data = [
            f"{m.find('h3 > a', first=True).text} - {m.find('h3:nth-child(1) > span:nth-child(3)', first=True).text}", #movie
            m.find('span.genre', first=True).text, #genre
            m.find('strong', first=True).text, #rating
        ]

        if url:
            link = [x for x in m.find('h3:nth-child(1) > a',first=True).absolute_links][0] #url
            link = link.split('?')[0]
            row_data.append(link)

        x.add_row(row_data)

    print(x)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', choices=['top_100', 'top_250', 'top_1000'], default='top_100', help='Show either IMDB top 100, top 250, top 1000')
    parser.add_argument('-sb', '--sortby', choices=['moviemeter','alpha', 'user_rating', 'num_votes', 'boxoffice_gross_us', 'runtime', 'year', 'release_date', 'your_rating_date', 'my_ratings'], default='moviemeter', help='sort by options')
    parser.add_argument('-s', '--sort', choices=['asc', 'desc'], default='asc', help='ascending or descending sort')
    parser.add_argument('-u', '--url', action="store_true", help='show IMDB url to movie')
    args = parser.parse_args()

    main(args.count, args.sortby, args.sort, args.url)

