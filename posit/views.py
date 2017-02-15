from django.shortcuts import render


# Create your views here.
def home(request):
    title = "Welcome"

    context = {
        "title": title,
    }

    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html", {})


def meta(request):
    return render(request, "meta.html", {})
