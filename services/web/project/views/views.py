import os

from werkzeug.utils import secure_filename
from flask import (
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from flask.blueprints import Blueprint

from project.tasks.tasks import send_three_async_emails


main_app_bp = Blueprint('main_app', __name__)


@main_app_bp.route("/")
def index():
    return jsonify({"message": "Hello, World!"})


@main_app_bp.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@main_app_bp.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@main_app_bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return f"""
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """


# GET for sending emails
@main_app_bp.route("/send_me_three_emails")
def send_me_three_emails():
    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': 'nataliia.dyshko@ukr.net',
        'body': 'This is a test email sent from a background Celery task.'
    }
    task = send_three_async_emails.apply_async(args=[email_data])
    return jsonify({
        "message": "3 emails will be sent.",
        "task_id": task.task_id}
    )


@main_app_bp.route("/emails_status/<task_id>")
def emails_status(task_id):
    from project import celery
    if task_id == 'all':  # ?????????
        if not celery.current_worker_task:
            return jsonify({"message": "No current tasks."})
        task_id = celery.current_worker_task.request.id
    task = send_three_async_emails.AsyncResult(task_id)  # task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': "0"
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', "100%")
        }
        # return will get here too????
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': "??%",
            '(exception!) status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
