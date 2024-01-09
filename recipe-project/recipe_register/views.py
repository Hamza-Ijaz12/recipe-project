from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
def recipesearch(request):
    recipes_data = []
    message=''
    if request.method == 'POST':
        query = request.POST.get('query')
        if request.user.is_authenticated:
            app_id = '778cc34b'
            app_key = '2ed4eb4f8744acd70309b028042cd179'

            url = f'https://api.edamam.com/api/recipes/v2'
            params = {
                'type': 'public',
                'q': query,
                'app_id': app_id,
                'app_key': app_key,
                
            }

            response = requests.get(url, params=params).json()
            if response['hits']==[]:
                message='No result found'
            hits = response['hits']
            print(response)
            if 'recipes' in request.session:
                del request.session['recipes']
            # Prepare the recipe data
            recipe_id = 1
            for hit in hits:
                recipe_title = hit['recipe']['label']
                ingredients = hit['recipe']['ingredientLines']
                nutrient_dic = hit['recipe']['totalNutrients']
                image_path = hit['recipe']['image']

                # Formatted nutrients for a recipe
                formatted_nutrients = []
                for nutrient, details in nutrient_dic.items():
                    label = details['label']
                    quantity = round(details['quantity'], 1)
                    unit = details['unit']
                    if quantity > 0.1 and label != 'Water':
                        # formatted_nutrients.append(f"{label} {quantity:.2f}{unit}")
                        formatted_nutrients.append([label, f"{quantity:.2f} {unit}"])


                # Append recipe data to the list
                recipes_data.append({
                    'id': recipe_id,
                    'title': recipe_title,
                    'ingredients': ingredients,
                    'nutrients': formatted_nutrients,
                    'image_path':image_path
                })
                recipe_id += 1
        else:
            message='Login is required'
    
    request.session['recipes']=recipes_data
    context = {'recipes_data':recipes_data,'message':message}
    return render(request, 'auth_user/index.html', context)


# for indvivual recipe
@login_required(redirect_field_name='login')
def recipedetail(request,pk):
    if 'recipes' in request.session:
        data = request.session['recipes']
    else:
        data = []
    desired_recipe = None
    for recipe in data:
        if recipe['id'] == int(pk):
            print('=========')
            desired_recipe = recipe
            
            break  
    context = {'desired_recipe':desired_recipe}
    return render(request, 'recipe_register/recipes-detail.html', context)