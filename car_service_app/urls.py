from django.urls import path
from . import views

urlpatterns = [
    path("autoservisas/", views.index, name='index'),
    path("", views.home, name='home'),
    path("cars/", views.automobiliai, name='cars'),
    path("cars/<int:auto_id>", views.automobilis, name='car'),
    path("uzsakymai/", views.OrdersListView.as_view(), name="uzsakymai"),
    path("uzsakymai/<int:pk>", views.OrderDetailView.as_view(), name="uzsakymas"),
    path("uzsakymai/<int:pk>/update", views.MyOrderUpdateView.as_view(), name="update_my_order"),
    path("search/", views.search, name='search'),
    path('my_orders/', views.UserOrdersListView.as_view(), name='my_orders'),
    path('my_orders/<int:pk>', views.UserOrderDetailView.as_view(), name='my_order'),
    path('my_orders/new', views.NewOrderByUserCreateView.as_view(), name='my_create_new_order'),
    path('my_orders/<int:pk>/delete', views.OrderByUserDeleteView.as_view(), name='my-order-delete'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profile, name='profile'),

]
