from datetime import datetime
from turtle import pos

from markupsafe import re
from app.exc.post_doenst_exist import PostDoenstExistError
from app.exc.update_body_invalid import UpdateBodyInvalidError
from app.models.post import Post
from flask import jsonify, request
import pymongo
import os
from http import HTTPStatus

client = pymongo.MongoClient("mongodb://localhost:27017/")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")
db = client[DATABASE]

def generate_id():
    post_list = get_posts()
    does_id_exist = db.get_collection(COLLECTION).find_one({"id":len(post_list) + 1})
    if does_id_exist:
        return len(post_list)+2
    return len(post_list) + 1

def is_body_valid(body):
    post_keys=["author","content", "tags", "title"]
    body_keys = body.keys()
    print(body_keys)
    for key in body_keys:
        if key not in post_keys:
            raise UpdateBodyInvalidError
    return True

def the_post_exists(id):
    post = db.get_collection(COLLECTION).find_one({"id":int(id)})
    Post.serialize_posts(post)
    if not post:
        raise PostDoenstExistError



def create_post_controller():
    
    try:
        time_of_creation = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
        data = request.get_json()
        post = Post(id=generate_id(), created_at=time_of_creation, updated_at=time_of_creation,**data )
        post.create_post()
        Post.serialize_posts(post)
        return post.__dict__, HTTPStatus.CREATED

    except TypeError:
        return {"msg":"Missing required fields or given more than necessary"}, HTTPStatus.BAD_REQUEST


def delete_post_controller(id):
    try:
        the_post_exists(id)
        deleted_post = db.get_collection(COLLECTION).find_one_and_delete({"id":id})
        Post.serialize_posts(deleted_post)
        return deleted_post, HTTPStatus.ACCEPTED
    except PostDoenstExistError:
        return {"msg":"invalid id"}, HTTPStatus.NOT_FOUND


def get_post_by_id(id):
    try:
        the_post_exists(id)
        post = db.get_collection(COLLECTION).find_one({"id":id})
        Post.serialize_posts(post)
        return post, HTTPStatus.OK
    except PostDoenstExistError:
        return {"msg":"Invalid id"}, HTTPStatus.NOT_FOUND



def get_posts():
    posts_list = list(Post.get_all_posts())
    
    Post.serialize_posts(posts_list)
    return posts_list
    

def update_post_controller(id):
    try:
        data = request.get_json()
        posts_list = get_posts()
        posts_list[int(id) - 1]
        is_body_valid(data)

        
        time_of_update = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
        data.update({"updated_at":time_of_update})
        updated_post = db.get_collection(COLLECTION).find_one_and_update({"id":id}, {"$set":data}, return_document=pymongo.ReturnDocument.AFTER)
        Post.serialize_posts(updated_post)

        return updated_post, HTTPStatus.OK

    except UpdateBodyInvalidError:
        return {"msg":"This field cant be updated or doenst exist."}, HTTPStatus.BAD_REQUEST

    except IndexError:
        return {"msg":"invalid id"}, HTTPStatus.NOT_FOUND


