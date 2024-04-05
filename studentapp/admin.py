from django.contrib import admin
from studentapp.models import student
from studentapp.models import Cart
# Register your models here.
#admin.site.register(student)

class studentAdmin(admin.ModelAdmin):
    list_display=['id','name','branch','percent']
    list_filter=['branch']

class cartAdmin(admin.ModelAdmin):
    list_display=['id','sid','uid','quantity']

admin.site.register(student,studentAdmin)
admin.site.register(Cart,cartAdmin)
