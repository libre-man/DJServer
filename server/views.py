from server import app


@app.route('/')
def index():
    return 'Hello World'


@app.route('/new_client')
def new_client():
    return 'Creating client'


@app.route('/join_session')
def join_session():
    return 'Joining data'


@app.route('/log_data')
def log_data():
    return 'Logging data'
