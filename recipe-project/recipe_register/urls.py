from django.urls import path,include
from . import views

urlpatterns = [
    path('find',views.recipesearch,name='find'),
    path('detail/<str:pk>',views.recipedetail,name='detail'),
    
    
]