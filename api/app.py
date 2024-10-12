from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Récupérer la clé API depuis l'environnement
DICTIONARY_API_URL = "https://dictionaryapi.com/api/v3/references/sd4/json/"
API_KEY = os.getenv('API_KEY_DICTIONARY')

@app.route('/define/<word>', methods=['GET'])
def define_word(word):
    response = requests.get(f"{DICTIONARY_API_URL}{word}?key={API_KEY}")
    
    if response.status_code == 200:
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            definitions = []
            
            for entry in data:
                for definition in entry.get('def', []):
                    for sense in definition.get('sseq', []):
                        for item in sense:
                            if isinstance(item, list):
                                sense_data = item[1]
                                short_def = sense_data.get('dt', [])
                                
                                for def_item in short_def:
                                    if isinstance(def_item, list) and def_item[0] == "text":
                                        definitions.append(def_item[1].replace('{bc}', '').strip())
            
            return jsonify({"word": word, "definitions": definitions})
        else:
            return jsonify({"error": "No definitions found for the word."}), 404
    else:
        return jsonify({"error": "Error accessing the dictionary API."}), response.status_code

if __name__ == '__main__':
    # Lancer Flask sur l'hôte 0.0.0.0 et le port 5000
    app.run(host="0.0.0.0", port=5000)
