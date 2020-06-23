from django.db import models
from django.urls import reverse
# user model import
from django.contrib.auth.models import User

STAGES = (
    ('A', 'Applied'),
    ('C', 'Contacted Back'),
    ('R', 'Recruiter Touch'),
    ('F', '1st Interview'),
    ('S', '2nd Interview'),
    ('T', '3rd Interview'),
)

# Create your models here.
class Application(models.Model):
    status = models.CharField(
        max_length = 1,
        choices = STAGES,
        default = STAGES[0][0]
    ),
    date_applied = models.DateField(),
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100),
    description = models.TextField(),
    notes = models.TextField(),
    salary = models.CharField(max_length=20),
    interest_level = models.IntegerField(),
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} at {self.company} on {self.date_applied}"

    # class Meta:
    #     ordering = ['-date']


class Interview(models.Model):
    company_info = models.TextField(),
    preparation_text = models.TextField(),
    questions = models.TextField(),
    rating = models.IntegerField(),
    application = models.ForeignKey(Application, on_delete=models.CASCADE)


class Skills(models.Model):
    skill_name = models.CharField(max_length=100),
    user = models.ForeignKey(User, on_delete=models.CASCADE)