import flask

from data import db_session
from data.jobs import Jobs
from flask import jsonify
from flask import request
import sqlalchemy


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 
                  'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    try:
        jobs = Jobs(
            id=request.json['id'],
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished']
        )
        db_sess.add(jobs)
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'error': 'Id already exists'})
    return jsonify({'success': 'OK'})

@blueprint.route('/api/get_jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 
                              'work_size', 'collaborators', 'start_date', 
                              'end_date', 'is_finished'))
                 for item in jobs]
        }
    )

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/jobs/<int:jobs_id>/<string:str_rem>', methods=['PUT'])
def edit_jobs(jobs_id, str_rem):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    jobs.job = str_rem
    db_sess.commit()
    return jsonify({'success': 'OK'})