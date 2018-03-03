from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'stack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/', views.login, name = 'login'),
    url(r'^sign_up/',views.signUp, name = 'signUp'),
    url(r'^logout/', views.logout, name = 'logout'),
    url(r'^$', views.home, name = 'home'),
    url(r'^create_issue/',views.create, name = 'create'),
    url(r'^view_issue/(?P<id>[0-9]+)',views.viewIssue, name = 'viewIssue'),
    url(r'^view_issue_solution/(?P<id>[0-9]+)', views.setSolution, name = "setSolution"),
    url(r'^edit/',views.edit, name = 'edit'),
    url(r'^edit_issue/(?P<id>[0-9]+)',views.editIssue, name = 'editIssue'),



    #url(r'^home_search_result',views.home, name = "home"),
    #url(r'^home_search_result',views.searchResult, name = "searchResult"),
    #url(r'^home_search_result',views.searchResult, name = "searchResult"),
]