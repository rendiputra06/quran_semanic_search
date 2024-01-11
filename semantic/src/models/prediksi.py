from requests import get
from flask import jsonify, make_response
from flask_restful import Resource
from gensim.models.fasttext import load_facebook_model
from gensim.models import Word2Vec
from .preprocess2 import *
from .fungsi_semantik import *
from .pooling import *
from .sinonim import pencarian

# model_tw = Word2Vec.load('././models/full_grams_cbow_100_twitter.mdl').wv
# model_wiki = Word2Vec.load("././models/indonesia/wiki.id.case.model").wv
# model_pakai = load_facebook_model('././models/fasttext/wiki.id.bin').wv
model_pakai = Word2Vec.load(
    '././models/word2vec/idwiki/idwiki_word2vec_200_new_lower.model').wv


quran_clean_text = get_quran_indo_clean_text()


def fetch(verse_ids):
    output = []
    for id in verse_ids:
        url = f"http://localhost:8000/api/lexical/verse-in-quran/{id}"
        headers = {'content-type': 'application/json'}
        results = get(url, headers=headers)
        results = results.json()
        output.append(results['data'])
    return output


class MostSimilarWord(Resource):

    def get(self, word):
        '''Outputs the 50 most similar words [from the Holy Quran],
        besides their relative similarity scores for the given word.

        @param word: the word to use
        @type word: str
        @return: the 50 most similar words from the Holy Quran] + similarity scores
        @rtype: list of tuples (score, word)
        '''
        word_scores = []
        for verse in quran_clean_text:
            for word in verse:
                if word not in model_pakai:
                    score = model_pakai.similarity(word, verse)
                    word_scores.append((score, word))
        word_scores.sort(reverse=True)

        out = word_scores[:min(len(word_scores), 50)]
        return make_response(jsonify({'results': out}), 200)


class SemantikSearch(Resource):

    def get(self, query):
        '''
        Outputs the 10 most similar words from the Holy Quran,
        besides their relative frequency scores for the given query.

        @param query: the query to use
        @type query: str
        @return: props of the most similar verses from the Holy Quran
        @rtype: list of tuples (score, verse_id, verse)

        '''
        results = search_by_sentence(query, model_pakai, get_verse_max_score)
        # kata = search_by_word(query, model_pakai, get_verse_max_score)
        # kata = search_similar_word(query, model_pakai)
        kata = search_similar_word_with_scores(query, model_pakai)
        # Fixing: TypeError(Object of type float32 is not JSON serializable)
        for idx, (score, verse_id, verse) in enumerate(results):
            tmp = (float(score), verse_id, verse)
            results[idx] = tmp

        print(kata)

        results = [verse_id+1 for score, verse_id, verse in results]
        results = fetch(results)

        return make_response(jsonify({'length': len(results), 'data': results, 'kata': kata}), 200)


class SinonimSearch(Resource):

    def get(self, query):
        '''
        Outputs the 10 most similar words from the Holy Quran,
        besides their relative frequency scores for the given query.

        @param query: the query to use
        @type query: str
        @return: props of the most similar verses from the Holy Quran
        @rtype: list of tuples (score, verse_id, verse)

        '''
        mintaData, kata = pencarian(query)

        results = [verse_id for verse_id, score, verse in mintaData[1:20]]
        # kata = [word for verse_id, score, word in mintaData[1:20]]
        results = fetch(results)

        return make_response(jsonify({'length': len(results), 'data': results, 'kata': kata}), 200)
