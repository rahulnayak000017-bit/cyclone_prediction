from django.shortcuts import render, redirect

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # simple hardcoded login (you can later connect DB users)
        if username == "admin" and password == "1234":
            request.session['user'] = username
            return redirect('predictor:predict')
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})