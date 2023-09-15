from django.contrib import admin
from todo.models import Todo, Category, Priority, Subtask, Contact

# Register your models here.
admin.site.register(Todo)
admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(Subtask)
admin.site.register(Contact)