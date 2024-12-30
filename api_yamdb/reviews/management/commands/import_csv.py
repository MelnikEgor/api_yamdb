# import csv
# import os

# from django.core.management.base import BaseCommand, CommandError

# from reviews.models import Category, Genre, Title, Review, Comment, TitleGenre
# # from users.models import MyUser
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class Command(BaseCommand):
#     help = 'Импорт данных из CSV файлов в модели Category, Genre и Title'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str,
#                             help='Путь к CSV файлу для импорта данных')

#     def handle(self, *args, **kwargs):
#         csv_file_path = os.path.join('static/data', kwargs['csv_file'])

#         if not os.path.exists(csv_file_path):
#             raise CommandError(f'Файл {csv_file_path} не найден.')

#         try:
#             with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#                 reader = csv.DictReader(csvfile)

#                 for row in reader:
#                     if 'genre_title' in csv_file_path:
#                         title = Title.objects.get(id=row['title_id'])
#                         genre = Genre.objects.get(id=row['genre_id'])
#                         TitleGenre.objects.update_or_create(
#                             title=title,
#                             genre=genre,
#                         )
#                     elif 'users' in csv_file_path:
#                         User.objects.update_or_create(
#                             id=row['id'],
#                             defaults={
#                                 'username': row['username'],
#                                 'email': row['email'],
#                                 'role': row.get('role', 'user'),
#                                 'bio': row.get('role', ''),
#                                 'first_name': row.get('first_name', ''),
#                                 'last_name': row.get('last_name', '')
#                             }
#                         )
#                     elif 'category' in csv_file_path:
#                         Category.objects.update_or_create(
#                             id=row['id'],
#                             defaults={
#                                 'name': row['name'],
#                                 'slug': row['slug']
#                             }
#                         )
#                     elif 'genre' in csv_file_path:
#                         Genre.objects.update_or_create(
#                             id=row['id'],
#                             defaults={
#                                 'name': row['name'],
#                                 'slug': row['slug']
#                             }
#                         )
#                     elif 'title' in csv_file_path:
#                         category = Category.objects.get(
#                             id=row['category']) if row['category'] else None
#                         Title.objects.update_or_create(
#                             id=row['id'],
#                             defaults={
#                                 'name': row['name'],
#                                 'year': row['year'],
#                                 'category': category
#                             }
#                         )
#                     elif 'review' in csv_file_path:
#                         user = User.objects.get(id=row['author'])
#                         Review.objects.create(
#                             id=row['id'],
#                             title_id=row['title_id'],
#                             text=row['text'],
#                             author=user,
#                             score=row['score'],
#                             pub_date=row['pub_date'],
#                         )
#                     elif 'comments' in csv_file_path:
#                         review = Review.objects.get(id=row['review_id'])
#                         user = User.objects.get(id=row['author'])
#                         Comment.objects.create(
#                             id=row['id'],
#                             text=row['text'],
#                             pub_date=row['pub_date'],
#                             author=user,
#                             review=review,
#                         )
#                     else:
#                         raise CommandError('Неизвестный тип файла')

#                 self.stdout.write(self.style.SUCCESS(
#                     f'Успешно импортировано {reader.line_num} записей из {csv_file_path}'))

#         except Exception as e:
#             raise CommandError(f'Ошибка при импорте данных: {e}')


import csv
import os

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Genre, Title, Review, Comment, TitleGenre
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов в модели Category, Genre и Title'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='Путь к CSV файлу для импорта данных')

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join('static/data', kwargs['csv_file'])

        if not os.path.exists(csv_file_path):
            raise CommandError(f'Файл {csv_file_path} не найден.')

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    self.process_row(csv_file_path, row)

                self.stdout.write(self.style.SUCCESS(
                    f'Успешно импортировано {reader.line_num} записей из {csv_file_path}'))

        except Exception as e:
            raise CommandError(f'Ошибка при импорте данных: {e}')

    def process_row(self, csv_file_path, row):
        if 'genre_title' in csv_file_path:
            self.import_genre_title(row)
        elif 'users' in csv_file_path:
            self.import_users(row)
        elif 'category' in csv_file_path:
            self.import_category(row)
        elif 'genre' in csv_file_path:
            self.import_genre(row)
        elif 'title' in csv_file_path:
            self.import_title(row)
        elif 'review' in csv_file_path:
            self.import_review(row)
        elif 'comment' in csv_file_path:
            self.import_comments(row)
        else:
            raise CommandError('Неизвестный тип файла')

    def import_genre_title(self, row):
        title = Title.objects.get(id=row['title_id'])
        genre = Genre.objects.get(id=row['genre_id'])
        TitleGenre.objects.update_or_create(
            title=title,
            genre=genre,
        )

    def import_users(self, row):
        User.objects.update_or_create(
            id=row['id'],
            defaults={
                'username': row['username'],
                'email': row['email'],
                'role': row.get('role', 'user'),
                'bio': row.get('bio', ''),
                'first_name': row.get('first_name', ''),
                'last_name': row.get('last_name', '')
            }
        )

    def import_category(self, row):
        Category.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'slug': row['slug']
            }
        )

    def import_genre(self, row):
        Genre.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'slug': row['slug']
            }
        )

    def import_title(self, row):
        category = Category.objects.get(
            id=row['category']) if row['category'] else None
        Title.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'year': row['year'],
                'category': category
            }
        )

    def import_review(self, row):
        user = User.objects.get(id=row['author'])
        Review.objects.create(
            id=row['id'],
            title_id=row['title_id'],
            text=row['text'],
            author=user,
            score=row['score'],
            pub_date=row['pub_date'],
        )

    def import_comments(self, row):
        review = Review.objects.get(id=row['review_id'])
        user = User.objects.get(id=row['author'])
        Comment.objects.create(
            id=row['id'],
            text=row['text'],
            pub_date=row['pub_date'],
            author=user,
            review=review,
        )
