# Use include() to add paths from the catalog application 
from django.urls import include
from django.urls import path
from . import views

app_name = 'getdb'


urlpatterns = [
	#path('', views.ConnectionView.get_db1, name='connection'),
	#path('connext/', views.LoadingView.gettingdata, name='connext/'),
    path('', views.LocationView.get_location, name=''),
]
