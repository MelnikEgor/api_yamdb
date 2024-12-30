from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def create(self, validated_data):
        genre = Genre.objects.create(**validated_data)
        return genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', write_only=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True,
        write_only=True
    )
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        ]

    def validate_year(self, value):
        if not value:
            raise serializers.ValidationError(
                "Поле year обязательно для заполнения.")
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError()
        return value

    def get_rating(self, obj):
        if obj.rating is not None:
            return round(obj.rating, 2)
        return None

    def to_representation(self, instance):
        """Переопределяем вывод данных."""
        representation = super().to_representation(instance)

        # Преобразование category
        category = instance.category
        if category:
            representation['category'] = {
                'name': category.name,
                'slug': category.slug
            }

        # Преобразование genre
        genres = instance.genre.all().distinct()
        representation['genre'] = [
            {'name': genre.name, 'slug': genre.slug} for genre in genres
        ]

        return representation


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
