from django.contrib import admin
from .models import CarModel, Car, Order, OrderLine, Service, OrderReview, UserProfile


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 10
    readonly_fields = ('order_id',)
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'data', 'servis', 'useris')
    inlines = [OrderLineInline]


class CarAdmin(admin.ModelAdmin):
    list_display = ('customer', 'marke', 'modelis', 'valstybinis_nr', 'vin_code')
    list_filter = ('customer', 'car_model_id')
    search_fields = ('valstybinis_nr', 'vin_code')

    def marke(self, obj):
        return obj.car_model_id.marke

    def modelis(self, obj):
        return obj.car_model_id.model


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(Service)
admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(UserProfile)
