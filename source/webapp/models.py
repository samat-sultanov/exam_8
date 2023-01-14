from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

CHOICES = [('others', 'Другое'), ('fast-food', 'Фаст-фуд'), ('drinks', 'Напитки'), ('sweets', 'Сладости')]


class Product(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    category = models.CharField(max_length=30, default='others', choices=CHOICES, verbose_name='Категория')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    picture = models.ImageField(upload_to='pictures', null=True, blank=True, verbose_name='Картинка')

    class Meta:
        db_table = "products"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} - {self.category}"

    def get_avg_mark(self):
        result = self.reviews.filter(is_moderated=True).aggregate(avg=Avg("mark"))
        return result["avg"]


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='reviews',
                                verbose_name='Товар')
    text = models.TextField(max_length=1500, verbose_name='Текст отзыва')
    mark = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_moderated = models.BooleanField(verbose_name='Прошел модерацию', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        permissions = [("review_not_moderated", "Просмотр немодерированных отзывов")]

    def __str__(self):
        return f"{self.pk}: {self.author.username} - {self.product.name}"

