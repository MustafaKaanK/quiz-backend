from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator


class Option(models.Model):
    description = models.CharField(max_length=100, default='')
    number_order = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    result_factor_list = ArrayField(models.PositiveIntegerField(validators=[MinValueValidator(1)]), default=list, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"No: {self.number_order} | Result Factor Size: {len(self.result_factor_list)} | Description : {self.description}"

class Question(models.Model):
    description = models.CharField(max_length=100, default='')
    number_order = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    options = models.ManyToManyField(Option, related_name='options', blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"No: {self.number_order} | Description : {self.description}"
    
class Result(models.Model):
    description = models.CharField(max_length=1000, default='')
    # TODO(MBM): Add variable for transfering images. 
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"Description : {self.description}"
    
class Quiz(models.Model):
    description = models.CharField(max_length=100, default='')
    number_of_questions = models.PositiveIntegerField(default=0)
    questions = models.ManyToManyField(Question, related_name='questions', blank=True)
    results = models.ManyToManyField(Result, related_name='results', blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"Description : {self.description}"
    
class Submission(models.Model):
    quiz_id = models.IntegerField(default=-1)
    selected_options_ids = ArrayField(models.PositiveIntegerField(validators=[MinValueValidator(1)]), default=list, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"Quiz: {self.quiz_id} | Created Date: {self.created_date}"