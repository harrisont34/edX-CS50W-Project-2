from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import User, Listing, Watchlist, ListComment, Bid

class NewForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = ListComment
        fields = ['comment']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]


def index(request):

    if request.user.is_authenticated:
        
        # Create List
        watch_list = Watchlist.objects.filter(user=request.user).all()
        list = []
        for n in watch_list:
            list.append(n.item_id.id)

        return render(request, "auctions/index.html", {
            "listings": Listing.objects.exclude(active=False).all(),
            "watch_list": list,
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.exclude(active=False).all(),
        })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def listing_page(request, title):

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():

            objects = Listing.objects.filter(title=title).first()
            comment = form.cleaned_data["comment"]

            # Store in db
            db = ListComment(user=request.user, item_id=objects, comment=comment)
            db.save()

            # Display tuple readable name
            category = objects.get_category_display()
 
            return render(request, "auctions/title.html", {
                "listing": Listing.objects.get(title=title),
                "category": category,
                "form": CommentForm,
                "comment_list": ListComment.objects.filter(item_id=objects.id).all()
            })
        else:
            # Display tuple readable name
            objects = Listing.objects.get(title=title)
            category = objects.get_category_display()

 
            return render(request, "auctions/title.html", {
                "listing": Listing.objects.get(title=title),
                "category": category,
                "form": CommentForm,
                "comment_list": ListComment.objects.filter(item_id=objects.id).all()
            })
            

    else: 
        # Display tuple readable name
        objects = Listing.objects.get(title=title)
        category = objects.get_category_display()

        return render(request, "auctions/title.html", {
            "listing": Listing.objects.get(title=title),
            "category": category,
            "form": CommentForm,
            "comment_list": ListComment.objects.filter(item_id=objects.id).all()
        })


def categories(request):
    return render(request, "auctions/categories.html", {
        "listing": Listing.CATEGORY
    })

def category_list(request, category):

    # Create List
    watch_list = Watchlist.objects.filter(user=request.user).all()
    list = []
    for n in watch_list:
        list.append(n.item_id.id)
    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category).exclude(active=False).all(),
        "watch_list": list
    })

@login_required
def create(request):

    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():

            # Obtain Summitted Data
            title = form.cleaned_data["title"]
            starting_bid = form.cleaned_data["starting_bid"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            
            # Store in db
            db = Listing(title=title, starting_bid=starting_bid, description=description, 
            image=image, category=category, owner=request.user)
            db.save()

            return render(request, "auctions/title.html", {
                "listing": Listing.objects.get(title=title),
                "form": CommentForm,
            })

        else: 
            return render(request, "auctions/create.html", {
                "form": NewForm()
            })

    else:
        return render(request, "auctions/create.html", {
            "form": NewForm()
        })


@login_required
def watchlist(request):

    watch_list = Watchlist.objects.filter(user=request.user).all()
    return render(request, "auctions/watchlist.html", {
        "watch_list": watch_list
    })

@login_required
def add_watchlist(request, item_id):

    # Add to watchlist
    item_id = Listing.objects.filter(id=item_id).first()

    # Store in db
    db = Watchlist(user=request.user, item_id=item_id)
    db.save()

    # Return Watchlist page
    return render(request, "auctions/watchlist.html", {
        "watch_list": Watchlist.objects.filter(user=request.user).all()
    })

@login_required
def del_watchlist(request, item_id):

    # Remove object from Watchlist
    db = Watchlist.objects.filter(user=request.user,item_id=item_id).delete()

    # Return Watchlist page
    return render(request, "auctions/watchlist.html", {
        "watch_list": Watchlist.objects.filter(user=request.user).all()
    })

@login_required
def bid(request, title):

    if request.method == "POST":

        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            objects = Listing.objects.filter(title=title).first()

            # Determine if bid is top bid
            highest = 0
            top_bid = Bid.objects.filter(item_id=objects).all()
            for n in top_bid:
                if n.bid >= highest:
                    highest = n.bid

            if bid > objects.starting_bid and bid > highest:

                db = Bid(user=request.user, item_id=objects, bid=bid)
                db.save()

                objects = Listing.objects.get(title=title)
                category = objects.get_category_display()

                return render(request, "auctions/bid.html", {
                    "listing": objects,
                    "category": category,
                    "form": BidForm,
                    "bid_list": Bid.objects.filter(item_id=objects.id).order_by('-timestamp').all(),
                    "user": request.user
                })

            else:
                objects = Listing.objects.get(title=title)
                category = objects.get_category_display()

                return render(request, "auctions/bid.html", {
                    "listing": objects,
                    "category": category,
                    "form": BidForm,
                    "bid_list": Bid.objects.filter(item_id=objects.id).order_by('-timestamp').all(),
                    "message": "Bid must be larger than starting bid and higher than other bids!"
                })

        
    else:    
        objects = Listing.objects.get(title=title)
        category = objects.get_category_display()

        return render(request, "auctions/bid.html", {
            "listing": objects,
            "category": category,
            "form": BidForm,
            "bid_list": Bid.objects.filter(item_id=objects.id).order_by('-timestamp').all()
        })

@login_required
def close_bid(request, title):

    objects = Listing.objects.filter(title=title).first()
    category = objects.get_category_display()

    # Change to inactive
    objects.active = False
    objects.save()

    # Determine top bid
    highest = 0
    top_bid = Bid.objects.filter(item_id=objects).all()
    for n in top_bid:
        if n.bid >= highest:
            highest = n.bid
    
    # Find winner
    w = Bid.objects.filter(bid=highest).first()
    winner = w.user

    return render(request, "auctions/bid.html", {
            "listing": objects,
            "category": category,
            "bid_list": Bid.objects.filter(item_id=objects.id).order_by('-timestamp').all(),
            "winner": winner,
            "highest": highest
        })
