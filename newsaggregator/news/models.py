from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    category = models.TextField(null=True)
    link = models.TextField()
    date = models.TextField(null=True) # <<-- Could be used DateField()
    source = models.URLField(null=True)
    img = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

