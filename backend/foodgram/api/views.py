from django.contrib.auth import get_user_model

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag
from users.models import MyUser
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeCreateSerializer, UserSubscribeSerializer,
                          UserSerializer)
from .permissions import IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
from .paginators import PageLimitPagination

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    pagination_class = PageLimitPagination

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if user.subscribe.filter(id=author.id).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)
        user.subscribe.add(author)
        follow = user.subscribe.get(id=author.id)
        serializer = UserSubscribeSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if user.subscribe.filter(id=author.id).exists():
            user.subscribe.remove(author)
            return Response({
                'success': 'Успешная отписка'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = MyUser.objects.filter(subscribers__in=[user])
        pages = self.paginate_queryset(queryset)
        serializer = UserSubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        print(queryset)
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageLimitPagination


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageLimitPagination


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly, )
    pagination_class = PageLimitPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
