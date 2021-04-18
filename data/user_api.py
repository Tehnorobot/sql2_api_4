import flask

from data import db_session
from data.users import User
from flask import jsonify
from flask import request, render_template, redirect, url_for, session
from api_utils2 import get_coords
import requests
import sys
import sqlalchemy


blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'position', 'address', 
                  'speciality', 'email', 'hashed_password', 'modified_date', 'city_from']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    try:
        user = User(
            id=request.json['id'],
            name=request.json['name'],
            surname=request.json['surname'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            email=request.json['email'],
            hashed_password=request.json['hashed_password'],
            city_from=request.json['city_from']
        )
        db_sess.add(user)
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'error': 'Id already exists'})
    return jsonify({'success': 'OK'})

@blueprint.route('/api/user')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'address', 
                  'speciality', 'email', 'hashed_password', 'modified_date', 'city_from'))
                 for item in users]
        }
    )
        
@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=(
                'id', 'name', 'surname', 'age', 'position', 'address', 
                  'speciality', 'email', 'hashed_password', 'modified_date', 'city_from'))
        }
    )

@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/user/<int:user_id>/<string:str_surname>/<string:str_name>/<string:str_age>/<string:str_position>/<string:str_speciality>/<string:str_address>/<string:str_email>/<string:str_hashed_password>', methods=['PUT'])
def edit_user(user_id, str_surname, str_name, str_age, str_position, str_speciality, str_address, str_email, str_hashed_password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.name = str_name
    user.surname = str_surname
    user.age = str_age
    user.position= str_position
    user.speciality = str_speciality
    user.address = str_address
    user.email = str_email
    user.hashed_password = str_hashed_password
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/show',  methods=['GET'])
def show():
    name=request.args.get('name')
    surname=request.args.get('surname')
    city=request.args.get('city')
    map_file=request.args.get('map_file')
    return render_template('map.html', name=name, surname=surname, city=city, path=map_file)

@blueprint.route('/users_show/<int:user_id>', methods=['GET', 'POST'])
def show_city(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    city = user.city_from
    surname = user.surname
    name = user.name
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    if not user:
        return jsonify({'error': 'Not found'})
    toponym_coodrinates = get_coords(city)
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = "0.2"
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "sat"
    }
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=map_params)

    if not response:
        print("Ошибка выполнения запроса:")
        sys.exit(1)
    map_file = r"static/img/map" + str(visits_count) + ".png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return redirect(url_for('user_api.show', map_file=map_file, name=name, surname=surname, city=city))