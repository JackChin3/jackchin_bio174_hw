#!/usr/bin/env python
# coding: utf-8

import requests
import urllib
from datetime import datetime
import pprint
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'API KEY HERE'
GAME_ID = 'a6448f2e94bb1a509384e83b754ab2e5'

def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}

def get_nba_games():
    now = datetime.now()
    print(now.strftime('%Y-%m-%d'))
    query_params = {
        'date': now.strftime('%Y-%m-%d'),
        # 'date': '2024-04-26',
         'tz': 'America/New_York',
         'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/nba?' + params
    return get_request(url)

def parse_games(data):
    games = data.get('games', [])
    return {f"{game['home_team']} vs {game['away_team']}": game['game_id'] for game in games}

def get_ncaab_games():
    now = datetime.now()
    print(now.strftime('%Y-%m-%d'))
    query_params = {
        'date': now.strftime('%Y-%m-%d'),
        # 'date': '2024-03-20',
         'tz': 'America/New_York',
         'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/ncaab?' + params
    return get_request(url)

def get_leagues():
    now = datetime.now()
    print(now.strftime('%Y-%m-%d'))
    query_params = {
        'api_key': API_KEY,
        'date': now.strftime('%Y-%m-%d'),
        # 'date': '2024-03-20',
         'tz': 'America/New_York',
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/leagues?' + params
    return get_request(url)

def get_game_info(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/game/' + game_id + '?' + params
    return get_request(url)

def get_markets(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/markets/' + game_id + '?' + params
    return get_request(url)

def get_most_recent_odds(game_id, market):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/odds/' + game_id + '/' + market + '?' + params
    print(url)
    df = get_request(url)
    return df

def no_vig(over, under):
    if over > 0:
        overp = (100 / (over + 100))
    else:
        overp = abs(over) / ((abs(over) + 100))
    if under > 0:
        underp = 100 / (under + 100)
    else:
        underp = abs(under) / (abs(under) + 100)
    no_vig_over = overp / (overp + underp)
    return round((no_vig_over * 100), 1)

def format_pinnacle(data):
    df = pd.DataFrame.from_dict(data)
    df['over'] = np.where(df['name']== 'Over', df['odds'], False)
    df['under'] = np.where(df['name']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    # combined_df['implied_over'] = no_vig(combined_df['over'], combined_df['under'])
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)

    return combined_df

def format_fanduel(data):
    df = pd.DataFrame.from_dict(data)
    df['o/u'] = df['name'].str.split(' ').str[-1]
    df['over'] = np.where(df['o/u']== 'Over', df['odds'], False)
    df['under'] = np.where(df['o/u']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    combined_df = combined_df[combined_df['over'] < 1000]
    combined_df = combined_df[combined_df['over'] > -1000]
    combined_df = combined_df[combined_df['under'] < 1000]
    combined_df = combined_df[combined_df['under'] > -1000]
    combined_df = combined_df[combined_df['over'] != 0]
    combined_df = combined_df[combined_df['under'] != 0]
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)
    return combined_df

def format_dk(data):
    df = pd.DataFrame.from_dict(data)
    df['o/u'] = df['name'].str.split(' ').str[0]
    df['over'] = np.where(df['o/u']== 'Over', df['odds'], False)
    df['under'] = np.where(df['o/u']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    combined_df = combined_df[combined_df['over'] < 1000]
    combined_df = combined_df[combined_df['over'] > -1000]
    combined_df = combined_df[combined_df['under'] < 1000]
    combined_df = combined_df[combined_df['under'] > -1000]
    combined_df = combined_df[combined_df['over'] != 0]
    combined_df = combined_df[combined_df['under'] != 0]
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)
    return combined_df

def format_caesars(data):
    df = pd.DataFrame.from_dict(data)
    df['over'] = np.where(df['name']== 'Over', df['odds'], False)
    df['under'] = np.where(df['name']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    # combined_df['implied_over'] = no_vig(combined_df['over'], combined_df['under'])
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)

    return combined_df

def format_betmgm(data):
    df = pd.DataFrame.from_dict(data)
    df['o/u'] = df['name'].str.split(' ').str[0]
    df['over'] = np.where(df['o/u']== 'Over', df['odds'], False)
    df['under'] = np.where(df['o/u']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    combined_df = combined_df[combined_df['over'] < 1000]
    combined_df = combined_df[combined_df['over'] > -1000]
    combined_df = combined_df[combined_df['under'] < 1000]
    combined_df = combined_df[combined_df['under'] > -1000]
    combined_df = combined_df[combined_df['over'] != 0]
    combined_df = combined_df[combined_df['under'] != 0]
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)
    return combined_df

def format_barstool(data):
    df = pd.DataFrame.from_dict(data)
    df['over'] = np.where(df['name']== 'Over', df['odds'], False)
    df['under'] = np.where(df['name']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    # combined_df['implied_over'] = no_vig(combined_df['over'], combined_df['under'])
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)

    return combined_df

def format_betrivers(data):
    df = pd.DataFrame.from_dict(data)
    df['o/u'] = df['name'].str.split(' ').str[0]
    df['over'] = np.where(df['o/u']== 'Over', df['odds'], False)
    df['under'] = np.where(df['o/u']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    combined_df = combined_df[combined_df['over'] < 1000]
    combined_df = combined_df[combined_df['over'] > -1000]
    combined_df = combined_df[combined_df['under'] < 1000]
    combined_df = combined_df[combined_df['under'] > -1000]
    combined_df = combined_df[combined_df['over'] != 0]
    combined_df = combined_df[combined_df['under'] != 0]
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)
    return combined_df

def format_pointsbet(data):
    df = pd.DataFrame.from_dict(data)
    df['o/u'] = df['name'].str.split(' ').str[-2]
    df['over'] = np.where(df['o/u']== 'Over', df['odds'], False)
    df['under'] = np.where(df['o/u']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    combined_df = combined_df[combined_df['over'] < 1000]
    combined_df = combined_df[combined_df['over'] > -1000]
    combined_df = combined_df[combined_df['under'] < 1000]
    combined_df = combined_df[combined_df['under'] > -1000]
    combined_df = combined_df[combined_df['over'] != 0]
    combined_df = combined_df[combined_df['under'] != 0]
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)
    return combined_df

def format_fliff(data):
    df = pd.DataFrame.from_dict(data)
    df['o/u'] = df['name'].str.split(' ').str[-2]
    df['over'] = np.where(df['o/u']== 'Over', df['odds'], False)
    df['under'] = np.where(df['o/u']== 'Under', df['odds'], False)
    combined_df = df.groupby(['handicap', 'participant_name']).agg({'over': 'sum', 'under': 'sum'}).reset_index()
    combined_df = combined_df[combined_df['over'] < 1000]
    combined_df = combined_df[combined_df['over'] > -1000]
    combined_df = combined_df[combined_df['under'] < 1000]
    combined_df = combined_df[combined_df['under'] > -1000]
    combined_df = combined_df[combined_df['over'] != 0]
    combined_df = combined_df[combined_df['under'] != 0]
    combined_df['implied_over'] = combined_df.apply(lambda row: no_vig(row['over'], row['under']), axis=1)
    return combined_df

def check_books_assists(assists):
        books = assists['sportsbooks']
        formatted_pinnacle = None
        formatted_fanduel = None
        formatted_dk = None
        formatted_caesars = None
        formatted_betmgm = None
        formatted_barstool = None
        formatted_betrivers = None
        formatted_pointsbet = None
        formatted_fliff = None
        for book in books:
                #print(book['bookie_key'])
                if book['bookie_key'] =='pinnacle':
                        formatted_pinnacle = format_pinnacle(get_book_assists('pinnacle', assists))
                elif book['bookie_key'] =='fanduel':
                        formatted_fanduel = format_fanduel(get_book_assists('fanduel', assists))
                elif book['bookie_key'] =='draftkings':
                        formatted_dk = format_dk(get_book_assists('draftkings', assists))
                elif book['bookie_key'] =='caesars':
                        formatted_caesars = format_caesars(get_book_assists('caesars', assists))
                elif book['bookie_key'] =='betmgm':
                        formatted_betmgm = format_betmgm(get_book_assists('betmgm', assists))
                elif book['bookie_key'] =='barstool':
                        formatted_barstool = format_barstool(get_book_assists('barstool', assists))
                elif book['bookie_key'] =='betrivers':
                        formatted_betrivers = format_betrivers(get_book_assists('betrivers', assists))
                elif book['bookie_key'] =='pointsbet':
                        formatted_pointsbet = format_pointsbet(get_book_assists('pointsbet', assists))
                elif book['bookie_key'] =='fliff':
                        formatted_fliff = format_fliff(get_book_assists('fliff', assists))
        for df in [formatted_pinnacle, formatted_fanduel, formatted_dk, formatted_caesars, formatted_betmgm, formatted_barstool, formatted_betrivers, formatted_pointsbet, formatted_fliff]:
                if df is not None:
                        df['o/u'] = df.apply(lambda row: [row['over'], row['under']], axis=1)
                        df.drop(['over', 'under'], axis=1, inplace=True)


        dataframes = [df.set_index(['participant_name', 'handicap']) for df in [formatted_pinnacle, formatted_fanduel, formatted_dk, formatted_caesars, formatted_betmgm, formatted_barstool, formatted_betrivers, formatted_pointsbet, formatted_fliff] if df is not None]

        names = ['pinnacle', 'fanduel', 'dk', 'caesars', 'betmgm', 'barstool', 'betrivers', 'pointsbet', 'fliff']

    # Concatenate the dataframes along the columns axis, creating a MultiIndex
        merged_df = pd.concat(dataframes, axis=1, keys=names)
        merged_df = merged_df.dropna(subset=[('pinnacle', col) for col in ['o/u', 'implied_over']])

        merged_df.insert(loc=0, column=('agg_odds', ''), value=merged_df.xs('implied_over', axis=1, level=1).mean(axis=1))



        # cols = merged_df.columns.tolist()
        # cols.insert(1, cols.pop(cols.index('agg_odds')))
        # merged_df = merged_df.reindex(columns=cols)

        return merged_df
        

def get_book_assists(name, assists):
    books = assists['sportsbooks']
    for book in books:
        if book['bookie_key'] == name:
            the_book = book['market']['outcomes']
            return the_book



def get_usage():
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/usage?' + params
    print(get_request(url))
    return get_request(url)


prop_mapping = {
    'Points': 'player_points_over_under',
    'Assists': 'player_assists_over_under',
    'Rebounds': 'player_rebounds_over_under',
    'Points + Assists': 'player_assists_points_over_under',
    'Points + Rebounds': 'player_points_rebounds_over_under',
    'Assists + Rebounds': 'player_assists_rebounds_over_under',
    'Points + Assists + Rebounds': 'player_assists_points_rebounds_over_under',
    'Steals': 'player_steals_over_under',
    'Threes': 'player_threes_over_under',
    'Turnovers': 'player_turnovers_over_under',
    'Blocks': 'player_blocks_over_under',
    'Blocks + Steals': 'player_blocks_steals_over_under',
}

table_styles=[
    dict(selector="th",       props="font-size: 0.8em; "),
    dict(selector="td",       props="font-size: 0.8em; text-align: right"),
    # dict(selector='tr:hover', props='background-color: yellow')
]

def color_based_on_value(val):
    """
    Colors values based on their distance from 50.
    """
    distance = abs(val - 50)
    if distance <= 5:
        # Scale the redness from 0 to 255 based on the distance from 50
        redness = int((distance / 5) * 255)
        return f'background-color: rgb({redness}, 0, 0)'
    else:
        # Scale the greenness from 0 to 255 based on the distance from 55
        greenness = int(((distance - 5) / 45) * 255)
        return f'background-color: rgb(0, {greenness}, 0)'

props = list(prop_mapping.keys())
selected_prop = st.selectbox('Select a prop:', props)

games_data = get_nba_games()
games = parse_games(games_data)
selected_game = st.selectbox('Select a game:', games)
if selected_game and selected_prop:
    df = check_books_assists(get_most_recent_odds(games[selected_game], prop_mapping[selected_prop]))
    # Print the resulting dataframe to the Streamlit page
    
    df = df.round(2)
    
    with st.container():

        st.markdown(
        f'<div style="text-align: center; overflow-x: auto;">'
        f'<style>'
        f'table {{width: 100%;}}'  # Adjust width as needed
        f'</style>'
        f'{df.to_html(float_format="%.2f")}'
        f'</div>',
        unsafe_allow_html=True
        )
