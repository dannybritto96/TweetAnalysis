from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',views.index,name='index'),
        url(r'^login/?$', views.twitter_login,name='login'),
        url(r'^home/$',views.home,name='home'),
        url(r'^logout/?$', views.twitter_logout,name='logout'),
        url(r'^login/authenticated/?$', views.twitter_authenticated,name='login/authenticated/'),
        url(r'^privacy_policy/$',views.privacy_policy,name='privacy_policy'),
        url(r'^terms/$',views.terms_and_conditions,name='terms'),
]
