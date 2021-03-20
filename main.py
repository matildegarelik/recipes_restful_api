from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from datetime import timedelta
import requests
import db_op
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
import requests
from bson import json_util, ObjectId
from pprint import pprint


app = Flask(__name__)
api = Api(app)

BASE = "http://127.0.0.1:5000/"

recipe_put_args = reqparse.RequestParser()
recipe_put_args.add_argument("name", type=str, help="Name required", required=True)
recipe_put_args.add_argument("ingredients", help="Ingredients required", required=True, type=str,action="append")
recipe_put_args.add_argument("owner", type=str, help="Owner required", required=True)
recipe_put_args.add_argument("time", type=str, help="Time required", required=True)
recipe_put_args.add_argument("process", type=str, help="Process required", required=True)
recipe_put_args.add_argument("tips", type=str, action="append", help="tips required", required=True)
recipe_put_args.add_argument("image", type=str, help="Image required", required=True)

recipe_update_args = reqparse.RequestParser()
recipe_update_args.add_argument("name", type=str)
recipe_update_args.add_argument("ingredients", type=str, action="append")
recipe_update_args.add_argument("owner", type=str)
recipe_update_args.add_argument("time", type=str)
recipe_update_args.add_argument("process", type=str)
recipe_update_args.add_argument("tips", type=str, action="append")
recipe_update_args.add_argument("image", type=str)

resource_fields = {
	'name': fields.String,
	'ingredients': fields.List(fields.String),
	'owner': fields.String,
    'time': fields.String,
	'process': fields.String,
	'tips': fields.List(fields.String),
	'image': fields.String
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

        print(new_recipe)
        
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
        print(updated_recipe)

        db.recipes.update_one({'name': recipe_name}, {"$set": updated_recipe})
        result = db.recipes.find_one({'name': recipe_name})

        return result

    def delete(self, recipe_name):
        db = db_op.db_connection()
        result = db.recipes.find_one({'name': recipe_name})
        
        if not result:
           abort(404, message="Recipe doesn't exist, cannot delete.")
		
        db.recipes.delete_one({'name': recipe_name})
		
        return 'Deletion successful.', 204 

api.add_resource(Recipe, '/recipes/<string:recipe_name>')

@app.route('/')
def home():
    return "<h1>Welcome to my Recipe's RESTful API</h1>"

@app.route('/recipes/')
def get_all():
    db = db_op.db_connection()
    result =  db.recipes.find()
    elements=[]
    for e in result:
        n = {}
        for k in e:
            if isinstance(e[k], ObjectId):
                n[k] =  str(e[k])
            else:
                n[k] = e[k]
        elements.append(n)
    return jsonify(elements)


if __name__ == "__main__":
    app.run(debug=True)