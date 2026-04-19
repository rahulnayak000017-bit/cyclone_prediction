from django.shortcuts import render, redirect
import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "predictor/models/random_forest_model.joblib")
scaler_path = os.path.join(BASE_DIR, "predictor/models/scaler.joblib")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "1234":
            request.session["user"] = username
            return redirect("predict")
        else:
            error = "Invalid username or password"

    return render(request, "predictor/login.html", {"error": error})


def predict_view(request):

    if "user" not in request.session:
        return redirect("login")

    result = None

    if request.method == "POST":
        try:
            data = [
                float(request.POST.get("f1")),
                float(request.POST.get("f2")),
                float(request.POST.get("f3")),
            ]

            data = scaler.transform([data])
            prediction = model.predict(data)[0]

            result = "Cyclone Risk" if prediction == 1 else "No Cyclone Risk"

        except:
            result = "Invalid input"

    return render(request, "predictor/form.html", {"result": result})