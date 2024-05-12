from django.db import models

class Articles(models.Model):
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=250)
    image = models.ImageField(upload_to='main/images', null= True, blank=True)

    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    info = models.TextField()

    def __str__(self):
        return "Some information"

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
