from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from library.models import Loan

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

def profile_info_by_id(request, user_id):
    user = User.objects.get(id=user_id)

    active_loans = Loan.objects.filter(user=user, returned_at__isnull=True)
    returned_loans = Loan.objects.filter(user=user, returned_at__isnull=False)

    context = {
        "user": user,
        "active_loans": active_loans,
        "returned_loans": returned_loans,
        "active_count": active_loans.count(),
    }

    return render(request, "accounts/profile_info.html", context)

def user_list(request):
    users = User.objects.all()
    return render(request, "accounts/user_list.html", {"users": users})

@login_required
def profile_info(request):
    return profile_info_by_id(request, request.user.id)