from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    CATEGORIES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Guildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Smiths', 'Кузнецы'),
        ('Tanners', 'Кожевники'),
        ('Potionbrewers', 'Зельевары'),
        ('Spellmasters', 'Мастера заклинаний')
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_category = models.CharField(max_length=254, choices=CATEGORIES)
    post_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    post_text = models.TextField()

    def preview(self):
        prev_text = self.post_text[:125]
        return f'{prev_text}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

class SubscribedUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Reply(models.Model):
    reply_text = models.TextField()
    reply_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, null=True, choices=[('A', 'Принят'),
                                                                ('D', 'Отклонён')])





