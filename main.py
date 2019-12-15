import pandas as pd
import numpy as np
from music2vec import Music2Vec
import youtube_dl
df = pd.read_csv('./output.csv')
contentIds = df['contentId'].values

m2v = Music2Vec()

ydl_opts = {
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
    'outtmpl':  "output" + '.%(ext)s',
}


for id in contentIds:

    print(id)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.nicovideo.jp/watch/'+id])

    data = m2v.load_wav('output.wav')
    label, feature = m2v.classifiy(data)
    print(m2v.to_genre(label))
    np.savetxt('./features/'+id+'.txt', feature)
