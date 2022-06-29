from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Demographic)
admin.site.register(Expertise)
admin.site.register(QuestionBank)
admin.site.register(Code)
admin.site.register(Question)
admin.site.register(Evaluation)
# admin.site.register(QuestionBankEvaluation)
admin.site.register(Score)
admin.site.register(QuestionBankLevel)
admin.site.register(Time)