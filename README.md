# Recipes RESTFul API
Built in Flask with Mongo DB Atlas. The identifier for each object is the recipe name.
<br>
To host the API in your local server, run on your cmd in the project folder.
<br>
`python main.py`<br>
## GET method
#### Get one
`<base_url> +'/recipes/<recipe_name>'`
#### Get all
`<base_url> + '/recipes/'`

## PUT, PATCH and DELETE methods
Create a .py file or run the python ide in your cmd. 
`import requests`
#### Put method
`requests.put(<base_url> + 'recipes/<recipe_name>', {
  'name': 'souffle',
  'ingredients': ['brocoli', 'huevos','cebolla', 'morron', 'queso crema', 'queso rallado', 'sal'],
  'owner': 'matilde',
  'time': '1 hora',
  'process': 'Precalentar horno. Hervir el brocoli. Rehogar cebolla y morrón. Batir huevos con quesos. Mezclar todo y al horno 20 minutos.',
  'tips': ['batir bien los huevos, casi a punto nieve', 'condimentar con pimienta y nuez moscada'],
  'image': 'http://nutricionenlared.com/web/wp-content/uploads/2014/03/broccoli-feta-frittata-l-400x300.jpg'
   })`
 #### Patch method
 `requests.patch(<base_url> + /recipes/<recipe_name>, {
  'time': '50 minutes',
  'owner': 'garelik'
 })`
 
 #### Delete method
`requests.delete(<base_url> + /recipes/<recipe_name>)`
