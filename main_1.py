from data import db_session, user_api
from flask import Flask
from flask import make_response, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(user_api.blueprint)
    app.run()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
if __name__ == '__main__':
    main()