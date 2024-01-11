from IPython.display import display, clear_output
import pickle
import pandas as pd
import itertools
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import string
import urllib.request
from bs4 import BeautifulSoup
import ast
print('ini adalah tempat test kode sebelum jalan karena restart lama kali')


factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
stemmer = StemmerFactory().create_stemmer()

vectorizer = TfidfVectorizer(use_idf=True)
query = 'dosa besar'
query = query.lower()
remove_punctuation_map = dict((ord(char), None)
                              for char in string.punctuation)
query = query.translate(remove_punctuation_map)
query = stopword.remove(query)
query = query.split()
query = [stemmer.stem(x) for x in query]

# Read data from Excel into a DataFrame
df_read = pd.read_excel('data/quran-words.xlsx', header=None)
df_read2 = pd.read_excel('data/thesaurus-quran.xlsx', header=None)
df_read3 = pd.read_excel('data/processed_quran.xlsx', header=None)

# Convert DataFrame to a list (assuming each row is a separate entry)
words = df_read[0].tolist()
thesaurus = df_read2.set_index(0).to_dict()[1]
processed_paper = df_read3[0].tolist()

# generate query expansion
list_synonym = []
for x in query:
    if x in words:
        list_synonym.append(thesaurus[x])
    else:
        name = x
        data = {"q": name}
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        content = urllib.request.urlopen(
            "http://www.sinonimkata.com/search.php", encoded_data)
        soup = BeautifulSoup(content, 'html.parser')
        try:
            synonym = soup.find('td', attrs={'width': '90%'}).find_all('a')
            synonym = [x.getText() for x in synonym]
            thesaurus[x] = [x] + synonym
            list_synonym.append(thesaurus[x])
        except:
            list_synonym.append([x])
# Convert string representation of lists back to lists
list_synonym = [ast.literal_eval(item) if isinstance(
    item, str) else item for item in list_synonym]

qs = []
for xy in itertools.product(*list_synonym):
    xy = [stemmer.stem(y) for y in xy]
    qs.append([' '.join(xy)])

# process the query

max_result = []
for x in qs:
    paper_tfidf = vectorizer.fit_transform(x + processed_paper)
    q = paper_tfidf[0]
    result = cosine_similarity(paper_tfidf, q)
    idx = np.argsort(-result, axis=0).flatten()
    final = [[num, y[0], x] for num, y in enumerate(result) if y[0] > 0.0]
    max_result += final
max_result = sorted(max_result, key=lambda x: x[1], reverse=True)
set_result = set()
new_result = []
for item in max_result:
    if item[0] not in set_result:
        set_result.add(item[0])
        new_result.append(item)
    else:
        pass

print(new_result)
