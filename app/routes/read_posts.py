from app.controllers.posts_controller import get_posts
from flask import jsonify
def retrieving_posts(app):
    @app.get("/posts")
    def read_posts():
        return jsonify(get_posts())