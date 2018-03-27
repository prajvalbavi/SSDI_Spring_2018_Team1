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
from beton.views import post_signup, get_user, get_topics, get_betinfo, get_bet_topics_and_info

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', TemplateView.as_view(template_name="index.html")),
    url(r'^api/v1/signup/', post_signup, name='post_signup'),
    url(r'^api/v1/user/$', get_user, name='get_user'),
    url(r'^api/v1/topic/$', get_topics, name='get_topics'),
    url(r'^api/v1/betinfo/$', get_betinfo, name='get_betinfo'),
    url(r'^api/v1/topicsandinfo/$', get_bet_topics_and_info, name='get_bet_topics_and_info'),

]

