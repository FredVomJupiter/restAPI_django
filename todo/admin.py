from django.contrib import admin
from todo.models import Priority, Todo, Category, Subtask, Contact

# Register your models here.
admin.site.register(Todo)
admin.site.register(Category)
admin.site.register(Subtask)
admin.site.register(Contact)
admin.site.register(Priority)