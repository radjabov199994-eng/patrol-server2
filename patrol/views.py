from django.shortcuts import render

def admin_dashboard(request):
    group = request.GET.get("group", "PROF")
    return render(request, "dashboard/admin_dashboard.html", {
        "group": group,
    })


def home(request):
    return render(request, "home.html")
