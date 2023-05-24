from django.db import models
from ckeditor.fields import RichTextField


class NewsToSend(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    wysiwyg_text = RichTextField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'
