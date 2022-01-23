from flask import jsonify

from app.controllers.posts_controller import delete_post_controller


def delete(app):
    @app.delete('/posts/<int:id>')
    def delete_post(id):
        
        return delete_post_controller(id)
