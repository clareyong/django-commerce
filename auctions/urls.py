from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("detail/<int:item_id>", views.detail, name="detail"),
    path("delete/<int:item_id>", views.delete, name="delete"),
    path("edit/<int:item_id>", views.edit, name="edit"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("inventory", views.inventory, name="inventory"),
    path("close/<int:item_id>", views.close, name="close"),
    path("comment/<int:item_id>", views.comment, name="comment"),
]
