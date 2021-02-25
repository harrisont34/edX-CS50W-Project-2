from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("close_bid/<str:title>", views.close_bid, name="close_bid"),
    path("add_watchlist/<int:item_id>", views.add_watchlist, name = "add_watchlist"),
    path("del_watchlist/<int:item_id>", views.del_watchlist, name = "del_watchlist"),
    path("categories/<str:category>", views.category_list, name="category_list"),
    path("<str:title>", views.listing_page, name="listing_page")
]
