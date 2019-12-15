import requests
import pprint
import pandas as pd
from time import sleep

url = 'https://api.search.nicovideo.jp/api/v2/video/contents/search'
params = {
    'q': '東方自作アレンジ',
    'targets': 'tags',
    '_sort': 'startTime',
    '_offset': '0',
    '_context': 'aappii',
    'fields': 'contentId,title,viewCounter,startTime,mylistCounter,userId',
    'filters[startTime][gte]': '2014-01',
    'filters[startTime][lt]': '2014-06',
    '_limit': '100'
}
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {'User-Agent': ua}

start = str(2007)+'-'+str(1).zfill(2)
end = str(2019)+'-'+str(12).zfill(2)
date_iteration = int(12*(2019-2007+1))

dfs = []

for d in range(date_iteration):

    f = str(2007+d//12)+'-'+str(1+d%12).zfill(2)
    if d%12 == 11:
        t = str(2007+d//12+1)+'-'+str(1).zfill(2)
    else:
        t = str(2007+d//12)+'-'+str(1+d%12+1).zfill(2)

    params.update({'filters[startTime][gte]': f})
    params.update({'filters[startTime][lt]': t})

    res = requests.get(url, params=params, headers=headers)
    json = res.json()
    dfs.append(pd.DataFrame(json['data']))
    contents_count = int(json['meta']['totalCount'])

    print(f, t, contents_count)
    print(len(json['data']))

    sleep(0.1)

    iteration = round(contents_count / 100)+1
    for i in range(0, iteration):
        params.update({'_offset': i*100})
        res = requests.get(url, params=params, headers=headers)
        json = res.json()
        print(len(json['data']))
        dfs.append(pd.DataFrame(json['data']))
        sleep(0.1)

df = pd.concat(dfs)
df.drop_duplicates().reset_index(drop=True).to_csv('output.csv')
