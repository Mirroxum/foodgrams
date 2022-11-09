from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, Recipe, Tag
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from .permissions import IsAdminOrReadOnly

class TagViewSet(ReadOnlyModelViewSet):
    queryset=Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )

class IngredientViewSet(ReadOnlyModelViewSet):
    queryset=Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )

class RecipeViewSet(ModelViewSet):
    queryset=Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrReadOnly, )
