from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.category_details, name="category_details"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]


