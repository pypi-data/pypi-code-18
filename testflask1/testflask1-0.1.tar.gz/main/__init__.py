from flask import Flask
from flask import request
from flask import abort
import json
from case_notes_suggestion import CaseNotesSuggester

'''
request = request = { "notes_summary": "Apple ID security questions"}
response = CaseNotesSuggester().get_neighbors(request, '_id', ['title', 'notes_title', 'notes_summary'],10)
print ("{\"caseId\":" + json.dumps(list(response)) + "}")
'''

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Turi Case"

@app.route('/datahub/api/v1/case/suggest', methods=['POST'])
def get_case_suggestions():
    if not request.json:
        abort(400, "Invaid json request")
    response = CaseNotesSuggester().get_neighbors(request.json, '_id', ['title', 'notes_title', 'notes_summary'],10)
    return "{\"caseId\":" + json.dumps(list(response)) + "}", 200

@app.route('/datahub/api/v1/case/testsuggest', methods=['POST'])
def testsuggest(self,summary):
    response = CaseNotesSuggester().get_neighbors_simple(summary, '_id', ['notes_summary'],10)
    return "{\"caseId\":" + json.dumps(list(response)) + "}", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
