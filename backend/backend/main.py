from flask import current_app as app
from flask import abort, request
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from sqlalchemy import desc
from werkzeug.security import generate_password_hash
from .models import User, Task
from . import db, login_manager
from .utils import bad, good
from .schemas import user_schema, tasks_schema, task_schema, users_schema


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        abort(404)

    if request.method == "POST":
        try:
            email = request.json["email"]
            first_name = request.json["first_name"]
            last_name = request.json["last_name"]
            contact_number = request.json["contact_number"]
        except KeyError:
            bad(
                "Error decoding JSON, ensure that the JSON has all the required fields"
            ), 400

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
        )
        user.set_password(request.json["password"])
        db.session.add(user)
        db.session.commit()
        return good("User registered!"), 200


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        abort(404)

    if request.method == "POST":
        try:
            email = request.json["email"]
            password = request.json["password"]
        except KeyError:
            bad(
                "Error decoding JSON, ensure that the JSON has all the required fields"
            ), 400

        user = User.query.filter_by(email=email).first()

        if user is not None:
            if user.check_password(password):
                login_user(user)
                return good("Logged in!"), 200
            else:
                return bad("Incorrect Password!"), 401
        else:
            return bad("User does not exist!"), 404


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    if request.method == "GET":
        abort(404)

    if request.method == "POST":
        logout_user()
        return good("User logged out!"), 200


@app.route("/profile", methods=["POST"])
@login_required
def profile():
    if current_user is not None:
        return good(user_schema.dump(current_user)), 200
    return bad("User does not exist!"), 400


@app.route("/new_request", methods=["POST"])
@login_required
def new_request():
    try:
        name = request.json["name"]
        contact_number = request.json["contact_number"]
        location = request.json["location"]
        address = request.json["address"]
        subject = request.json["subject"]
        description = request.json["description"]
    except KeyError:
        bad(
            "Error decoding JSON, ensure that the JSON has all the required fields"
        ), 400

    task = Task(
        name=name,
        contact_number=contact_number,
        location=location,
        address=address,
        subject=subject,
        description=description,
        help_seeker=current_user.id,
    )

    db.session.add(task)
    db.session.commit()
    return good("Help registered!"), 200


@app.route("/all_requests", methods=["POST"])
@login_required
def all_requests():
    if (request.json) is not None:
        location = request.json["location"]
        all_requests = Task.query.filter_by(location=location).all()
    else:
        all_requests = Task.query.all()

    return tasks_schema.dumps(all_requests), 200


@app.route("/request_info", methods=["POST"])
@login_required
def request_info():
    try:
        request_id = request.json["request_id"]
    except KeyError:
        bad(
            "Error decoding JSON, ensure that the JSON has all the required fields"
        ), 400

    request_object = Task.query.filter_by(id=request_id).first()

    if request_object is not None:
        return task_schema.dump(request_object), 200
    else:
        return bad("Request does not exist!"), 404


@app.route("/accept_request", methods=["POST"])
@login_required
def accept_request():
    try:
        request_id = request.json["request_id"]
        helper_id = request.json["helper_id"]
    except KeyError:
        bad(
            "Error decoding JSON, ensure that the JSON has all the required fields"
        ), 400

    request_object = Task.query.filter_by(id=request_id).first()
    print(request_object.status)

    if request_object is not None:
        request_object.status = "accepted"
        request_object.helper = helper_id
        db.session.add(request_object)
        db.session.commit()
        return good("Request accepted!"), 202
    else:
        return bad("The request does not exist!"), 404


@app.route("/reject_request", methods=["POST"])
@login_required
def reject_request():
    try:
        request_id = request.json["request_id"]
    except KeyError:
        bad(
            "Error decoding JSON, ensure that the JSON has all the required fields"
        ), 400

    request_object = Task.query.filter_by(id=request_id).first()

    if request_object is not None:
        if request_object.status == "accepted":
            request_object.status = "cancelled"
            db.session.add(request_object)
            db.session.commit()
            return good("Request cancelled!"), 202
        else:
            return bad("Only accepted requests can be rejected"), 400
    else:
        return bad("The request does not exist!"), 404


@app.route("/complete_request", methods=["POST"])
@login_required
def complete_request():
    try:
        request_id = request.json["request_id"]
    except KeyError:
        bad(
            "Error decoding JSON, ensure that the JSON has all the required fields"
        ), 400

    request_object = Task.query.filter_by(id=request_id).first()
    helper_object = User.query.filter_by(id=request_object.helper).first()

    if request_object is not None:
        if request_object.status == "accepted":
            request_object.status = "completed"
            helper_object.points = helper_object.points + 1
            db.session.add(request_object, helper_object)
            db.session.commit()
            return good("Request completed!"), 202
        else:
            return bad("Only accepted requests can be completed"), 400
    else:
        return bad("The request does not exist!"), 404


@app.route("/request_history", methods=["POST"])
@login_required
def request_history():
    history = Task.query.filter_by(id=current_user.id).all()
    return tasks_schema.dumps(history)


@app.route("/leaderboard", methods=["POST"])
def leaderboard():
    top_users = User.query.order_by(desc(User.points)).all()
    return users_schema.dumps(top_users), 200
