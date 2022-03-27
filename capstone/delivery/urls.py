from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order", views.order, name="order"),
    path("orderitem/<int:item_id>", views.orderitem, name="orderitem"),
    path("updateitem/<int:item_id>", views.updateitem, name="updateitem"),
    path("orders", views.orders, name="orders"),
    path("cart", views.cart, name="cart"),
    path("success", views.success, name="success")
]