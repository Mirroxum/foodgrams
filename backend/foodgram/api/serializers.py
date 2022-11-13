from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Tag, Recipe, Ingredient, AmountIngredient, Cart

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_subscribed', )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class UserSubscribeSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')
        model = Ingredient

class IngredientAmountListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredients.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredients.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit',
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountListSerializer(many=True)
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

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return False if user.is_anonymous else user.favorites.filter(
            id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return False if user.is_anonymous else Cart.objects.filter(
            user=user).exists()


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'amount'
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientRecipeCreateSerializer(many=True)
    image = Base64ImageField()
    name = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Recipe.objects.all(),
            )
        ]
    )

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_id = get_object_or_404(Ingredient, id=id)
            add_ingredient = AmountIngredient.objects.create(
                ingredients=ingredient_id, amount=amount
            )
            recipe.ingredients.add(add_ingredient)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        if validated_data.get('tags'):
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            for tag in tags_data:
                tag_id = tag.id
                tag_object = get_object_or_404(Tag, id=tag_id)
                instance.tags.add(tag_object)
        if validated_data.get('ingredients'):
            ingredients_data = validated_data.pop('ingredients')
            instance.ingredients.clear()
            for ingredient in ingredients_data:
                ingredient_id = ingredient.get('id')
                amount = ingredient.get('amount')
                ingredient_object = get_object_or_404(
                    Ingredient, id=ingredient_id)
                instance.ingredients.add(
                    ingredient_object, amount=amount
                )
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeListSerializer(
            instance,
            context=self.context
        )
        return serializer.data
