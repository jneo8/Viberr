from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    def get_absolute_url(self):
        return reverse('superlist:view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default='', blank=False)
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)