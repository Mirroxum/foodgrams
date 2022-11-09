import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import F, Q, Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField

from users.models import MyUser
from recipes.models import Tag, Recipe, Ingredient 
from foodgram.conf import MAX_LENGTH_MED_SERIALIZE, MAX_LENGTH_LONG_SERIALIZE
from .validators import NotFoundValidationError, username_restriction
from .utils import is_hex_color

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = MyUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed', )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'clolor', 'slug')
        model = Tag

    def validate_color(self, color):
        color = str(color).strip(' #')
        is_hex_color(color)
        return f'#{color}'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')
        model = Ingredient

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time')
        read_only_fields = (
            'is_favorited',
            'is_in_shopping_cart'
        )
        model = Recipe

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return False if user.is_anonymous else user.favorites.filter(
            id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return False if user.is_anonymous else user.carts.filter(
            id=obj.id).exists()
