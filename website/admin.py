from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, Enquiry


# Register your models here.

# Start of Product
class PriceRangeFilter(admin.SimpleListFilter):
    title = 'price range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('0-50', '0 to 50'),
            ('50-100', '50 to 100'),
            ('100-200', '100 to 200'),
            ('200+', '200 and above'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-50':
            return queryset.filter(price__gte=0, price__lte=50)
        elif self.value() == '50-100':
            return queryset.filter(price__gte=50, price__lte=100)
        elif self.value() == '100-200':
            return queryset.filter(price__gte=100, price__lte=200)
        elif self.value() == '200+':
            return queryset.filter(price__gte=200)
        return queryset


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',  'image_url', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category', 'brand', PriceRangeFilter)

admin.site.register(Product, ProductAdmin)
# End of Product


# Start of OrderItem
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    can_add = False
    readonly_fields = ('id', 'user', 'product', 'quantity', 'price', 'order')

# End of OrderItem

# Start of Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'user', 'total', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ['order_id', 'user__username', 'user__email']
    inlines = [OrderItemAdmin]

    def get_readonly_fields(self, request, obj=None):
        """Make fields read-only based on condition."""
        if obj and obj.status == 'delivered' or obj and obj.status == 'canceled' or obj and obj.status == 'refunded':
            # Make all fields read-only when status is 'completed' or 'cancelled' or 'refunded'
            return [field.name for field in self.model._meta.fields]
        return []

    def has_add_permission(self, request):
        # Disable add permission
        return False

    def get_actions(self, request):
        # Disable delete action
        actions = super(OrderAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission
        return False

admin.site.register(Order, OrderAdmin)
# End of Order


# Start of Transaction
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'user', 'amount', 'created_at', 'status')
#     list_filter = ('status', 'amount', 'user')

#     def has_add_permission(self, request):
#         # Disable add permission
#         return False
    
#     def has_change_permission(self, request):
#         # Disable change permission
#         return False

#     def get_actions(self, request):
#         # Disable delete action
#         actions = super(TransactionAdmin, self).get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

#     def has_delete_permission(self, request, obj=None):
#         # Disable delete permission
#         return False
    
# admin.site.register(Transaction, TransactionAdmin)

# End of Transaction

# Start of CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'user')
    list_filter = ('user', 'product')

    # def has_add_permission(self, request):
    #     # Disable add permission
    #     return False
    
    # def has_change_permission(self, request):
    #     # Disable change permission
    #     return False

    def get_actions(self, request):
        # Disable delete action
        actions = super(CartItemAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission
        return False
    
admin.site.register(CartItem, CartItemAdmin) 


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'mobile', 'product', 'user')
    list_filter = ('product', 'user')

    def has_add_permission(self, request):
        # Disable add permission
        return False

    def get_actions(self, request):
        # Disable delete action
        actions = super(EnquiryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission
        return False
    
admin.site.register(Enquiry, EnquiryAdmin)