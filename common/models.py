from django.db import models

# Create your models here.

class BaseModel(models.Model):
    """
    대부분의 테이블에서 공통적으로 사용되는 컬럼에 대한 추상화 클래스
    
    - 필요한 테이블에서 models.Model 대신 해당 추상 클래스를 상속받아 사용하면 생성일자, 수정일자를 공통적으로 삽입할 수 있음.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일자")
    
    class Meta:
        abstract = True