from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Категория")
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Жанр")
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название произведения")
    year = models.IntegerField(verbose_name="Год")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание")
    genre = models.ManyToManyField(Genre, through="TitleGenre",
                                   related_name="titles")
    category = models.ForeignKey(
        Category, related_name="titles", on_delete=models.SET_NULL, null=True
    )

    @property
    def rating(self):
        return self.reviews.aggregate(Avg('score'))['score__avg']

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="title_genres"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True,
        related_name="genre_titles")

    class Meta:
        unique_together = ('title', 'genre')

    def __str__(self):
        return f"{self.title.name} - {self.genre.name}"


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_per_user_per_title'  # Уникальное имя ограничения
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
