from django.db import models

from common.models import BaseModel


class Category(BaseModel):
    
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50, null=False)
    is_public = models.SmallIntegerField(default=1, null=False)
    
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children'
                               )
    create_user = models.ForeignKey('Users.user',
                                    on_delete=models.DO_NOTHING,
                                    null=True,
                                    blank=True,
                                    related_name='created_category'
                                    )
    
    
class Article(BaseModel):
    
    article_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    is_public = models.SmallIntegerField(null=False, default=1)
    is_deleted = models.SmallIntegerField(null=False, default=0)
    
    category = models.ForeignKey(Category, null=True, related_name='articles')