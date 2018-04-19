"""SSDI_Spring_2018_Team1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     url(r'^index/', TemplateView.as_view(template_name="index.html")),
# ]


from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from beton.views import post_signup, get_user, get_topics, get_betinfo, get_bet_topics_and_info, get_bet_details, place_a_bet,auth_user, validate_user
from beton.views import post_edituserdetails, post_user_betdetails
from beton.views import declare_winner, fetch_balance, dailybets


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', TemplateView.as_view(template_name="index.html")),
    url(r'^api/v1/signup/', post_signup, name='post_signup'),
    url(r'^api/v1/user/$', get_user, name='get_user'),
    url(r'^api/v1/topic/$', get_topics, name='get_topics'),
    url(r'^api/v1/betinfo/$', get_betinfo, name='get_betinfo'),
    url(r'^api/v1/topicsandinfo/$', get_bet_topics_and_info, name='get_bet_topics_and_info'),

    url(r'^api/v1/edituserdetails/', post_edituserdetails, name='post_edituserdetails'),
    url(r'^api/v1/userbetdetails/', post_user_betdetails, name='post_betdetails'),

    url(r'^api/v1/auth/', auth_user, name='auth_user'),
    url(r'^api/v1/validuser/', validate_user, name='validate_user'),
    url(r'^api/v1/betdetails/$', get_bet_details, name='get_bet_details'),
    url(r'^api/v1/placebet/$', place_a_bet, name='place_a_bet'),

    url(r'^api/v1/declarewinner/$', declare_winner, name='declare_winner'),
    url(r'^api/v1/fetch_balance/$', fetch_balance, name='fetch_balance'),
    url(r'^api/v1/dailybets/$', dailybets, name='dailybets'),


]

