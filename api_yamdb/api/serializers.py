from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment

from django.utils.timezone import now


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        ]

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        genre_data = validated_data.pop('genre', None)

        if category_data is not None:
            instance.category = Category.objects.get(pk=category_data['id'])
        if genre_data is not None:
            genre_ids = [genre['id'] for genre in genre_data]
            instance.genre.set(genre_ids)

        instance.save()
        return instance

    def validate_year(self, value):
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError()
        return value

    def get_rating(self, obj):
        if obj.rating is not None:
            return round(obj.rating, 2)
        return 0


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                "Оценка должна быть в диапазоне от 1 до 10."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review', 'pub_date')
from rest_framework import serializers
from reviews.models import Category, Genre, Title

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)

    # def create(self, validated_data):
    #     print(self.request.data)
    #     # serializer = UserSerializer(data=request.data)
    #     if self.request.data['username'] != 'me':
    #         return User.objects.create(**validated_data)
    #         # return super().create(request)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
