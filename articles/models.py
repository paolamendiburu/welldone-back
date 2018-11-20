from datetime import datetime
from django.contrib.auth.models import  User
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import uuid as uuid_lib




class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(
        User, related_name='categories',  on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):

        return '{0}'.format(self.name)


class Article(models.Model):

    DRAFT = 'DRA'
    PUBLISHED = 'PUB'

    STATUSES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    uuid = models.UUIDField(
        db_index=True, default=uuid_lib.uuid4, editable=False)
    owner = models.ForeignKey(User,
                              related_name='articles',  on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    introduction = models.TextField()
    full_text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    media = models.FileField("video", null=True, blank=True)
    status = models.CharField(
        max_length=3, choices=STATUSES, default=PUBLISHED)
    category = models.ManyToManyField(
        Category, related_name="article_in_category")
    answer_article = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(unique=True, primary_key=True)

    class Meta:
        ordering = ('publish_date', 'created_on')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True) + \
            "-"+slugify(self.uuid)
        return super(Article, self).save(*args, **kwargs)

    def __str__(self):
        """
        Define cómo se representa un Ad como una string
        """
        return '{0} by {1}'.format(self.title, self.owner)

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})


class Follow(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    user_followed = models.ForeignKey(
        User, related_name="follows", on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} follows {1}'.format(self.owner, self.user_followed)


class Comment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} comments article {1}'.format(self.owner, self.article)


class Highlight(models.Model):

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    highlight_content = models.TextField()

    def __str__(self):
        return '{0} highlights article {1}'.format(self.owner, self.article)


class Favorite(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    article = models.ForeignKey(Article,  on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} marked {1} as favorite'.format(self.owner, self.article)
