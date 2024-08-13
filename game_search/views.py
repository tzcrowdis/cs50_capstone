from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
import json

from .models import User, TrackedGame
from .search import game_search


def index(request):

    # check if input submitted
    game_name = request.GET.get("game")
    if game_name == None:
        return render(request, "game_search/index.html")

    # call search function
    results = game_search(game_name)
    
    try:
        return render(request, "game_search/index.html", {"results": results})
    except:
        print("search not returned")
        return render(request, "game_search/index.html", {"results": results})


def tracked(request):

    # goes to page with tracked list
    tracked_list = TrackedGame.objects.filter(user=request.user).all()

    return render(request, "game_search/tracked.html", {"tracked_list": tracked_list})


def track_untrack(request):

    try:
        if request.method == "POST":
            search_data = json.loads(request.body)

            # store track data if not already stored
            if search_data['status'] == "track":
                tracked_game = TrackedGame(
                    user = request.user,
                    query = search_data['query'],
                    steam_title = search_data['steam'][0],
                    steam_price = search_data['steam'][1],
                    aband_title = search_data['abandonware'][0],
                    aband_price = search_data['abandonware'][1],
                    gog_title = search_data['gog'][0],
                    gog_price = search_data['gog'][1]
                    )
                tracked_game.save()
            # delete record if found
            elif search_data['status'] == "untrack":
                tracked_game = TrackedGame.objects.filter(user=request.user, query=search_data['query'])
                tracked_game.delete()

            return JsonResponse({"response_status": "success"})
    except:
        return JsonResponse({"response_status": "failure"})
    

def check_tracked(request):

    # checks if a search query is tracked
    # informs track button status
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            
            if TrackedGame.objects.filter(user=request.user, query=data['query']).exists():
                print("found")
                return JsonResponse({"response_status": "tracked"})
            else:
                return JsonResponse({"response_status": "untracked"})
    except:
        return JsonResponse({"response_status": "untracked"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "game_search/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "game_search/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "game_search/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "game_search/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "game_search/register.html")