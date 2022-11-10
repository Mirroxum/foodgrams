from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet, UserViewSet)

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
