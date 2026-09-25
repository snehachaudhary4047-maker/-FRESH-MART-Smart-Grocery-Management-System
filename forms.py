from django import forms
from store.models import Category, Product, ProductVariant, Sales,Customer
from django.forms import formset_factory
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Enter category name(snacks,beverages,etc....)',
            }),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['prod_name','category']
        widgets = {
            'prod_name': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Enter product(chips,beverages,etc....)',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model=ProductVariant
        fields=[
            'product','brand','variant_type','quantity','unit','price',
            'cost_price','stock','min_stock_level','expiry_date']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
            }),
            'brand': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'e.g. Amul, Lays, Haldiram',
            }),
            'variant_type': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'e.g. Full Cream, Magic Masala',
            }),
            'quantity': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'e.g. 500, 1, 26',
            }),
            'unit': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Selling price e.g. 55',
            }),
            'cost_price': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Buying price e.g. 40',
            }),
            'stock': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Current stock e.g. 100',
            }),
            'min_stock_level': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Alert below this e.g. 5',
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date',
            }),
        }
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer

        fields=['name','phone','email','address']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer name'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address (optional)'}),
        }


class SalesForm(forms.ModelForm):
    class Meta:

        model=Sales

        fields=['variant','sell_quantity','sale_price']
        widgets = {
            'variant': forms.Select(attrs={
                'class': 'form-control',
            }),
            'sell_quantity': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'How many sold e.g. 5',
            }),
            'sale_price': forms.NumberInput(attrs={
                'class':       'form-control',
                'placeholder': 'Price sold at e.g. 55',
            }),
        }

class SaleItemForm(forms.Form):

    variant       = forms.ModelChoiceField(
        queryset  = ProductVariant.objects.all(),
        widget    = forms.Select(attrs={'class': 'form-control variant-select'})
    )
    sell_quantity = forms.IntegerField(
        min_value = 1,
        widget    = forms.NumberInput(attrs={'class': 'form-control qty-input', 'value': '1'})
    )
    sale_price    = forms.DecimalField(
        max_digits    = 10,
        decimal_places = 2,
        widget        = forms.NumberInput(attrs={'class': 'form-control price-input'})
    )


SaleItemFormSet = formset_factory(SaleItemForm, extra=1)

class BillHeaderForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset  = Customer.objects.all(),
        required  = False,
        widget    = forms.Select(attrs={'class': 'form-control'})
    )
    discount = forms.DecimalField(
        max_digits    = 10,
        decimal_places = 2,
        initial       = 0,
        required      = False,
        widget        = forms.NumberInput(attrs={'class': 'form-control', 'value': '0'})
    )









