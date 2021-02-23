from django.contrib import admin
from secondapp.models import Student,Contact_Us,Category,register_table,add_product,cart,Order

admin.site.site_header="Zykaa"

class StudentAdmin (admin.ModelAdmin):
    list_display=["name","roll_no","email","fee"]
    search_fields=["roll_no","name"]
    list_filter=["name","email","gender"]
    list_editable=["email"]
    # fields= ["name","email","roll_no"]

class Contact_UsAdmin (admin.ModelAdmin):
    list_display=["id","name","contact_number","subject","message","added_on"]
    search_fields=["contact_number","name"]
    list_filter=["name"]
    list_editable=["contact_number"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","cat_name","description","added_on"]


admin.site.register(Student,StudentAdmin)
admin.site.register(Contact_Us,Contact_UsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(register_table)
admin.site.register(add_product)
admin.site.register(cart)
admin.site.register(Order)



