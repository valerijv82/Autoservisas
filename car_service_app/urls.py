from django.urls import path
from . import views

urlpatterns = [
    path("autoservisas/", views.index, name='index'),
    path("", views.home, name='home'),
    path("cars/", views.automobiliai, name='cars'),
    path("cars/<int:auto_id>", views.automobilis, name='car'),
    path("uzsakymai/", views.UzsakymaiView.as_view(), name="uzsakymai"),
    path("uzsakymai/<int:pk>", views.UzsakymaiDetailView.as_view(), name="uzsakymas"),
    path("search/", views.search, name='search'),
    path('my_orders/', views.LoadCarsByListView.as_view(), name='my_orders'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profile, name='profile'),

]
