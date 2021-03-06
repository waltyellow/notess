from app import server
from app.user import api as user_api
from app.knowledge import api as knowledge_api

from flask import render_template, make_response, request
from app.store.database import Database

db = Database()


@server.route('/')
def hello():
    return render_template('index.html', isNew=True, note_id=-1)


@server.route('/docs', methods=['GET'])
def load_editor():
    # TODO: validate user identity
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response("No note id")
    try:
        user_name = request.args['user_name']
    except KeyError:
        return make_response("No user id")
    try:
        found_result = db.get_note(note_id=note_id, username=user_name)
        return_text = found_result['text'].replace('\n', ' ')
        if found_result is not None:
            return render_template('index.html', isNew=False, note_id=note_id, note_title=found_result['note_name'], note_text=return_text)
    except:
        print("caught some unknown error")
    return render_template('index.html', isNew=True, note_id=-1)


@server.route('/notes')
def notes_page():
    return render_template('notes_page.html')


@server.route('/edit', methods=['GET'])
def edit_page():
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response("No note id")
    try:
        user_id = request.args['user']
    except KeyError:
        return make_response("No user id")
    return render_template('edit_page.html', userId=user_id, noteId=note_id)
