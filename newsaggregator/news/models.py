from django.db import models

class Headline(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    link = models.TextField()
    date = models.TextField(default=None)
    source = models.URLField(null=True)
    img = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

