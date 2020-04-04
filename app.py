#!/usr/bin/env python3

import os
import random
import string

from flask import Flask, render_template_string, render_template, abort, send_from_directory, request, url_for, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from data import conf


users = {u: generate_password_hash(p) for u, p in conf.users_pt.items()}


def create_app():
    """ Flask application factory """
    # Create Flask app load app.config
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    app.config['MAX_CONTENT_LENGTH'] = conf.max_filesize

    auth = HTTPBasicAuth()

    def allowed_file(fn: str):
        return "." in fn and fn.rsplit(".", 1)[1].lower() in conf.exts

    @auth.verify_password
    def verify_password(username, password):
        if username in users:
            return check_password_hash(users.get(username), password)
        return False

    @app.route("/", methods=["GET", "POST"])
    @auth.login_required
    def upload():
        if request.method == "POST":
            if "file" not in request.files:
                flash("No file uploaded!")
                return render_template("upload.html", conf=conf)
            ul_file = request.files["file"]
            if ul_file.filename == "":
                flash("No file uploaded!")
                return render_template("upload.html", conf=conf)
            if ul_file and allowed_file(ul_file.filename):
                if "rename" in request.form:
                    ext = ul_file.filename.rsplit(".", 1)[1].lower()
                    name = hex(hash(ul_file)).lstrip("0x")
                    fn = secure_filename(name + "." + ext)
                else:
                    fn = secure_filename(ul_file.filename)
                ul_file.save(os.path.join(conf.upload_folder, fn))
                img_url = url_for("serve_img", fn=fn)
                flash(f"Image uploaded: <a href=\"{img_url}\">URL</a>")
            else:
                flash("Bad filetype!")
        return render_template("upload.html", conf=conf)

    @app.route("/<string:fn>")
    def serve_img(fn: str):
        try:
            return send_from_directory("images", fn)
        except FileNotFoundError:
            abort(404)
    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
