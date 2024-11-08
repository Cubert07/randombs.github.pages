from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'MuBC1EstEby8rRH6Td2J'

@app.route('/', methods=['GET', 'POST'])
def login():

    with open("database.json") as json_file:
        user = json.load(json_file)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in user and user[email]["password"] == password:
            session['email'] = email
            session['username'] = user[email]['name']
            session['list'] = user[email]['list']
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Please try again.", 401
    else:
        if session.get('logged_in'):
            return redirect(url_for('home'))
        else:
            return render_template('login.html')

@app.route('/home', methods = ['POST', 'GET'])
def home():
    with open("database.json") as json_file:
        user = json.load(json_file)
    session['list'] = user[session['email']]['list']

    if request.method == 'POST':
        item = request.form['todo'].strip()
        bio = request.form['bio']

        session['list'][item] = {"item": item, "bio": bio}
        #({item: {"item": item, "bio": bio}})
        user[session['email']]['list'] = session['list']
        
        with open("database.json", "w") as outfile:
                json.dump(user, outfile)

        #2d = [[todo, description], [todo2, description], etc]
        #i jinja
        #{% for x in 2d %}
        #---lägg in html för todo--- x[0]
        #---lägg in html för description--- x[1]
    if session.get('logged_in'):
        return render_template('home.html', username=session['username'], list=session['list'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logged_in'] = None
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        with open("database.json") as json_file:
            user = json.load(json_file)
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']
            if email in user:
                return render_template('register.html', taken = True)
        user.update({email: {"name": username, "password": password, "list": []}})

        with open("database.json", "w") as outfile:
            json.dump(user, outfile)
        return redirect(url_for('login'))
    else:
        return render_template('register.html')
    
@app.route('/remove/<todo>')
def remove(todo):
    with open("database.json") as json_file:
        user = json.load(json_file)

    session['list'].pop(todo)
    user[session['email']]['list'] = session['list']

    with open("database.json", "w") as outfile:
        json.dump(user, outfile)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=9000)