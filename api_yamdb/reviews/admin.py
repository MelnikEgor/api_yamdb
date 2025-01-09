from django.contrib import admin

from .models import Category, Comment, Review, Genre, Title


admin.site.empty_value_display = 'Не задано'


class TitleInline(admin.TabularInline):
    model = Title
    extra = 0


class ReviewInline(admin.StackedInline):
    model = Review
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
    # list_editable = (
    #     'is_published',
    # )
    # search_fields = (
    #     'title',
    # )
    # list_filter = (
    #     'is_published',
    # )
    # list_display_links = (
    #     'title',
    # )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # inlines = (
    #     PostInline,
    # )
    list_display = (
        'name',
        'slug'
    )
    # list_editable = (
    #     'is_published',
    # )
    # search_fields = (
    #     'title',
    # )
    # list_filter = (
    #     'is_published',
    # )
    # list_display_links = (
    #     'title',
    # )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    # list_editable = (
    #     'is_published',
    # )
    # search_fields = (
    #     'name',
    # )
    # list_filter = (
    #     'is_published',
    # )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (
        ReviewInline,
    )
    list_display = (
        'name',
        'year',
        'description',
        # 'genre',
        'category',
    )
    # list_editable = (
    #     'pub_date',
    #     'author',
    #     'location',
    #     'is_published',
    #     'category'
    # )
    # search_fields = (
    #     'title',
    # )
    # list_filter = (
    #     'category',
    #     'pub_date',
    #     'location',
    #     'author',
    # )
    # list_display_links = (
    #     'title',
    # )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review',
        'pub_date'
    )
    # list_editable = (
    #     'author',
    # )
    # search_fields = (
    #     'author__username',
    # )
    # list_filter = (
    #     'author',
    # )
