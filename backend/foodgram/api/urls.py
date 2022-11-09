from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet)

v1_router = SimpleRouter()
# v1_router.register('users', UserViewSet, basename='auth-users')
# v1_router.register(
#     r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
# )
# v1_router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(v1_router.urls)),
    # path('auth/signup/', EmailRegistrationView.as_view()),
    # path(
    #     'auth/token/', RetrieveAccessToken.as_view(), name='token_obtain_pair'
    # ),
]
