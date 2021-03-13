from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import db_op
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
import requests

app = Flask(__name__)
api = Api(app)

BASE = "http://127.0.0.1:5000/"

recipe_put_args = reqparse.RequestParser()
recipe_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
recipe_put_args.add_argument("ingredients", type=list, help="Views of the video", required=True)
recipe_put_args.add_argument("owner", type=str, help="Likes on the video", required=True)
recipe_put_args.add_argument("time", type=str, help="Name of the video is required", required=True)
recipe_put_args.add_argument("process", type=str, help="Views of the video", required=True)
recipe_put_args.add_argument("tips", type=list, help="Likes on the video", required=True)
recipe_put_args.add_argument("image", type=str, help="Name of the video is required", required=True)

recipe_update_args = reqparse.RequestParser()
recipe_update_args.add_argument("name", type=str, help="Name of the video is required")
recipe_update_args.add_argument("ingredients", type=list, help="Views of the video")
recipe_update_args.add_argument("owner", type=str, help="Likes on the video")
recipe_update_args.add_argument("time", type=str, help="Name of the video is required")
recipe_update_args.add_argument("process", type=str, help="Views of the video")
recipe_update_args.add_argument("tips", type=list, help="Likes on the video")
recipe_update_args.add_argument("image", type=str, help="Name of the video is required")

resource_fields = {
	'name': fields.String,
	'ingredients': fields.List,
	'owner': fields.String,
    'time': fields.String,
	'process': fields.String,
	'tips': fields.List,
	'image': fields.Url
}

class Recipe(Resource):
    @marshal_with(resource_fields)
    def get(self, recipe_name):
        db = db_op.db_connection()
        result = db.recipes.find_one({'name': recipe_name})
        if not result:
            abort(404, message="Could not find recipe for that meal.")
		
        return result

    @marshal_with(resource_fields)
    def put(self, recipe_name):
        db = db_op.db_connection()
        result =  db.recipes.find_one({'name': recipe_name})
		
        if result:
            abort(409, message="Recipe for that meal already exists...")
		
        args = recipe_put_args.parse_args()
        new_recipe = {}
        new_recipe['name'] = args['name'] 
        new_recipe['ingredients'] = args['ingredients']
        new_recipe['owner']  = args['owner']
        new_recipe['time'] =  args['time']
        new_recipe['process'] = args['process']
        new_recipe['tips'] = args['tips']
        new_recipe['image'] = args['image']
        
        db.recipes.insert_one(new_recipe)
		
        return new_recipe, 201

    @marshal_with(resource_fields)
    def patch(self, recipe_name):
        args = recipe_update_args.parse_args()
        db = db_op.db_connection()
        result = db.recipes.find_one({'name': recipe_name})
        
        if not result:
           abort(404, message="Recipe doesn't exist, cannot update")
		
        updated_recipe = {}
        for arg in args:
            if args[arg]:
                updated_recipe[arg] = args[arg]

        #if args['name']:
		#	result.name = args['name']
		#if args['views']:
		#	result.views = args['views']
		#if args['likes']:
		#	result.likes = args['likes']

        db.recipes.update_one({'name': recipe_name}, {"$set": {updated_recipe}})
        result = db.recipes.find_one({'name': recipe_name})

        return result

    def delete(self, recipe_name):
        db = db_op.db_connection()
        result = db.recipes.find_one({'name': recipe_name})
        
        if not result:
           abort(404, message="Recipe doesn't exist, cannot delete.")
		
        db.recipes.delete_one({'name': recipe_name})
		
        return 'Deletion successful.', 204 

api.add_resource(Recipe, '/recipe/<string:recipe_name>')

@app.route('/')
def home():
    return "<h1>Welcome to my Recipe's RESTful API</h1>"

@app.route('/get_all')
def get_all():
    db = db_op.db_connection()
    response = db.recipes.find()
    return render_template(response)

if __name__ == "__main__":
    app.run(debug=True)