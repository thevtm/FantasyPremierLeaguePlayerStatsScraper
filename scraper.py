# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

## The MIT License (MIT)
##
## Copyright (c) 2015 Vinícius Tabille Manjabosco
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

# <codecell>

import itertools as it
import json
import scraperwiki
import pandas as pd

# <codecell>

## Consts
PLAYER_DATA_URL = "http://fantasy.premierleague.com/web/api/elements/"

# <codecell>

def ExtractPlayerDF(Data):
    colNames = ['Date', 'Round', 'Opponent', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS',
                'PM', 'YC', 'RC', 'S', 'B', 'ESP', 'BPS', 'NT', 'Value', 'Points']
    fixtures = Data['fixture_history']['all']
    playerDF = pd.DataFrame(fixtures, columns = colNames)

    playerDF['ID'] = Data['id']
    playerDF['Code'] = Data['code']
    playerDF['WebName'] = Data['web_name']
    playerDF['FirstName'] = Data['first_name']
    playerDF['SecondName'] = Data['second_name']
    playerDF['Position'] = Data['type_name']
    playerDF['Team'] = Data['team_name']

    colOrder = ['ID', 'Code', 'Round', 'WebName', 'FirstName', 'SecondName', 'Position', 'Team',
                'Date', 'Opponent', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS', 'PM', 'YC',
                'RC', 'S', 'B', 'ESP', 'BPS', 'NT', 'Value', 'Points']

    return playerDF[colOrder]

# <codecell>

## Download data
playersDataRaw = []

for i in it.count(1):
    url = PLAYER_DATA_URL + str(i)
    try:
        playerDataJson = scraperwiki.scrape(url)
        playersDataRaw.append(json.loads(playerDataJson))
    except:
        print 'Last Player Index evaluated: ' + str(i)
        break

# <codecell>

## Mine Players Data
## and concat all into one DataFrame
PlayersData = pd.concat(map(ExtractPlayerDF, playersDataRaw), ignore_index = True)

# <codecell>

## Save DataFrame to SQLite
scraperwiki.sqlite.save(unique_keys = [],
                        data = PlayersData.to_dict(outtype = 'records'),
                        table_name = 'data')

