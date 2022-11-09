import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q, Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from recipes.models import Tag, Recipe, Ingredient

# from .validators import NotFoundValidationError, username_restriction

User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         max_length=20,
#         validators=[
#             UniqueValidator(queryset=User.objects.all()),
#             username_restriction,
#         ],
#     )
#     email = serializers.EmailField(
#         max_length=30,
#         validators=[UniqueValidator(queryset=User.objects.all())],
#     )

#     class Meta:
#         fields = (
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'role',
#         )
#         model = User


# class UserSelfSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         max_length=MAX_LENGTH_MED,
#         validators=[
#             UniqueValidator(
#                 queryset=User.objects.filter(access_code__isnull=False)
#             ),
#             username_restriction,
#         ],
#     )
#     email = serializers.EmailField(
#         max_length=MAX_LENGTH_LONG,
#         validators=[
#             UniqueValidator(
#                 queryset=User.objects.filter(access_code__isnull=False)
#             )
#         ],
#         required=True,
#     )
#     role = serializers.CharField(max_length=MAX_LENGTH_MED, read_only=True)

#     class Meta:
#         fields = (
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'bio',
#             'role',
#         )
#         model = User


# class EmailRegistration(serializers.Serializer):
#     email = serializers.EmailField(
#         max_length=MAX_LENGTH_LONG,
#     )
#     username = serializers.CharField(
#         max_length=MAX_LENGTH_MED,
#         validators=[
#             username_restriction,
#         ],
#     )

#     def validate(self, data):
#         email = data.get('email')
#         username = data.get('username')
#         duplicate_email = (
#             User.objects.filter(Q(email=email))
#             .filter(~Q(username=username))
#             .exists()
#         )
#         duplicate_username = (
#             User.objects.filter(Q(username=username))
#             .filter(~Q(email=email))
#             .exists()
#         )
#         if duplicate_email:
#             raise serializers.ValidationError(
#                 {'detail': 'Email is already taken.'}
#             )
#         if duplicate_username:
#             raise serializers.ValidationError(
#                 {'detail': 'Username is already taken.'}
#             )
#         return data


# class LoginUserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     confirmation_code = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = User.objects.filter(username=data['username']).first()
#         if user == None:
#             raise NotFoundValidationError({'detail': 'User not found'})
#         check_access_code = check_password(
#             data['confirmation_code'], user.access_code
#         )
#         if not check_access_code:
#             raise serializers.ValidationError(
#                 {'detail': 'Incorrect username or access_code'}
#             )
#         return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        user = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                {
                    'detail': 'It is not allowed to create multiple reviews for same user'
                }
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'author')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ('__all__')

    def create(self, validated_data):
        genres = validated_data.pop('genre', [])
        title = Title.objects.create(**validated_data)
        title.genre.set(genres)
        return title

    def validate_year(self, value):
        year_now = dt.date.today().year
        if year_now < value:
            raise serializers.ValidationError({'detail': 'Year is invalid.'})
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return round(rating) if int(rating) == rating else float(f'{rating:.2f}')

    class Meta:
        fields = '__all__'
        model = Title
