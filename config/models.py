from django.db import models

class test():
    name = models.CharField(verbose_name="test", max_length=15)
    
    class Meta:
        verbose_name = "test"
        verbose_name_plural = "test"
        
    def __str__(self) -> str:
        return self.name