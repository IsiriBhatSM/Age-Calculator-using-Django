from django.shortcuts import render, redirect

from calculator.forms import DOBForm
from .models import DOB
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from datetime import datetime

def calculate_age(dob):
    today = datetime.today()
    birthdate = datetime(dob.year, dob.month, dob.day)
    
    # Calculate the difference
    delta = relativedelta(today, birthdate)
    
    # Extract years, months, and days
    age_years = delta.years
    age_months = delta.months
    age_days = delta.days
    
    return age_years, age_months, age_days

def is_leap_year(year):
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

def get_days_in_month(month, year):
    # Returns the number of days in a given month and year.
    # Handle February separately
    if month == 2:
        return 29 if is_leap_year(year) else 28
    # Handle months with 30 days
    elif month in {4, 6, 9, 11}:
        return 30
    # Handle months with 31 days
    elif month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    # Invalid month
    return 0

def determine_test_case(dob):
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day
    invalid_count = 0

    # Check for invalid months
    if dob.month < 1 or dob.month > 12:
        invalid_count += 1

    # Check for invalid days
    if dob.day < 1 or dob.day > get_days_in_month(dob.month, dob.year):
        invalid_count += 1

    # Check for invalid years
    if not (1724 <= dob.year <= 2024):
        invalid_count += 1

    # Determine test case based on invalid count
    if invalid_count > 1:
        return 'Worst Robust'
    elif invalid_count == 1:
        return 'Robust'
    elif (dob.year == current_year) and ((dob.month == current_month and dob.day > current_day) or (dob.month > current_month and dob.day <= current_day)):
        return 'Robust'
    elif (dob.year == current_year) and (dob.month > current_month or (dob.month == current_month and dob.day > current_day)):
        return 'Worst Robust'
    elif dob.year in {1724, 2024} or dob.month in {1, 12} or dob.day in {1, 31}:
        return 'Boundary'
    return 'Nominal'



def classify_invalid_test_case(errors):
    num_invalid = 0
    for field_errors in errors.values():
        for error in field_errors:
            if "Invalid day" in error or "Invalid month" in error or "Invalid year" in error:
                num_invalid += 1
    if num_invalid > 1:
        return 'Worst Robust'
    return 'Robust'

def add_dob(request):
    age_years = age_months = age_days = None
    date_is_invalid = False
    future_date = False

    if request.method == 'POST':
        form = DOBForm(request.POST)
        if form.is_valid():
            dob = form.save(commit=False)
            today = datetime.today()

            try:
                dob_date = datetime(dob.year, dob.month, dob.day)
                if dob_date > today:
                    future_date = True
                    dob.is_future_date = True
                    dob.age_years = -1  # Set a specific value
                    dob.age_months = -1
                    dob.age_days = -1
                else:
                    age_years, age_months, age_days = calculate_age(dob_date)
                    dob.age_years, dob.age_months, dob.age_days = age_years, age_months, age_days
                    dob.is_future_date = False
                dob.test_case_type = determine_test_case(dob)
                dob.save()
                form = DOBForm()  # Clear the form after saving
            except ValueError:
                date_is_invalid = True
                dob.test_case_type = determine_test_case(dob)
                dob.save()
        else:
            # Check for errors and set invalid date flag
            date_is_invalid = True
            dob = form.instance
            dob.test_case_type = classify_invalid_test_case(form.errors)  # Use the classify_invalid_test_case function
            dob.save()  # Save invalid data with test case type

    else:
        form = DOBForm()

    return render(request, 'calculator/add_dob.html', {
        'form': form,
        'age_years': age_years,
        'age_months': age_months,
        'age_days': age_days,
        'date_is_invalid': date_is_invalid,
        'future_date': future_date
    })



def test_cases(request):
    test_case_type = request.GET.get('test_case_type', 'Both')
    if test_case_type == 'Both':
        dobs = DOB.objects.all()
    else:
        dobs = DOB.objects.filter(test_case_type=test_case_type)

    return render(request, 'calculator/test_cases.html', {
        'dobs': dobs,
        'selected_filter': test_case_type
    })

def about_us(request):
    return render(request, 'calculator/about_us.html')


