from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("news/<str:news_type>/", views.news_list, name="newsList"),
    path("news/detail/<int:news_id>/", views.news_detail, name="newsDetail"),
    path("search/", views.search, name="search"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signon/", views.signon, name="signon"),
    path("accounts/login/", views.login, name="accounts_login"),
    path("accounts/logout/", views.logout, name="accounts_logout"),
]
