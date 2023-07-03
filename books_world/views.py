from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
# from http import HttpResponse
import requests as req
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from .models import FavoriteBooks, BookReview, BookSearch
from django.db.models import Count
# Create your views here.

BASE_URL = "https://www.googleapis.com/books/v1/volumes/?q="
def index(request):
   
    # for general fiction books
    # url = "https://www.googleapis.com/books/v1/volumes?q=GeneralFiction+inpublishedDate=2022"
    url = BASE_URL+"MafiaRomance&orderBy=newest&maxResults=12"
    response = req.request("GET", url)
    fiction_books = response.json()
    items1 = fiction_books["items"]
    item_zeroth_one = items1[0]

# https://developers.google.com/books/docs/v1/using#pagination
    # for fantasy books
    url2 = BASE_URL+"FantasyRomance&orderBy=newest&maxResults=12"
    response2 = req.request("GET", url2)
    fiction_books2 = response2.json()
    items2 = fiction_books2["items"]
    item_zeroth_two = items2[0] 


    items = [items1, items2]
    item_zeroth =[item_zeroth_one, item_zeroth_two]
    titles = ["New Mafia Romance Release", "New Fantasy Release"]
    combined_items = zip(items, item_zeroth, titles)
    
    if request.user.is_authenticated:
        return render(request, "index.html", { "range" : range(1, 4), "combined_items": combined_items})

    else:
        return redirect("/login")

def search(request):

    if request.user.is_authenticated:
        if request.method =="POST":
            query = request.POST["search"]
            search = BookSearch.objects.create(guest_id=request.user, query=query)
            search.save()
            url = BASE_URL+f"{query}"
            response = req.request("GET", url)
            fiction_books = response.json()
            items = fiction_books["items"]
            return render(request, "search.html", { "items": items})
        return render(request, "search.html")
    else:
        return redirect("/login")
def loginUser(request):
    if request.method == "POST":
        if 'Username' and 'Password' in request.POST:
            username = request.POST['Username']
            password = request.POST['Password']
            print(username, password)
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect("/home")
            else:
                return render(request, "login.html")

    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect("/login")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = UserCreationForm()    
    return render(request, "signup.html", {"form": form})

def about(request):
    return render(request, "about.html")

def review(request, item_id):
    if request.method == "POST":
        resp = request.POST.get("action")
        
        if resp=="delete_review":
            # if BookReview.objects.filter(guest_id=request.user).exists():
            review_id = request.POST.get("review_id")
            print(review_id)
            try:
                # review = BookReview.objects.get(id=review_id)
                review = get_object_or_404(BookReview, id=review_id)
                if review.guest_id == request.user:
                    review.delete()
                else:
                    print("Review is not yours to delete, so back off you fucker!")    
            except ValueError:
                print(request.POST.get("review_id"))
                print("Invalid integer representation")
           
        else:
            review_input = request.POST.get("reviewInput")
            rev_books= BookReview.objects.create(guest_id=request.user, item_id=item_id, reviewInput=review_input)
            rev_books.save()

        return redirect("review", item_id=item_id)
    else:
        url = f"https://www.googleapis.com/books/v1/volumes/{item_id}"
        response = req.request("GET", url)
        if response.status_code == 200:
            item = response.json()
            reviews = BookReview.objects.filter(item_id=item_id)
            return render(request, "book_review.html", {'item': item, "reviews": reviews})
        else:
            # Handle the case when the API request fails or the item is not found
            return HttpResponse("Error retrieving book data")

def favorite(request, bookId):
    favBooks, created = FavoriteBooks.objects.get_or_create(guest_id=request.user, bookId = bookId)
    favorite_books = FavoriteBooks.objects.filter(guest_id=request.user).values_list('bookId', flat=True)

    if created:
        favBooks.save()
        # return render(request, 'book_review.html', {'favorite_books': favorite_books, 'item_id': bookId})
    else:
        favBooks.delete() 
        # return render(request, 'book_review.html', {'favorite_books': favorite_books, 'item_id': bookId})
    return redirect("favorites")


def favorites(request):
    favBooks = FavoriteBooks.objects.filter(guest_id = request.user)
    Books = []

    for favorite in favBooks:
        bookId = favorite.bookId
        resp = req.request("GET", f"https://www.googleapis.com/books/v1/volumes/{bookId}")
        resp_json = resp.json()
        Books.append(resp_json)
    return render(request, 'favorites.html', {"favBooks": Books})

def recommend(request):
    most_common_queries = BookSearch.objects.values('query').annotate(count=Count('query')).order_by('-count')[:10]

    recom_set = []

    for query in most_common_queries:
        url = BASE_URL+f"{query}"
        response = req.request("GET", url)
        fiction_books = response.json()
        items = fiction_books["items"]
        recom_set.append(items)
    return render(request, 'recommendations.html', {"recom_set": recom_set})