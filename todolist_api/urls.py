from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from todo.views import LoginView, TodoViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('api/', include(router.urls)),
]
