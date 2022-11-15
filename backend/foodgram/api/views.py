from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet,
                                     GenericViewSet)
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag, AmountIngredient, Cart
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeCreateSerializer, UserSubscribeSerializer,
                          ShortRecipeSerializer)
from .permissions import IsAdminOrReadOnly
from .paginators import PageLimitPagination

User = get_user_model()


class UserSubscribeViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSubscribeSerializer
    pagination_class = PageLimitPagination

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        if request.user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if request.user.subscribe.filter(id=author.id).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)
        request.user.subscribe.add(author)
        serializer = self.get_serializer(
            author, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        is_subscribe = request.user.subscribe.filter(id=author.id).exists()
        if request.user == author:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not is_subscribe:
            return Response({
                'errors': 'Вы уже отписались'
            }, status=status.HTTP_400_BAD_REQUEST)
        request.user.subscribe.remove(author)
        return Response({
            'success': 'Успешная отписка'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def subscriptions(self, request):
        queryset = request.user.subscribe.all()
        pages = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageLimitPagination


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = PageLimitPagination

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        user = self.request.user
        if user.is_anonymous:
            return queryset
        is_in_shopping = self.request.query_params.get('is_in_shopping_cart')
        if is_in_shopping in ('1', 'true',):
            queryset = queryset.filter(cart__user=user)
        elif is_in_shopping in ('0', 'false',):
            queryset = queryset.exclude(cart__user=user)
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in ('1', 'true',):
            queryset = queryset.filter(favorite=user)
        if is_favorited in ('0', 'false',):
            queryset = queryset.exclude(favorite=user)
        return queryset

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        is_favorite = recipe.favorite.filter(id=user.id).exists()
        if is_favorite:
            return Response({
                'errors': 'Вы уже добавили этот рецепт в избраное'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe.favorite.add(user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def del_favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        is_favorite = recipe.favorite.filter(id=user.id).exists()
        if not is_favorite:
            data = {'errors': 'Такого рецепта нет в избранных.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        recipe.favorite.remove(user)
        return Response({
            'success': 'Рецепт успешно удален из избраного'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        is_cart = user.cart.filter(recipe=recipe).exists()
        if is_cart:
            return Response({
                'errors': 'Вы уже добавили этот рецепт в список покупок'
            }, status=status.HTTP_400_BAD_REQUEST)
        user.cart.create(recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        is_cart = user.cart.filter(recipe=recipe).exists()
        if not is_cart:
            data = {'errors': 'Такого рецепта нет в списке покупок.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user.cart.filter(recipe=recipe).delete()
        return Response({
            'success': 'Рецепт успешно удален из списка покупок'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user
        if not Cart.objects.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = AmountIngredient.objects.filter(
            recipe__cart__user=user
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = [f'Список покупок для:\n{user.first_name}',
                         '{user.last_name}\n\n']
        for number, ingredient in enumerate(ingredients, start=1):
            shopping_list += (
                f'{number}){ingredient["ingredient"]}:\
{ingredient["amount"]} {ingredient["measure"]}\n'
            )
        shopping_list += ['\n\nПосчитано в Foodgram\n',
                          f'{dt.now().strftime("%d/%m/%Y %H:%M")}']
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
