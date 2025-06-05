from flask import Blueprint

task_bp = Blueprint('task', __name__)

@task_bp.route('/test', methods=['GET'])
def test_task():
    return {'message': 'Task route working!'}
