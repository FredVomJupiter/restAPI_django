from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from todo.views import CategoryViewSet, ContactViewSet, LoggedUserView, LoginView, LogoutView, RegisterView, SubtaskViewSet, TodoViewSet, VerifyView
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'v1/todos', TodoViewSet, basename='todos')
router.register(r'v1/categories', CategoryViewSet, basename='categories')
router.register(r'v1/contacts', ContactViewSet, basename='contacts')
router.register(r'v1/subtasks', SubtaskViewSet, basename='subtasks')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api/', include(router.urls)),
    path('api/v1/user/', LoggedUserView.as_view()),
    path('register-account/', RegisterView.as_view()),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('verify/<str:token>/', VerifyView.as_view(), name='verify_email'),
]