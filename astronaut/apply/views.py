from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

# Create your views here.
class NewApplForm(forms.Form):
    name = forms.CharField(label="Name")
    height = forms.IntegerField(label="Height (in centimeters)", min_value=100, max_value=300)

def index(request):
    return render(request, "apply/index.html", context={"form": NewApplForm()})

def result(request):
    if request.method == "POST":
        form = NewApplForm(request.POST)
        context_dict = {"form": form}

        # this is the server-side validation
        if form.is_valid():
            name = form.cleaned_data["name"]
            height = form.cleaned_data["height"]

            if height > 160 and height < 190:
                result = f"Congratulations {name.capitalize()}! You have the correct height to be an astronaut."
                subheading = ""
            elif height <= 160:
                result = f"Sorry, {name.capitalize()}. Your height is below the minimum height to be an astronaut."
                subheading = "Aside: If you are not the right height to be an astronaut, that is fine! Space is dangerous anyways. But still, most people found a happy alternative job here on earth anyways. 🌱."
            else: #height >= 190
                result = f"Sorry, {name.capitalize()}. Your height is above the maximum height to be an astronaut."
                subheading = "Aside: If you are not the right height to be an astronaut, that is fine! Space is dangerous anyways. But still, most people found a happy alternative job here on earth anyways. 🌱."

            # session variable
            request.session['result'] = result
            request.session['subheading'] = subheading

            context_dict = {
                "result": request.session['result'],
                "subheading": request.session['subheading']
            }
            return render(request, "apply/result.html", context=context_dict)
        else:
            return HttpResponseRedirect(reverse("apply:index"))
    else:
        # check if application result exists
        if not ("result" in request.session and "subheading" in request.session):
            return HttpResponseRedirect(reverse("apply:index")) # if not, redirect to index

        context_dict = {
            "result": request.session['result'],
            "subheading": request.session['subheading']
        }
        return render(request, "apply/result.html", context=context_dict)