from django.contrib import admin
from .models import Category, Product, ProductVariant, Sales,ExpiredItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name')
    search_fields = ('name',)


class ProductVariantInline(admin.TabularInline):
    model  = ProductVariant
    extra  = 1
    fields = ('brand', 'variant_type', 'quantity', 'unit',
              'price', 'cost_price', 'stock', 'expiry_date')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('id', 'prod_name', 'category')
    search_fields = ('prod_name',)
    list_filter   = ('category',)
    inlines       = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'brand', 'variant_type',
                     'quantity', 'unit', 'price', 'cost_price',
                     'stock', 'expiry_date')
    search_fields = ('brand', 'variant_type', 'product__prod_name')
    list_filter   = ('unit', 'product__category')   # filter by unit and category


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'variant', 'sell_quantity',
                     'sale_price', 'sold_at')
    search_fields = ('variant__brand', 'variant__product__prod_name')
    list_filter   = ('sold_at',)
@admin.register(ExpiredItem)
class ExpiredItemAdmin(admin.ModelAdmin):
    list_display =('id','product_variant','product_name','brand','variant_type',
                    'quantity','unit','expired_stock','cost_price','total_loss',
                    'expiry_date','moved_on')
    search_field =('product_variant')

