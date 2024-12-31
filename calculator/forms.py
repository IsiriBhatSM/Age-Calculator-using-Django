from django import forms
from .models import DOB
from datetime import datetime

class DOBForm(forms.ModelForm):
    class Meta:
        model = DOB
        fields = ['day', 'month', 'year']

    def clean_day(self):
        day = self.cleaned_data.get('day')
        if day is None or not (1 <= day <= 31):
            self.add_error('day', "Invalid day. Please enter a value between 1 and 31.")
        return day

    def clean_month(self):
        month = self.cleaned_data.get('month')
        if month is None or not (1 <= month <= 12):
            self.add_error('month', "Invalid month. Please enter a value between 1 and 12.")
        return month

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is None or not (1724 <= year <= 2024):
            self.add_error('year', "Invalid year. Please enter a value between 1724 and 2024.")
        return year

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if day and month and year:
            try:
                datetime(year, month, day)
               
            except ValueError:
                self.add_error(None, "Date is invalid. Please enter a valid date.")
        return cleaned_data



