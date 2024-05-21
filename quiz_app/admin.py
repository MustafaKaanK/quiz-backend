from django.contrib import admin
from .models import Option, Question, Quiz, Result, Submission


admin.site.register(Option)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Quiz)
admin.site.register(Submission)