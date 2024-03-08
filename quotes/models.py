from django.db import models


class Quote(models.Model):
    _id = models.CharField(max_length=200, unique=True, verbose_name="Quote Id")
    author = models.CharField(max_length=200, verbose_name="Author")
    content = models.TextField(verbose_name="Content")
    tags = models.CharField(max_length=250, verbose_name="Tags")
    authorSlug = models.SlugField(max_length=250, verbose_name="Author Slug")
    length = models.IntegerField(verbose_name="Length")
    dateAdded = models.DateField(verbose_name="Date Added")
    dateModified = models.DateField(verbose_name="Date Modified")

    def __str__(self):
        return self.author
