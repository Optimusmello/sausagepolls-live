from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):

    Question = models.CharField(max_length=100,unique=True)
    created_by = models.ForeignKey(User,related_name='created_by',on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.Question
    
    class Meta:

        ordering = ['-created_date']

class PollOptions(models.Model):

    poll = models.ForeignKey(Poll,related_name='polloptions',on_delete=models.CASCADE)
    option1 = models.CharField(max_length=100,null=True,blank=True)
    option2 = models.CharField(max_length=100,null=True,blank=True)
    option3 = models.CharField(max_length=100,null=True,blank=True)

    option1count = models.IntegerField(default=0)
    option2count = models.IntegerField(default=0)
    option3count = models.IntegerField(default=0)

    option1photo = models.ImageField(null=True, blank=True)
    option2photo = models.ImageField(null=True,blank=True)
    option3photo = models.ImageField(null=True,blank=True)

class Voter(models.Model):

    voter = models.ForeignKey(User,related_name='voter',on_delete=models.CASCADE)
    option = models.ForeignKey(PollOptions,related_name='options',on_delete=models.CASCADE)

    class Meta:

        unique_together = ['voter','option']