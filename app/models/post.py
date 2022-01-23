import pymongo
import os


client = pymongo.MongoClient("mongodb://localhost:27017/")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")
db = client[DATABASE]


class Post():
    def __init__(self,id, created_at, updated_at, title, author, tags, content) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.title = title.title()
        self.author  = author.title()
        self.tags = tags
        self.content = content

    def __repr__(self) -> str:
        return f"Titulo:{self.title} | Autor:{self.author} | id:{self.id}"


    def create_post(self):
        db.get_collection(COLLECTION).insert_one(self.__dict__)

    @staticmethod
    def get_all_posts():
        all_posts = db.get_collection(COLLECTION).find()
        return all_posts

    @staticmethod
    def serialize_posts(data):
        if type(data) is list:
            for post in data:
                post.update({"_id":str(post["_id"])})


        if type(data) is Post:
            data._id = str(data._id)

        if type(data) is dict:
            data.update({"_id":str(data["_id"])})
