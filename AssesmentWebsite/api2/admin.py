from django.contrib import admin
from .models import *
# Register your models here.
# import pprint
# from django.contrib.sessions.models import Session
# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
#     _session_data.allow_tags=True
#     list_display = ['user','session_key', '_session_data', 'expire_date']
#     readonly_fields = ['_session_data']
#     exclude = ['session_data']
#     date_hierarchy='expire_date'
# admin.site.register(Session, SessionAdmin)
from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)
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
# admin.site.register(django_session)