from django.db import models
from Groups.models import Village
# Create your models here.
class Application(models.Model):
    applicant=models.CharField(verbose_name="name", max_length=32)
    applyreason=models.CharField(verbose_name="reason", max_length=32)
    applyemail=models.CharField(verbose_name="email", max_length=30, blank=True)
    goal = models.ForeignKey(Village, related_name='applicants', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.applicant


