from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='homepage'),
path('about/',views.about,name='about'),
path('contact/',views.contact,name='contact us'),
path('tracker/',views.tracker,name='tracker'),
path('search/',views.search,name='Search'),
path('product/<int:id>',views.product,name='product view'),
path('checkout/',views.checkout,name='checkout'),
path('handlerequest/',views.handlerequest,name='handlerequest'),

]