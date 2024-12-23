import csv
import os

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import MyUser


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
                    if 'category' in csv_file_path:
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
                        title = Title.objects.get(id=row['title_id'])
                        user = MyUser.objects.get(id=row['author'])
                        Review.objects.create(
                            text=row['text'],
                            author=user,
                            score=row['score'],
                            pub_date=row['pub_date'],
                            title_id=title
                        )
                    elif 'comment' in csv_file_path:
                        # Получаем объект по связке с моделью Review
                        review = Review.objects.get(id=row['review_id'])
                        Comment.objects.create(
                            text=row['text'],
                            author=row['author'],
                            pub_date=row['pub_date'],
                            review_id=review
                        )
                    else:
                        raise CommandError('Неизвестный тип файла')

                self.stdout.write(self.style.SUCCESS(
                    f'Успешно импортировано {reader.line_num} записей из {csv_file_path}'))

        except Exception as e:
            raise CommandError(f'Ошибка при импорте данных: {e}')
import csv
import os

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов в модели Category, Genre и Title'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу для импорта данных')

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join('static/data', kwargs['csv_file'])

        if not os.path.exists(csv_file_path):
            raise CommandError(f'Файл {csv_file_path} не найден.')

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if 'category' in csv_file_path:
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
                        category = Category.objects.get(id=row['category']) if row['category'] else None
                        Title.objects.update_or_create(
                            id=row['id'],
                            defaults={
                                'name': row['name'],
                                'year': row['year'],
                                'category': category
                            }
                        )
                    else:
                        raise CommandError('Неизвестный тип файла')

                self.stdout.write(self.style.SUCCESS(f'Успешно импортировано {reader.line_num} записей из {csv_file_path}'))

        except Exception as e:
            raise CommandError(f'Ошибка при импорте данных: {e}')
