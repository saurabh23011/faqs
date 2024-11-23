from django.db import models

# Create your models here.

class FAQ(models.Model):
    questions=models.TextField()
    answer=models.TextField()
    keywords=models.JSONField(blank=True,null=True)

    def __str__(self):
        return self.questions
    

