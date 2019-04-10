from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from django.conf import settings
from django.conf.urls.static import static
#from Stocks.views import stock_upload


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

    # path('stocksubmission/',views.stock_question_submission, name='stock_question_submission'),
    path('<int:stock_id>/results/', views.results, name='results'),
    #for csvupload
    path('upload-csv/', views.stock_upload, name='stock_upload')

]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
#certifi==2018.10.15