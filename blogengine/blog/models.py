from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s + '-' + str(int(time())))
    return new_slug
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150,db_index=True)
    slug = models.SlugField(max_length=150, blank=True,unique=True)
    body = models.TextField(blank=True,db_index=True)
    tags = models.ManyToManyField('Tag',blank=True,related_name='posts')
    date_pub = models.DateField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)

        super().save(*args,**kwargs)



    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        #return reverse('post_detail_url',kwargs={'slug':self.slug+'1'})
        return reverse('post_detail_url', kwargs={'slug': self.slug})

class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url',kwargs={'slug':self.slug})

    def __str__(self):
        return '{}_{}'.format(self.title,self.slug)

#for union sql kostyl fro pagination add calculable field type
class TagPostVirtual(models.Model):
    title = models.CharField(max_length=150)
    type = models.CharField(max_length=50)

    class Meta:
        db_table = "blog_virt_tag_post"

    def get_absolute_url(self):
        return reverse('TagPostVirtual',kwargs={'slug':self.slug})

    def __str__(self):
        return '{}_{}'.format(self.title, self.type)



