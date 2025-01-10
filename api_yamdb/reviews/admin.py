from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


admin.site.empty_value_display = 'Не задано'


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0
    filter_horizontal = ('genre',)


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        TitleInline,
    )
    list_display = (
        'name',
        'slug'
    )
    search_fields = (
        'name',
        'slug'
    )
    list_display_links = (
        'name',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = (
        'name',
        'slug'
    )
    list_display_links = (
        'name',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = (
        'text',
    )
    search_fields = (
        'title__name',
        'author__username',
    )
    list_filter = (
        'title',
        'author',
        'score'
    )
    list_display_links = (
        'title',
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (
        ReviewInline,
    )
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = (
        'description',
        'category'
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'category',
    )
    list_display_links = (
        'name',
    )
    filter_horizontal = (
        'genre',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review',
        'pub_date'
    )
    search_fields = (
        'author__username',
    )
    list_filter = (
        'author',
    )
