from django.shortcuts import render
def show_main(request):
    context = {
        'name': 'Health Potion',
        'class': 'Potionn',
        'amount' : '1000',
        'description' : 'Gives you some health ',
    }

    return render(request, "main.html", context)
# Create your views here.
