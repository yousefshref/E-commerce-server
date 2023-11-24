from django.contrib import admin
from . import models
from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)
from django.db.models import Q

admin.site.register(models.Cart)
admin.site.register(models.CartItem)

"""
Auth
"""
admin.site.register(models.User)



class LandingInline(admin.TabularInline):
    model = models.Landing
    extra = 3

@admin.register(models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    inlines = [LandingInline]

"""
State
"""
admin.site.register(models.State)


"""
Category
"""
admin.site.register(models.Category)

"""
Brand
"""
admin.site.register(models.Brand)

"""
Color
"""
admin.site.register(models.Color)


"""
Product
"""
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 3

class VariantInline(admin.TabularInline):
    model = models.Variant
    extra = 3

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description',)

    list_editable = ('title',)

    search_fields = ('title',)
    
    inlines = [VariantInline, ProductImageInline]

    def save(self, req, obj):
        for o in obj:
            o.save()

    actions = [save]


# """
# Cart
# """
# class CartItemInline(admin.TabularInline):
#     model = models.CartItem
#     extra = 3


# @admin.register(models.Cart)
# class CartAdmin(admin.ModelAdmin):
#     inlines = [CartItemInline]



"""
Order
"""
class OrdertemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 3


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','name','address','state','status','total_coast','created_date',)
    list_editable = ('state','status',)
    inlines = [OrdertemInline]

    search_fields = ('user__username__icontains', 'name__icontains')

    list_filter = (
        ("created_date", DateRangeQuickSelectListFilterBuilder()),
        'status'
    )

    def pending(self, req, obj):
        for i in obj:
            i.status = 'pending'
            i.save()

    def itw(self, req, obj):
        for i in obj:
            i.status = 'in the way'
            i.save()

    def arrived(self, req, obj):
        for i in obj:
            i.status = 'arrived'
            i.save()

    def cancelled(self, req, obj):
        for i in obj:
            i.status = 'cancelled'
            i.save()

    actions = [pending, itw, arrived, cancelled]

    change_list_template = 'admin/order.html'


    def changelist_view(self, request, extra_context=None):
        orders = self.model.objects.all()

        if(request.GET.get('created_date__range__gte') and request.GET.get('created_date__range__lte')):
            orders = orders.filter(created_date__range=[request.GET.get('created_date__range__gte'), request.GET.get('created_date__range__lte')])

        if(request.GET.get('created_date__gte') and request.GET.get('created_date__lt')):
            orders = orders.filter(created_date__range=[request.GET.get('created_date__gte'), request.GET.get('created_date__lt')])

        if(request.GET.get('q')):
            orders = orders.filter(Q(user__username__icontains=request.GET.get('q')) | Q(name__icontains=request.GET.get('q')))

        if(request.GET.get('status__exact')):
            orders = orders.filter(status__icontains=request.GET.get('status__exact'))

            
        
        # total coast
        sum_total_coast = 0
        for order in orders:
            sum_total_coast += order.total_coast


        # total earning
        sum_earning = 0
        for order in orders:
            items = models.OrderItem.objects.filter(order=order.pk)
            for item in items:
                sum_earning += item.product.earning * item.quantity

        
        extra_context = {
            "sum_total_coast":sum_total_coast,
            "sum_earning":sum_earning,
        }
        return super().changelist_view(request, extra_context=extra_context)
