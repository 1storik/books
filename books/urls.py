from django.contrib import admin

from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, auth, UserBookRelationView

from debug_toolbar.toolbar import debug_toolbar_urls

router = SimpleRouter()

router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', auth),
    re_path('', include('social_django.urls', namespace='social'))
] + debug_toolbar_urls()


urlpatterns += router.urls
