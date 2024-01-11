from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_restful import Api
# semantic/src/models/predict.py
# from src.models.predict import MostSimilarWord, MostSimilarVerse
from src.models.prediksi import MostSimilarWord, SemantikSearch, SinonimSearch

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# This will enable CORS for all routes
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def apiView():
    return render_template('api.html')


# routes to apis
api.add_resource(MostSimilarWord, '/api/semantic/similar-word/<string:word>')
api.add_resource(SemantikSearch,
                 '/api/semantic/similar-verse/<string:query>')
api.add_resource(SinonimSearch,
                 '/api/semantic/similar-verse-sinonim/<string:query>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
