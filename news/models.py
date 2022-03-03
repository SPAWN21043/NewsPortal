from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext as _


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)

    def update_rating(self, up_rating):
        self.rating_user = up_rating
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name_category = models.CharField(unique=True, max_length=50, help_text=_('Category name'))
    subscr_user = models.ManyToManyField(User, related_name='subscribed_categories')

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    post_user = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_news = models.CharField(max_length=2, choices=POSITIONS, default=news)
    date_create = models.DateTimeField(auto_now_add=True)
    categ = models.ManyToManyField(Category, through="PostCategory")
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        size = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:size] + '...'

    def __str__(self):
        return f'{self.post_user}{self.date_create}{self.heading}{self.text}{self.categ}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_caty = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_post}{self.post_caty}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
