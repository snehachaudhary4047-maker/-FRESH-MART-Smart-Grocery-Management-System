from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    prod_name = models.CharField(max_length=100)
    category  = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.prod_name


class ProductVariant(models.Model):

    UNIT_CHOICES = [
        ('ml',   'ML'),
        ('l',    'Litre'),
        ('g',    'Gram'),
        ('kg',   'KG'),
        ('pcs',  'Pieces'),
        ('pack', 'Pack'),
    ]

    product         = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    brand           = models.CharField(max_length=100, blank=True, null=True)
    variant_type    = models.CharField(max_length=100, blank=True, null=True)
    quantity        = models.DecimalField(max_digits=6, decimal_places=2)
    unit            = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock           = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    min_stock_level = models.IntegerField(default=5)
    expiry_date     = models.DateField(blank=True, null=True)
    is_expired      = models.BooleanField(default=False)

    def __str__(self):
        brand   = self.brand or ''
        variant = self.variant_type or ''
        return f"{brand} {self.product.prod_name} {variant} {self.quantity}{self.unit}".strip()

    def profit_per_unit(self):
        return self.price - self.cost_price

    def is_low_stock(self):
        return self.stock <= self.min_stock_level

    def is_out_of_stock(self):
        return self.stock == 0

    def has_expired(self):
        return self.expiry_date and self.expiry_date <= date.today()
    # keep track of expired item in inventory

    class Meta:
        verbose_name_plural = "Product Variants"

class ExpiredItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    product_name    = models.CharField(max_length=200)
    brand           = models.CharField(max_length=100, blank=True, null=True)
    variant_type    = models.CharField(max_length=100, blank=True, null=True)
    quantity        = models.DecimalField(max_digits=6, decimal_places=2)
    unit            = models.CharField(max_length=10)
    expired_stock   = models.IntegerField(default=0)
    cost_price      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_loss      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expiry_date     = models.DateField(blank=True, null=True)
    moved_on        = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - Loss ₹{self.total_loss}"

class Customer(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15,blank=True,null=True)
    email=models.EmailField(blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Sales(models.Model):
    bill_no       = models.IntegerField(default=0)
    customer      = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    variant       = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    sell_quantity = models.IntegerField()
    sale_price    = models.DecimalField(max_digits=10, decimal_places=2)
    sold_at       = models.DateTimeField(default=timezone.now)


    def revenue(self):
        return self.sell_quantity * self.sale_price

    def profit(self):
        return self.sell_quantity * self.variant.profit_per_unit()

    def cost(self):
        return self.sell_quantity * self.variant.cost_price

    def __str__(self):
        return f"Bill#{self.bill_no} {self.variant} × {self.sell_quantity}"


class Profit(models.Model):
    bill_no       = models.IntegerField()
    customer      = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date          = models.DateField(auto_now_add=True)
    created_at    = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Profit Bill#{self.bill_no} — ₹{self.total_profit}"



