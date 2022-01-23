from flask import jsonify, request

from app.controllers.posts_controller import create_post_controller, get_posts, generate_id
def creating(app):
    @app.post("/posts")
    def create_post():
        return create_post_controller()