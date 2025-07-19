import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import re

root = 'https://www.imdb.com/search/title/?title_type=feature&countries=in&languages=hi&start='
movie_id = []
movie_name = []
year = []
genre = []
overview = []
director = []
cast = []

for pages in range(1, 2200, 50):
    print(pages)
    html = requests.get(root + str(pages) + '&ref_=adv_nxt')
    soup = BeautifulSoup(html.content, 'html.parser')

    movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        movie_name.append(name)

        id_var = store.find('div', class_='lister-item-image float-left').find('img')
        tconst = id_var.get('data-tconst')
        movie_id.append(tconst)

        year_of_release = store.h3.find('span', class_='lister-item-year text-muted unbold').text.replace(' ',
                                                                                                          '').replace(
            'I', '').replace('(', '').replace(')', '')
        year.append(year_of_release)

        genre_var = store.p.find('span', class_='genre').text.replace('\n', '').replace('            ',
                                                                                        '') if store.p.find('span',
                                                                                                            class_='genre') else ' '
        genre.append(genre_var)

        overview_var = store.findAll('p', attrs={'class': 'text-muted'})
        over = overview_var[1].text.replace('\n', '')
        overview.append(over)

        directors_var = store.findAll('p')
        direct = directors_var[2].text
        for text in direc:
            if '|' in text:
                direct = direc.split('|')[0].replace('\n', '').replace('Director:', '').replace('\n', '').replace(
                    '    ', '').replace('Directors:', '')
        director.append(direct)
        for text in direc:
            if '|' in text:
                cast_var = direc.split('|')[1].replace('\n', '').replace('Stars:', '').replace('Star:', '').replace(
                    '     ', '')
                cast.append(cast_var)

df = pd.DataFrame(
    {'movie_id':movie_id,
     'movie_name':movie_name,
     'year':year,
     'genre':genre,
     'overview':overview,
     'director':director,
     'cast':cast,
    })

#store.find('div', class_ = 'lister-item-image float-left').find('img')

df.to_csv('Movie Dataset 2023.csv')