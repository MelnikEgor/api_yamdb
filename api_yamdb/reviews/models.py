from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from api_yamdb.constants import NAME_LENGTH, NAME_MAX_LENGTH, TEXT_LENGTH


User = get_user_model()


class Category(models.Model):
    name = models.CharField('Категория', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:NAME_LENGTH]


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:NAME_LENGTH]


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=NAME_MAX_LENGTH
    )
    year = models.PositiveSmallIntegerField('Год')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        # 'Жанры',
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        # 'Категория',
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:NAME_LENGTH]

    def clean(self):
        current_year = now().year
        if self.year > current_year:
            raise ValidationError({
                'year': 'Год произведения не может быть больше текущего.'
            })


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзовы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            ),
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:NAME_LENGTH]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        # verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LENGTH]
