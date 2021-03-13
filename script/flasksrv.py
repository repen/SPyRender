import os
from flask import Flask

from f_api.view  import Api
from config   import BASE_DIR, PRODUCTION_WORK
from waitress import serve
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint( Api )

@app.route('/')
def index():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    return "<h1>Flask Main</h1> <p> It is currently {} </p>".format( the_time )

@app.errorhandler(404)
def error_404(error):
    return "404 Not found", 404


def app_run():
    PRODUCTION_WORK = True
    if PRODUCTION_WORK:
        serve(app, host='0.0.0.0', port=5000)
    else:
        app.run(port=5000, host='0.0.0.0', debug=True)

if __name__ == '__main__':
    app_run()