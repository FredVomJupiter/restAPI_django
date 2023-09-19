from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from todo.views import CategoryViewSet, ContactViewSet, LoggedUserView, LoginView, TodoViewSet

router = routers.DefaultRouter()
router.register(r'v1/todos', TodoViewSet, basename='todos')
router.register(r'v1/categories', CategoryViewSet, basename='categories')
router.register(r'v1/contacts', ContactViewSet, basename='contacts')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('api/', include(router.urls)),
    path('api/v1/user/', LoggedUserView.as_view()),
]
