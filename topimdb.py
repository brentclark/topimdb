#!/usr/bin/env python3

import argparse
from requests_html import HTMLSession
from prettytable import PrettyTable

def main(count):
  session = HTMLSession()
  base_url = (
    f"https://www.imdb.com/search/title?title_type="
    f"feature&sort=num_votes,desc&count={count}"
  )

  try:
    htmlSource = session.get(base_url)
  except Exception as e:
    print(e)

  x = PrettyTable()
  x.field_names = ['Movie', 'Genre', 'Rating']
  x.align['Movie'] = "l"
  x.align['Genre'] = "l"

  main = htmlSource.html.find('div.lister-list', first=True)
  for m in main.find('div.lister-item-content'):
    x.add_row([
      m.find('h3 > a', first=True).text, #movie
      m.find('span.genre', first=True).text, #genre
      m.find('strong', first=True).text, #rating
    ])

  print(x)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count',
                        action='store', type=int, help='How many movies would you like to see?')
    args = parser.parse_args()
    main(args.count)
