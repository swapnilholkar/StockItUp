from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'Stocks'
urlpatterns = [
    path('',views.index, name='index'), 
    path('Stocks/', views.selectStock, name='SelectStock'),
    path('<int:stock_id>/Stocks/',views.stocks, name='stocks'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('<int:stock_id>/favourite/', views.makeFavourite, name='makeFavourite'),
    path('login/', auth_views.LoginView.as_view(template_name='Stocks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Stocks/logout.html'), name='logout'),
    path('feedback/',views.feedback, name='feedback'),
    path('<int:stock_id>/results/', views.results, name='results'),

]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 