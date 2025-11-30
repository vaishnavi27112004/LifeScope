from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import LifestyleData
from .forms import LifestyleDataForm

# ML imports
import numpy as np
from sklearn.linear_model import LinearRegression


# -------------------------------------------------
#                 DASHBOARD VIEW
# -------------------------------------------------
@login_required
def dashboard(request):
    # Fetch all user data ordered by date
    all_data = LifestyleData.objects.filter(user=request.user).order_by('date')

    dates = [d.date.strftime('%Y-%m-%d') for d in all_data]
    steps = [d.steps for d in all_data]

    return render(request, 'tracker/dashboard.html', {
        'dates': dates,
        'steps': steps,
    })


# -------------------------------------------------
#                 ADD DATA VIEW
# -------------------------------------------------
@login_required
def add_data(request):
    if request.method == 'POST':
        form = LifestyleDataForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('tracker:dashboard')
    else:
        form = LifestyleDataForm()

    return render(request, 'tracker/add_data.html', {'form': form})


# -------------------------------------------------
#                 HISTORY VIEW
# -------------------------------------------------
@login_required
def history(request):
    records = LifestyleData.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/history.html', {'records': records})


# -------------------------------------------------
#                 PREDICT VIEW (ML)
# -------------------------------------------------
@login_required
def predict(request):
    predicted_value = None
    error_message = None

    if request.method == "POST":
        try:
            sleep = float(request.POST.get("sleep"))
            steps = float(request.POST.get("steps"))
            water = float(request.POST.get("water"))

            # Get last 30 entries
            user_data = LifestyleData.objects.filter(user=request.user).order_by('-date')[:30]

            if user_data.exists():
                avg_calories = user_data.aggregate(Avg('calories'))['calories__avg'] or 0
                adjustment = (sleep * 10) + (steps * 0.01) - (water * 5)
                predicted_value = round(avg_calories + adjustment, 2)
            else:
                predicted_value = round(
                    0.5 * sleep - 0.003 * steps - 2 * water + 70,
                    2
                )

        except ValueError:
            error_message = "Invalid input! Please enter valid numbers."

    return render(request, "tracker/predict.html", {
        "predicted": predicted_value,
        "error": error_message,
    })



"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LifestyleData
from .forms import LifestyleDataForm
from django.db.models import Avg

@login_required
def dashboard(request):
    '''today_entries = LifestyleData.objects.filter(user=request.user)[:7]  # last entries'''
    all_data = LifestyleData.objects.filter(user=request.user).order_by('date')
    # prepare simple chart data (dates & steps)
    dates = [d.date.strftime('%Y-%m-%d') for d in all_data]
    steps = [d.steps for d in all_data]
    return render(request, 'tracker/dashboard.html', {
        'dates': dates,
        'steps': steps,
    })

@login_required
def add_data(request):
    if request.method == 'POST':
        form = LifestyleDataForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('tracker:dashboard')
    else:
        form = LifestyleDataForm()
    return render(request, 'tracker/add_data.html', {'form': form})

@login_required
def history(request):
    records = LifestyleData.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/history.html', {'records': records})


@login_required
def predict(request):
    # very simple prediction: average of last 7 entries
    last7 = LifestyleData.objects.filter(user=request.user).order_by('-date')[:7]
    avg_steps = last7.aggregate(Avg('steps'))['steps__avg'] or 0
    avg_sleep = last7.aggregate(Avg('sleep_hours'))['sleep_hours__avg'] or 0
    avg_cal = last7.aggregate(Avg('calories'))['calories__avg'] or 0
    return render(request, 'tracker/predict.html', {
        'avg_steps': int(avg_steps),
        'avg_sleep': round(float(avg_sleep),2),
        'avg_cal': int(avg_cal),
    })"""
 


