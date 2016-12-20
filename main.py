import ose
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = 'br6YwkwSk5JSjo62MheXjPT9PPOjWjlbA9rG9aLJC1bmIr3WV5JarPHPwFVp3'

@app.route('/')
def trainPosition():
    data = ose.trainPosition()
    return render_template('index.html', stations=data['stations'],
                       stationsFrom=data['stationsFrom'],
                       stationsTo=data['stationsTo'],
                       from_airport=data['from_airport'],
                       to_airport=data['to_airport'])



if __name__ == '__main__':
    app.run(debug=True)
