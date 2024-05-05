from django.contrib import admin,messages
# from django.contrib.contenttypes.admin import  GenericTabularInline
from django.http.request import HttpRequest
from django.db.models.aggregates import Count
from django.urls import reverse
from .import models
from django.utils.html import format_html,urlencode
# from django.db.models import Count
# Register your models here.

#To customize the list page in the modeladmin
# admin.site.register(models.Collection)



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
     list_display = ["title","product_count"]


     @admin.display(ordering="product_count")
     # TO ADD NEW COLUMN TO LIST
     # To override the existing querryset
     def product_count(self,collection):
          # return collection.product_count
          #71
          url = (
            reverse("admin:store_product_changelist")  + "?"  
          +  
          urlencode({'collection_id':str(collection.id)}))

          return format_html("<a href='{}'>{}</a>",url,collection.product_count)
     
     def get_queryset(self, request):
          return super().get_queryset(request).annotate(
               product_count= Count("product")
          )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
     list_display = ["first_name","last_name","membership","orders"]
     list_per_page = 10
     list_editable = ["membership"]
     ordering = ["first_name","last_name"]

     search_fields = ["first_name__istartswith",'last_name__istartswith']

     @admin.display(ordering='orders_count')
     def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

     def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


# class TagInline(GenericTabularInline):
#      # model = TaggedItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
     search_fields =["title"]
     # inlines = [TagInline]
     list_display = ["title","unit_price","inventory_status","collection_title"]
     list_per_page = 10
     list_filter = ["collection","last_update"]
     list_editable = ["unit_price"]
     # To display related field
     list_select_related = ["collection"]

     # For selecting related field
     def collection_title(self,product):
          return product.collection.title
          
     @admin.display(ordering="inventory")
     def inventory_status(self,product):
          if (product.inventory) < 10:
               return "Low"
          return "Ok"

#EDITING CHILDREN USING INLINE admin.TabularInline,admin.StackedInline
class OrderItemInline(admin.TabularInline):
     autocomplete_fields = ["product"]
     model = models.OrderItem
     min_num = 1
     max_num = 10
     # extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
     autocomplete_fields = ["customer"]
     inlines= [OrderItemInline]
     list_display = ["id","placed_at","customer"]
     # list_per_page = 10
     