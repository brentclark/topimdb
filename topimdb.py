#!/usr/bin/python3

import argparse
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

def main(imdb_top_n):
    """ main function """
    x = PrettyTable()
    x.field_names = ['Movie', 'Genre', 'Rating', 'Link']
    x.align['Movie'] = "l"
    x.align['Genre'] = "l"
    x.align['Link'] = "l"

    base_url = (
        f"https://www.imdb.com/search/title?title_type="
        f"feature&sort=num_votes,desc&count={imdb_top_n}"
    )

    source = BeautifulSoup(requests.get(base_url).content, "html.parser")
    for m in source.findAll("div", class_="lister-item mode-advanced"):
        x.add_row([
            m.h3.a.text.strip(), # movie's name
            m.find("span", attrs={"class": "genre"}).text.strip(), # genre
            m.strong.text.strip(), # movie's rating
            f"https://www.imdb.com{m.a.get('href')}" # movie's page link
        ])

    x.sortby = 'Rating'
    x.reversesort = True
    print(x)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count',
                        action='store', type=int, help='How many movies would you like to see?')
    args = parser.parse_args()
    main(args.count)