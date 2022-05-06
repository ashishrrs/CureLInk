from django.db import models

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.email_id


class Article(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    hours = models.IntegerField()
    minutes = models.IntegerField()
    published = models.BooleanField()
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
