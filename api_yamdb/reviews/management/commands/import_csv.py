import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title, Review, Comment

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
                    if 'users' in csv_file_path:
                        User.objects.update_or_create(
                            id=row['id'],
                            defaults={
                                'username': row['username'],
                                'email': row['email'],
                                'role': row.get('role', 'user'),
                                'bio': row.get('role', ''),
                                'first_name': row.get('first_name', ''),
                                'last_name': row.get('last_name', '')
                            }
                        )
                    elif 'category' in csv_file_path:
                        Category.objects.update_or_create(
                            id=row['id'],
                            defaults={
                                'name': row['name'],
                                'slug': row['slug']
                            }
                        )
                    elif 'genre' in csv_file_path:
                        Genre.objects.update_or_create(
                            id=row['id'],
                            defaults={
                                'name': row['name'],
                                'slug': row['slug']
                            }
                        )
                    elif 'title' in csv_file_path:
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
                    elif 'review' in csv_file_path:
                        user = User.objects.get(id=row['author_id'])
                        Review.objects.create(
                            id=row['id'],
                            title_id=row['title_id'],
                            text=row['text'],
                            author=user,
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                    elif 'comments' in csv_file_path:
                        review = Review.objects.get(id=row['review_id'])
                        user = User.objects.get(id=row['author_id'])
                        Comment.objects.create(
                            id=row['id'],
                            text=row['text'],
                            pub_date=row['pub_date'],
                            author=user,
                            review=review,
                        )
                    else:
                        raise CommandError('Неизвестный тип файла')

                self.stdout.write(self.style.SUCCESS(
                    f'Успешно импортировано {reader.line_num} записей из {csv_file_path}'))

        except Exception as e:
            raise CommandError(f'Ошибка при импорте данных: {e}')
