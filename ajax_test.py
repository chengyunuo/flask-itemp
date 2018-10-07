from flask import (
    Flask,
    request,
    jsonify,
    render_template,
)
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('ajax.html')


@app.route('/api/set_temp', methods=['GET', 'POST'])
def set_temp():
    # data = request.form.get('todo')
    data = request.json.get('todo')
    print(data)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
