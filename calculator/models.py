from django.db import models

class DOB(models.Model):
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    age_years = models.IntegerField(null=True, blank=True)
    age_months = models.IntegerField(null=True, blank=True)
    age_days = models.IntegerField(null=True, blank=True)
    test_case_type = models.CharField(max_length=20)
    is_future_date = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"


