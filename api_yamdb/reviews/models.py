from django.db import models


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

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="title_genres"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True,
        related_name="genre_titles")

    def __str__(self):
        return f"{self.title.name} - {self.genre.name}"
