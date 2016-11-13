from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    def get_absolute_url(self):
        return reverse('superlist:view_list', args=[self.id])

class Item(models.Model):
    text = models.CharField(default='', blank=False, max_length=200)
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        # not work in mysql
        unique_together = ('list', 'text')
        ordering = ('id',)

    def __str__(self):
        return self.text