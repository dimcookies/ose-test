from transport.ose import ose
from flask import Flask, render_template

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True

app.secret_key = 'br6YwkwSk5JSjo62MheXjPT9PPOjWjlbA9rG9aLJC1bmIr3WV5JarPHPwFVp3'

@app.route('/')
def trainPosition():
    data = ose.trainPosition()
    return render_template('ose.html', stations=data['stations'],
                       stationsFrom=data['stationsFrom'],
                       stationsTo=data['stationsTo'],
                       from_airport=data['from_airport'],
                       to_airport=data['to_airport'])


@app.route('/css')
def css():
    return app.send_static_file('style.css')


if __name__ == '__main__':
    app.run(debug=True)
