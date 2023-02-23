from django.urls import path
from django.contrib import admin
from .views import SearchView, AddSourceView, DeleteSourceView, GetAllSourcesView, GetSourceView, Top100View

urlpatterns = [
    # Api reference
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search'),
    path('top_100/', Top100View.as_view(), name='search_100'),
    # ADD/DELETE/GET source
    path('add_source/', AddSourceView.as_view(), name='add_source'),
    path('delete_source/', DeleteSourceView.as_view(), name='delete_source'),
    path('get_source/', GetSourceView.as_view(), name='get_source'),
    # Get all sources
    path('sources_list/', GetAllSourcesView.as_view(), name='get_sources'),
]
