from django.shortcuts import render
def show_main(request):
    context = {
        'name': 'Draga',
        'class': 'Dragon',
        'amount' : '1000',
        'description' : 'entitas tak dikenal ',
    }

    return render(request, "main.html", context)
# Create your views here.
