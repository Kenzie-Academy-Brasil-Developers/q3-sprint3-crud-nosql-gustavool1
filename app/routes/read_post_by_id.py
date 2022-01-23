from http import HTTPStatus
from app.controllers.posts_controller import get_post_by_id
from flask import jsonify

def read_by_id(app):
    @app.get("/posts/<int:id>")
    def read_post_by_id(id):
        return get_post_by_id(int(id))