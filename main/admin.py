from django.contrib import admin
from .models import Articles, CompanyInfo, FAQ, Vacancy

admin.site.register(Articles)
admin.site.register(CompanyInfo)
admin.site.register(FAQ)
admin.site.register(Vacancy)
