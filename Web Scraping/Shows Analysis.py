from cgitb import html
from pydoc import stripid
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tqdm as tq


df = pd.DataFrame(columns=["title", "year", "season", "genre_list", "no_of_episodes", "episode_duration", 
                "first_ep_date", "studio", "source", "theme", "demographics", 
                "rating", "members", "sypnosis"])
incomplete_url = "https://myanimelist.net/anime/season/"
seasons = ['winter', 'spring', 'summer', 'fall']
years = list(range(2018, 2023))
for year in years:
    for season in seasons:
        complete_url = incomplete_url + str(year) +'/' + season
        webpage = requests.get(complete_url)
        content = webpage.content
        soup = BeautifulSoup(content, 'html.parser')
        animes = soup.find_all('div', class_ = 'js-anime-type-all')

        for anime in animes:
            title = anime.find('a', class_ = 'link-title').text
            genres = anime.find_all('span', class_ = 'genre')
            genre_list = list()
            for i in genres:
                genre_list.append((i.text).strip('\n'))
            #print(genre_list)
            sypnosis = anime.find('p').text
            rating = (anime.find('div', title = 'Score').text).strip()
            #print(rating)
            members = (anime.find('div', title = 'Members').text).strip()
            #print(members)
            
            
            
            properties = anime.find_all('div', class_ = 'property')
            item_list = list()
            properties_dict = {'studio': "", 'source': "", 'theme': "", 'demographics': ""}
            for property in properties:
                
                
                #print(property)
                caption = property.find('span', class_ = 'caption').text
                
                item_list.append(caption)
            
                item = property.find_all('span', class_ = 'item')
                property_list = list()
                for k in item:
                    property_list.append(k.text)
                item_list.append(property_list)
            #print(property_list)
            #print(item_list)

            for x in range(len(item_list)):
                if (x%2 == 0):
                    if item_list[x].lower() == 'studio' or item_list[x].lower() == 'studios':
                        properties_dict['studio'] = item_list[x+1]
                    if item_list[x].lower() == 'source' or item_list[x].lower() == 'sources':
                        properties_dict['source'] = item_list[x+1]
                    if item_list[x].lower() == 'theme' or item_list[x].lower() == 'themes' :
                        properties_dict['theme'] = item_list[x+1]
                    if item_list[x].lower() == 'demographics' or item_list[x].lower() == 'demographic':
                        properties_dict['demographics'] = item_list[x+1]
            #print(properties_dict)
                    
                
            air_date = anime.find('div', class_ = 'info')
            anime_air_date = air_date.find_all('span', class_ = 'item')
            first_ep_date = (anime_air_date[0].text.rstrip('\n'))
            time_episode_string = anime_air_date[1].text.split(',')
            no_of_episodes = time_episode_string[0].strip('\n')
            episode_duration = time_episode_string[1].strip()
            # print("1 " + first_ep_date)
            # print("2 " + no_of_episodes)
            # print("3 " + episode_duration)

            # print(anime.find("div", class_="title"))
            # print(anime.find("div", class_="title-text"))
            # subtitle = anime.find('h3', class_ = 'h3_anime_subtitle')
            # if (subtitle):
            #     anime_subtitle = subtitle.text
            # else:
            #     anime_subtitle = 'N/A'

            #df = pd.DataFrame(columns=["title", "year", "season", "genre_list", "no_of_episodes", "episode_duration", 
            #        "subtitle", "first_ep_date", "studio", "source", "theme", "demographics", 
            #        "rating", "members", "sypnosis"])
            
            df.loc[len(df.index)] = [title, year, season, genre_list, 
                                    no_of_episodes, episode_duration, first_ep_date,
                                    properties_dict.get('studio', "None"), properties_dict.get('source', "None"),
                                    properties_dict.get('theme', "None"), properties_dict.get('demographics', "None"),
                                    rating, members, sypnosis]

df.to_csv("anime.csv")


    #Following are ok:
    #title, year, season, genre_list
    #no_of_episodes, episode_duration
    #subtitle, first_ep_date
    #studio, source, theme, demographics
    #rating, members, sypnosis
    #print(sypnosis, sep = '\n')




    
#print(anime_subtitle)

# for property in properties:
#     caption = property.find('span', class_ = 'caption').text
#     item = property.find('span', class_ = 'item').text
#     print(caption)
#     print(item)
# property_list = list()
# for j in properties:
#     property_list.append((j.text).strip('\n'))
# print(property_list)
#print(title)
#print(sypnosis)
#for anime in animes:
