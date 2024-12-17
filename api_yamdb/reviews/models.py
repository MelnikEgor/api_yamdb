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
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, related_name="titles", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name
