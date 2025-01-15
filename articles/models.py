from django.db import models

from common.models import BaseModel

class Article(BaseModel):
    
    article_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    is_public = models.SmallIntegerField(null=True)
    is_deleted = models.SmallIntegerField(null=False, default=0)
    
    author = models.ForeignKey('users.User',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='articles')
    
    category = models.ForeignKey('categories.Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='articles')
    
    class Meta:
        db_table = 'articles'