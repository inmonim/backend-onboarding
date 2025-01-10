from django.db import models

from common.models import BaseModel

class Comment(BaseModel):
    
    comment_id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length=1024, null=False)
    is_deleted = models.SmallIntegerField(default=0, null=False)
    
    article = models.ForeignKey('articles.Article',
                                on_delete=models.CASCADE,
                                related_name='comments',
                                null=False
                                )
    author = models.ForeignKey('users.User',
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='comments')
    
    class Meta:
        db_table = "comments"