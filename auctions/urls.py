from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("detail_and_bid/<int:item_id>", views.detail_and_bid, name="detail-and-bid"),
    path("delete/<int:item_id>", views.delete, name="delete"),
    path("edit/<int:item_id>", views.edit, name="edit"),
]
