from django.contrib import admin
from .models import Articles, CompanyInfo, FAQ, Vacancy

class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['title', 'summary']
    search_fields = ['title', 'summary']

class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['info']
    search_fields = ['info']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'date_added']
    search_fields = ['question', 'answer']

class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'creation_date']
    search_fields = ['title', 'description']

admin.site.register(Articles, ArticlesAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Vacancy, VacancyAdmin)
