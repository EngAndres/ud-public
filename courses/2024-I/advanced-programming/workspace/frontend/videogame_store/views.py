from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contact.html')

def videogames_list(request):
    videogames_list = [
        {
            "name": "CoD",
            "price": "150.000 COP",
            "description": "Militia first-person videogame",
            "image": "images/CoD.jpeg"
        },
        {
            "name": "CupHead",
            "price": "90.000 COP",
            "description": "Two sinblings sell their souls to the devil",
            "image": "images/CupHead.png"
        }
    ]
    return render(request, 'videogames_list.html', {"videogames": videogames_list})
