from app.controllers.posts_controller import update_post_controller
def updating_post(app):
    @app.patch("/posts/<int:id>")
    def update_post(id):
        
        return update_post_controller(int(id))