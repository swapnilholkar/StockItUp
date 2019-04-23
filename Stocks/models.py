import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# stores basic stock data
class StockDetail(models.Model):
    
    stock_symbol = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    target_price = models.FloatField(max_length=200)
    company_logo = models.ImageField(default='default.png', upload_to='logos')
    favourite = models.ManyToManyField(User,related_name='favourite',blank=True)
    
    def __str__(self):
        return self.company_name
    
# stores questions
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

#    stores the responses 
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockDetail, on_delete=models.CASCADE) 
    response_text = models.CharField(max_length=201)
    response_posted = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.response_text 
        
# stores the feedback
class Feedback(models.Model):
    rate_function = models.CharField(max_length=201)
    most_function = models.CharField(max_length=201)
    improve_function = models.CharField(max_length=201)
    rate_design = models.CharField(max_length=201)
    most_design = models.CharField(max_length=201)
    improve_design = models.CharField(max_length=201)
    feedback_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.rate_design 
  

        