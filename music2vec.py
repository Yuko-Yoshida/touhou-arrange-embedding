from tensorflow.keras.models import load_model
from librosa.feature import melspectrogram
from librosa.util import normalize
import soundfile as sf
from PIL import Image
import numpy as np

class Music2Vec:
    def __init__(self):
        self.clf = load_model('./models/clf.h5')
        self.embed = load_model('./models/embed.h5')
        self.labels = [
            'blues',
            'classical',
            'country',
            'disco',
            'hiphop',
            'jazz',
            'metal',
            'pop',
            'reggae',
            'rock',
        ]

    def down_sampling(self, x, original, to=22050):
        ratio = original // to
        x = x[::ratio]
        return x

    def load_wav(self, filename):
        data, samplerate = sf.read(filename)
        data = self.down_sampling(data, samplerate)
        data = data[:,0]
        data = np.asfortranarray(data)
        return data

    def classifiy(self, data, num_samples=60):
        x_b = []
        rate = len(data) // num_samples
        for n in range(num_samples-1):
            d = data[n*(rate):n*(rate)+(rate)]
            mel = melspectrogram(d, n_mels=224)
            mel = Image.fromarray(mel).resize((224, 224), resample=2)
            mel = normalize(mel)
            mel = np.expand_dims(mel, -1)
            x_b.append(mel)
        x = np.array(x_b)
        label = self.clf.predict(x)
        label = np.mean(label, axis=0).argmax()
        feature = self.embed.predict(x)
        feature = np.mean(feature, axis=0)
        return label, feature

    def to_genre(self, label):
        return self.labels[label]

    def cos_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
