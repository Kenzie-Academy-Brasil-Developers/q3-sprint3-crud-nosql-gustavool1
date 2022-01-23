from app.routes.create_post import creating
from app.routes.delete_post import delete
from app.routes.read_post_by_id import read_by_id
from app.routes.read_posts import retrieving_posts
from app.routes.update_post import updating_post
def init_app(app):
    creating(app)
    retrieving_posts(app)
    delete(app)
    read_by_id(app)
    updating_post(app)