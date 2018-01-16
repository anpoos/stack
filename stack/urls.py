from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'stack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/', views.login, name = 'login'),
    url(r'^home/', views.home, name = 'home'),
    url(r'^create_issue/',views.createIssue, name = 'createIssue'),
    url(r'^view_issue/(?P<id>[0-9]+)',views.viewIssue, name = 'viewIssue'),
    url(r'^view_issue_solution/(?P<id>[0-9]+)', views.viewSolution, name = "viewSolution"),
]
