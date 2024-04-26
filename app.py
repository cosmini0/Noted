from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'cosmins'

notes = []
deleted_notes = []

@app.route('/')
def home():
    recent_notes = notes[-3:]  # last 3 NOTES
    return render_template('home.html', recent_notes=recent_notes)

@app.route('/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = {'title': title, 'content': content}
        notes.append(note)
        return redirect('/notes')
    return render_template('new_note.html')

@app.route('/notes')
def view_notes():
    return render_template('notes.html', notes=notes)

@app.route('/search')
def search_notes():
    query = request.args.get('query')
    filtered_notes = [note for note in notes if query.lower() in note['title'].lower()]
    return render_template('notes.html', notes=filtered_notes)

@app.route('/delete', methods=['POST'])
def delete_note():
    note_id = int(request.form['note_id'])
    deleted_note = notes.pop(note_id)
    deleted_notes.append(deleted_note)
    return redirect('/notes')

@app.route('/trash')
def view_trash():
    return render_template('trash.html', deleted_notes=deleted_notes)

@app.route('/restore', methods=['POST'])
def restore_note():
    note_id = int(request.form['note_id'])
    restored_note = deleted_notes.pop(note_id)
    notes.append(restored_note)
    return redirect('/trash')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        dark_mode = 'dark_mode' in request.form
        session['dark_mode'] = dark_mode
    else:
        dark_mode = session.get('dark_mode', False)
    feedback_sent = 'feedback_sent' in request.args
    return render_template('settings.html', feedback_sent=feedback_sent, dark_mode=dark_mode)

@app.route('/reset', methods=['POST'])
def reset_notes():
    global notes, deleted_notes
    notes = []
    deleted_notes = []
    return redirect('/settings')


@app.route('/feedback', methods=['POST'])
def send_feedback():
    feedback = request.form['feedback']
    return redirect('/settings?feedback_sent=1')

if __name__ == '__main__':
    app.run(debug=True)