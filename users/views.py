from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "users/index.html")


def login_views(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                # admin:index เป็น url ที่ Django กำหนดไว้ให้เป็นหน้า admin page
                return redirect(reverse("admin:index"))
            else:
                return render(request, "users/index.html")

        else:
            return render(
                request, "users/login.html", {"message": "Invalid credentials."}
            )
    return render(request, "users/login.html")


def logout_views(request):
    logout(request)
    context = {"message": "You're Logout"}
    return render(request, "users/login.html", context)


def register_views(request):
    if request.method == "POST":
        username = request.POST["Username"]
        password = request.POST["Password"]
        password_again = request.POST["Password again"]

        if password != password_again:
            return render(
                request,
                "users/register.html",
                {"message": "Password not match, Please try again."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "users/register.html",
                {"message": "This Username already registry, Please try again."},
            )
        User.objects.create_user(username=username, password=password)
        return render(
            request,
            "users/login.html",
            {"registry": "Register success"},
        )
    return render(request, "users/register.html")
