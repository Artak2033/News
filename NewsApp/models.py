from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICES = (
    ('draft', 'DRAFT'),
    ('published', 'PUBLISHED'),
)


class Category(models.Model):
    title = models.CharField('Category title', max_length=255)
    slug = models.SlugField('URL', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    additional_category = models.ManyToManyField(Category, blank=True, related_name='Additional', verbose_name='Additional_categories')
    title = models.CharField('Article title', max_length=255)
    slug = models.SlugField('URL', unique=True)
    image = models.ImageField('Photo', upload_to='NewsPhoto')
    content = RichTextUploadingField('News Content')
    status = models.CharField('Status', choices=STATUS_CHOICES, default='published', max_length=10)
    author = models.CharField('Author', default='Admin', max_length=30)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


