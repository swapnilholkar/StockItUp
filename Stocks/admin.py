from django.contrib import admin

from .models import Question,StockDetail,Response,Feedback


admin.site.register(Question)
admin.site.register(StockDetail)
admin.site.register(Response)
admin.site.register(Feedback)

# Register your models here.
