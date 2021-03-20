import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.put(BASE + "recipes/souffle", 
    #{'name': 'souffle',
    #'ingredients': ['brocoli', 'huevos','cebolla', 'morron', 'queso crema', 'queso rallado', 'sal'],
    #'owner': 'matilde',
    #'time': '1 hora',
    #'process': 'Precalentar horno. Hervir el brocoli. Rehogar cebolla y morrón. Batir huevos con quesos. Mezclar todo y al horno 20 minutos.',
    #'tips': ['batir bien los huevos, casi a punto nieve', 'condimentar con pimienta y nuez moscada'],
    #'image': 'http://nutricionenlared.com/web/wp-content/uploads/2014/03/broccoli-feta-frittata-l-400x300.jpg'
    #})


#response = requests.delete(BASE + "recipes/souffle")

response = requests.patch(BASE + "recipes/souffle", {
    'process': 'Precalentar horno. Hervir el brocoli. Rehogar cebolla y morron. Batir huevos con quesos. Mezclar todo y al horno 20 minutos.'
})