from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Product, ProductVariant, Sales,Customer,Profit,ExpiredItem
from .forms import CategoryForm, ProductForm, ProductVariantForm, SalesForm,CustomerForm,SaleItemForm,BillHeaderForm,SaleItemFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login,logout
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum,F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io,json,time
import base64
from django.db.models.functions import TruncMonth

# login and logout credential
class LoginView(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('store:home')
        return render(request, 'store/login.html')

    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            return render(request,'store/login.html',{
                'wrong credential!!!!':'redirect to login page'
                })

class LogoutView(View):

    def get(self, request):

        logout(request)
        return redirect('store:login')
# home view credential

class HomeView(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self,request):
        categories=Category.objects.all()
        return render(request, 'store/home.html', {'categories': categories})
 #category detail view

from django.db.models import Q

class CategoryDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category)

        strval = request.GET.get('search', False)

        if strval:
            # search in brand OR variant_type OR product name
            query = Q(brand__icontains=strval)
            query.add(Q(variant_type__icontains=strval), Q.OR)
            query.add(Q(product__prod_name__icontains=strval), Q.OR)
            variants = ProductVariant.objects.filter(
                query,
                product__category=category
            ).select_related('product').distinct()
        else:
            variants = ProductVariant.objects.filter(
                product__category=category
            ).select_related('product')

        return render(request, 'store/category_detail.html', {
            'category': category,
            'products': products,
            'variants': variants,
            'search':   strval,
        })


#category add view

class CategoryAddView(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self,request):

        form=CategoryForm()
        return render(request,'store/category_form.html',{'form':form,'action':'add'})

    def post(self,request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:home')
        return render(request,'store/category_form.html',{'form':form,'action':'add'})

class CategoryUpdateView(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        form=CategoryForm(instance=category)
        return render(request,'store/category_form.html',{'form':form,'action':'update'})

    def post(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('store:home')
        return render(request,'store/category_form.html',{'form':form,'action':'update'})

class CategoryDeleteView(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self ,request,pk):
        category=get_object_or_404(Category,pk=pk)
        return render(request,'store/form_delete.html',{
            'object': category,
            'name':   category.name,
            'type':   'Category',
            'cancel_url': 'store:home',
            })


    def post(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        category.delete()
        return redirect('store:home')

# product add view
class ProductAddView(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self ,request):
        form = ProductForm()
        return render(request,'store/product_form.html',{'form':form,'action':'add'})
    def post(self ,request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:home')
        return render(request,'store/product_form.html',{'form':form,'action':'add'})

class ProductUpdateView(LoginRequiredMixin,View):
    login_url='/login/'
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        form=ProductForm(instance=product)
        return render(request,'store/product_form.html',{'form':form,'action':'update'})

    def post(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        form=ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('store:home')
        return render(request,'store/product_form.html',{'form':form,'action':'update'})

class ProductDeleteView(LoginRequiredMixin,View):
    login_url='/login/'
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        return render(request,'store/form_delete.html',{
            'object': product,
            'name':   product.prod_name,
            'type':   'Product',
            'cancel_url': 'store:home',
            })

    def post(self,request,pk):

        product=get_object_or_404(Product,pk=pk)
        product.delete()
        return redirect('store:home')

class VariantAddView(LoginRequiredMixin,View):

    login_url='/login/'

    def get(self,request):
        form = ProductVariantForm()
        return render(request,'store/variant_form.html', {'form':form,'action':'add'})

    def post(self,request):
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:home')
        return render(request,'store/variant_form.html', {'form':form,'action':'add'})

class VariantUpdateView(LoginRequiredMixin,View):
    login_url='/login/'
    def get(self,request,pk):
        variant=get_object_or_404(ProductVariant,pk=pk)
        form=ProductVariantForm(instance=variant)
        return render(request,'store/variant_form.html',{'form':form,'action':'update'})

    def post(self,request,pk):
        variant=get_object_or_404(ProductVariant,pk=pk)
        form=ProductVariantForm(request.POST,instance=variant)
        if form.is_valid():
            form.save()
            return redirect('store:home')
        return render(request,'store/variant_form.html',{'form':form,'action':'update'})

class VariantDeleteView(LoginRequiredMixin,View):
    login_url='/login/'
    def get(self,request,pk):

        variant=get_object_or_404(ProductVariant,pk=pk)
        return render(request,'store/form_delete.html',{
            'object': variant,
            'name':   str(variant),
            'type':   'Product Variant',
            'cancel_url': 'store:home',
            })

    def post(self,request,pk):
        variant=get_object_or_404(ProductVariant,pk=pk)
        variant.delete()
        return redirect('store:home')


class SalesListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # ── Sales ──
        sales         = Sales.objects.all().order_by('-sold_at')
        actual_revenue = sum(s.revenue() for s in sales)
        total_cost    = sum(s.cost()    for s in sales)
        total_profit  = sum(s.profit()  for s in sales)
        return render(request, 'store/sales_list.html', {

            'sales':           sales,
            'actual_revenue':  actual_revenue,
            'total_cost':      total_cost,
            'total_profit':    total_profit,

        })

class SalesAddView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = SalesForm()
        return render(request, 'store/sales_form.html', {'form': form, 'action': 'Add'})

    def post(self, request):
        form = SalesForm(request.POST)
        if form.is_valid():
            sale          = form.save(commit=False)

            sale.variant.stock -= sale.sell_quantity
            sale.variant.save()

            sale.save()
            return redirect('store:bill', pk=sale.pk)
        return render(request, 'store/sales_form.html', {'form': form, 'action': 'Add'})

class SalesUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        sale = get_object_or_404(Sales, pk=pk)
        form     = SalesForm(instance=sale)
        return render(request, 'store/sales_form.html', {
            'form':     form,
            'action':   'Update',
            'sale':      sale,
        })

    def post(self, request, pk):
        sale = get_object_or_404(Sales, pk=pk)
        old_qty=sale.sell_quantitiy
        form     = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            updated_sale = form.save(commit=False)
            new_qty      = updated_sale.sell_quantity
            diff = new_qty - old_qty
            updated_sale.variant.stock -= diff
            updated_sale.variant.save()

            updated_sale.save()
            return redirect('store:sales_list')

        return render(request, 'store/sales_form.html', {
            'form':   form,
            'action': 'Update',
            'sale':   sale,
        })

class SalesDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        sale = get_object_or_404(Sales, pk=pk)
        return render(request, 'store/form_delete.html', {
            'name': str(sale),
            'type': 'Sale',
        })

    def post(self, request, pk):
        get_object_or_404(Sales, pk=pk).delete()
        return redirect('store:sales_list')



class CustomerListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        customers = Customer.objects.all().order_by('-created_at')
        return render(request, 'store/customer_list.html', {
            'customers': customers,
        })


class CustomerAddView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = CustomerForm()
        return render(request, 'store/customer_form.html', {
            'form':   form,
            'action': 'Add',
        })

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:customer_list')
        return render(request, 'store/customer_form.html', {
            'form':   form,
            'action': 'Add',
        })

class CustomerUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form     = CustomerForm(instance=customer)
        return render(request, 'store/customer_form.html', {
            'form':     form,
            'action':   'Update',
            'customer': customer,
        })

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form     = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('store:customer_list')
        return render(request, 'store/customer_form.html', {
            'form':     form,
            'action':   'Update',
            'customer': customer,
        })


class CustomerDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'store/form_delete.html', {
            'name':       customer.name,
            'type':       'Customer',
            'cancel_url': 'store:customer_list',
        })

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return redirect('store:customer_list')

class BillCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        header_form = BillHeaderForm()
        formset     = SaleItemFormSet()
        return render(request, 'store/bill_create.html', {
            'header_form': header_form,
            'formset':     formset,
        })

    def post(self, request):
        header_form = BillHeaderForm(request.POST)
        formset     = SaleItemFormSet(request.POST)

        if header_form.is_valid() and formset.is_valid():
            customer = header_form.cleaned_data.get('customer')
            discount = header_form.cleaned_data.get('discount') or 0

            last_bill = Sales.objects.order_by('-bill_no').first()
            bill_no   = (last_bill.bill_no + 1) if last_bill else 1

            total_revenue = 0
            total_cost    = 0

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    variant       = form.cleaned_data['variant']
                    sell_quantity = form.cleaned_data['sell_quantity']
                    sale_price    = form.cleaned_data['sale_price']


                    Sales.objects.create(
                        bill_no       = bill_no,
                        customer      = customer,
                        variant       = variant,
                        sell_quantity = sell_quantity,
                        sale_price    = sale_price,
                    )


                    variant.stock -= sell_quantity
                    variant.save()

                    total_revenue += sell_quantity * sale_price
                    total_cost    += sell_quantity * variant.cost_price

            amount_to_pay  =  total_revenue-discount

            Profit.objects.create(
                bill_no       = bill_no,
                customer      = customer,
                total_revenue = total_revenue,
                total_cost    = total_cost,
                discount      = discount,
                total_profit  = total_revenue - total_cost - discount,
                amount_to_pay = amount_to_pay,
            )

            return redirect('store:bill_print', bill_no=bill_no)

        return render(request, 'store/bill_create.html', {
            'header_form': header_form,
            'formset':     formset,
        })


class BillPrintView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, bill_no):
        sales    = Sales.objects.filter(bill_no=bill_no)
        profit   = Profit.objects.filter(bill_no=bill_no).first()
        customer = sales.first().customer if sales.exists() else None
        return render(request, 'store/bill_print.html', {
            'sales':    sales,
            'profit':   profit,
            'customer': customer,
            'bill_no':  bill_no,

        })


class ProfitView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        profits         = Profit.objects.all().order_by('-created_at')
        for profit in profits:
            profit.amount_to_pay = profit.total_revenue - (profit.discount or 0)
            profit.total_revenue -=(profit.discount or 0)
        p_total_revenue = sum(p.total_revenue for p in profits)
        p_total_cost    = sum(p.total_cost    for p in profits)
        p_total_profit = sum(p.total_profit for p in profits)
        return render(request, 'store/profit.html', {
            'profits':         profits,
            'p_total_revenue': p_total_revenue,
            'p_total_cost':    p_total_cost,
            'p_total_profit': p_total_profit,
        })
class ProfitDelete(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, pk):
        profit = get_object_or_404(Profit, pk=pk)
        return render(request, 'store/form_delete.html', {
            'name': str(profit),
            'type': 'Profit',
        })

    def post(self, request, pk):
        get_object_or_404(Profit, pk=pk).delete()
        return redirect('store:profit')

class ProfitTotalDelete(LoginRequiredMixin, View):
    login_url='/login/'

    def get(self, request):
        return render(request, 'store/form_delete.html', {
            'name': 'TOTAL PROFIT',
            'type': 'Profit',
        })
    def post(self, request):
        Profit.objects.all().delete()
        return redirect('store:profit')
class ChatBotView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        return render(request, 'store/chatbot.html')

    def post(self, request):
        try:
            data = json.loads(request.body or "{}")
            message = data.get('message', '').lower().strip()

            if not message:
                return JsonResponse({'reply': 'Please enter a message.'}, status=400)

            variants = ProductVariant.objects.select_related(
                'product', 'product__category'
            ).all()

            # Low stock
            if "low stock" in message:
                low_items = [v for v in variants if v.stock <= v.min_stock_level]
                if not low_items:
                    return JsonResponse({'reply': 'No low stock items right now.'})

                reply = "Low Stock Items:\n"
                for v in low_items:
                    reply += f"- {v.product.prod_name} ({v.quantity}{v.unit}) → Stock: {v.stock}\n"
                return JsonResponse({'reply': reply})

            # Out of stock
            elif "out of stock" in message:
                out_items = [v for v in variants if v.stock == 0]
                if not out_items:
                    return JsonResponse({'reply': 'ITEMS ARE SUFFICIENT'})

                reply = "Out of Stock Items:\n"
                for v in out_items:
                    reply += f"- {v.product.prod_name} ({v.quantity}{v.unit})\n"
                return JsonResponse({'reply': reply})

            # Expiring soon
            elif "expiring" in message or "expiry" in message:
                soon = date.today() + timedelta(days=7)
                exp_items = [v for v in variants if v.expiry_date and v.expiry_date <= soon]

                if not exp_items:
                    return JsonResponse({'reply': 'No products expiring in the next 7 days.'})

                reply = "Products expiring soon:\n"
                for v in exp_items:
                    reply += f"- {v.product.prod_name} → Expiry: {v.expiry_date}\n"
                return JsonResponse({'reply': reply})

            # Price query
            elif "price" in message:
                for v in variants:
                    if v.product.prod_name.lower() in message:
                        return JsonResponse({
                            'reply': f"{v.product.prod_name} price is ₹{v.price} for {v.quantity}{v.unit}."
                        })
                return JsonResponse({'reply': 'Please mention the product name for price.'})

            # General fallback
            else:
                return JsonResponse({
                    'reply': 'You can ask: low stock items, out of stock items, expiring products, or product price.'
                })

        except Exception as e:
            print("CHATBOT ERROR:", str(e))
            return JsonResponse({'reply': f'Backend error: {str(e)}'}, status=500)

class ExpiryTracker:
    @staticmethod
    def move_expired_items():
        today = date.today()

        expired_variants = ProductVariant.objects.filter(
            expiry_date__isnull=False,
            expiry_date__lte=today,
            is_expired=False
        )

        for item in expired_variants:
            expired_stock = item.stock
            total_loss = Decimal(expired_stock) * item.cost_price

            ExpiredItem.objects.create(
                product_variant=item,
                product_name=item.product.prod_name,
                brand=item.brand,
                variant_type=item.variant_type,
                quantity=item.quantity,
                unit=item.unit,
                expired_stock=expired_stock,
                cost_price=item.cost_price,
                total_loss=total_loss,
                expiry_date=item.expiry_date
            )

            item.is_expired = True
            item.stock = 0
            item.save()
    @staticmethod
    def get_total_loss():
        total = ExpiredItem.objects.aggregate(total=Sum('total_loss'))['total']
        return total or 0

class ExpiredCornerView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # First move expired items automatically
        ExpiryTracker.move_expired_items()

        expired_items = ExpiredItem.objects.all().order_by('-moved_on')
        total_loss = ExpiryTracker.get_total_loss()

        return render(request, 'store/expiredcorner.html', {
            'expired_items': expired_items,
            'total_loss': total_loss
        })
class ProjectContributorView(LoginRequiredMixin, View):
    login_url='/login/'
    def get(self,request):
        return render(request,'store/contributor.html')

def generate_chart(fig):
    """Convert matplotlib figure to base64 image for HTML"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',
                dpi=130, facecolor='#f8faff')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_base64

class MatplotlibChartView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):

        data = Sales.objects.annotate(
            month=TruncMonth('sold_at')
        ).values(
            'month',
            'variant__product__prod_name',
            'variant__brand',
        ).annotate(
            total_profit=Sum(
                F('sell_quantity') * F('sale_price') -
                F('sell_quantity') * F('variant__cost_price')
            ),
            total_revenue=Sum(F('sell_quantity') * F('sale_price')),
            total_qty=Sum('sell_quantity'),
        ).order_by('month', '-total_profit')

        # ── Chart 1 — Max Profit Product Per Month (Bar) ──
        chart1 = self.chart_max_profit_per_month(data)

        # ── Chart 2 — Top 5 Products Overall (Horizontal Bar) ──
        chart2 = self.chart_top_products()

        # ── Chart 3 — Monthly Profit Trend (Line) ──
        chart3 = self.chart_monthly_trend()

        # ── Chart 4 — Category Profit (Pie) ──
        chart4 = self.chart_category_pie()

        return render(request, 'store/matplotlib_charts.html', {
            'chart1': chart1,
            'chart2': chart2,
            'chart3': chart3,
            'chart4': chart4,
            'data':   data,
        })

    def chart_max_profit_per_month(self, data):

        # Group by month → find max profit product
        monthly = {}
        for row in data:
            month = row['month'].strftime('%b %Y')
            if month not in monthly:
                monthly[month] = []
            monthly[month].append({
                'product': f"{row['variant__brand'] or ''} {row['variant__product__prod_name']}".strip(),
                'profit':  float(row['total_profit'] or 0),
            })

        # Pick max profit product for each month
        months   = []
        products = []
        profits  = []
        for month, items in monthly.items():
            best = max(items, key=lambda x: x['profit'])
            months.append(month)
            products.append(best['product'])
            profits.append(best['profit'])

        if not months:
            return None

        colors = plt.cm.Blues([0.5 + 0.5 * p / max(profits) for p in profits])

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f0f5ff')

        bars = ax.bar(months, profits, color=colors,
                      edgecolor='white', linewidth=1.5,
                      width=0.55, zorder=3)

        # Value labels on bars
        for bar, product, profit in zip(bars, products, profits):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(profits) * 0.02,
                    f'₹{profit:,.0f}',
                    ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color='#1e40af')
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() / 2,
                    product[:14] + ('…' if len(product) > 14 else ''),
                    ha='center', va='center',
                    fontsize=8, color='white', fontweight='bold')

        ax.set_title('Most Profitable Product Per Month',
                     fontsize=15, fontweight='bold',
                     color='#0f172a', pad=16)
        ax.set_xlabel('Month', fontsize=11, color='#64748b')
        ax.set_ylabel('Max Profit (₹)', fontsize=11, color='#64748b')
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
        ax.grid(axis='y', color='white', linewidth=1.2, zorder=2)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors='#64748b')
        plt.tight_layout()
        return generate_chart(fig)



    def chart_top_products(self):
        top = Sales.objects.values(
            'variant__product__prod_name',
            'variant__brand',
        ).annotate(
            total_profit=Sum(
                F('sell_quantity') * F('sale_price') -
                F('sell_quantity') * F('variant__cost_price')
            )
        ).order_by('-total_profit')[:8]

        if not top:
            return None

        labels  = [
            f"{p['variant__brand'] or ''} {p['variant__product__prod_name']}".strip()
            for p in top
        ]
        profits = [float(p['total_profit'] or 0) for p in top]
        colors  = ['#1a56db','#2563eb','#3b82f6','#60a5fa',
                   '#93c5fd','#1e40af','#1d4ed8','#2d6dd4'][:len(profits)]

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f0f5ff')

        bars = ax.barh(labels, profits, color=colors,
                       edgecolor='white', linewidth=1.2,
                       height=0.55, zorder=3)

        for bar, profit in zip(bars, profits):
            ax.text(profit + max(profits) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f'₹{profit:,.0f}',
                    va='center', fontsize=9,
                    fontweight='bold', color='#1e40af')

        ax.set_title('Top Products by Total Profit',
                     fontsize=14, fontweight='bold',
                     color='#0f172a', pad=14)
        ax.set_xlabel('Total Profit (₹)', fontsize=10, color='#64748b')
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
        ax.grid(axis='x', color='white', linewidth=1.2, zorder=2)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors='#64748b')
        ax.invert_yaxis()
        plt.tight_layout()

        return generate_chart(fig)



    def chart_monthly_trend(self):
        monthly = Sales.objects.annotate(
            month=TruncMonth('sold_at')
        ).values('month').annotate(
            total_profit =Sum(
                F('sell_quantity') * F('sale_price') -
                F('sell_quantity') * F('variant__cost_price')
            ),
            total_revenue=Sum(F('sell_quantity') * F('sale_price')),
        ).order_by('month')

        if not monthly:
            return None

        months  = [m['month'].strftime('%b %Y') for m in monthly]
        profits  = [float(m['total_profit']  or 0) for m in monthly]
        revenues = [float(m['total_revenue'] or 0) for m in monthly]
        x        = range(len(months))

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f0f5ff')

        # Revenue line
        ax.plot(x, revenues, color='#3b82f6', linewidth=2.5,
                marker='o', markersize=7, label='Revenue ₹',
                markerfacecolor='#1a56db', zorder=4)
        ax.fill_between(x, revenues, alpha=0.08, color='#3b82f6')

        # Profit line
        ax.plot(x, profits, color='#f59e0b', linewidth=2.5,
                marker='s', markersize=7, label='Profit ₹',
                markerfacecolor='#d97706', zorder=4)
        ax.fill_between(x, profits, alpha=0.08, color='#f59e0b')

        # Value labels
        for i, (r, p) in enumerate(zip(revenues, profits)):
            ax.annotate(f'₹{r:,.0f}', (i, r),
                        textcoords='offset points',
                        xytext=(0, 10), ha='center',
                        fontsize=8, color='#1e40af', fontweight='bold')
            ax.annotate(f'₹{p:,.0f}', (i, p),
                        textcoords='offset points',
                        xytext=(0, -16), ha='center',
                        fontsize=8, color='#b45309', fontweight='bold')

        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=30, ha='right')
        ax.set_title('Monthly Revenue vs Profit Trend',
                     fontsize=14, fontweight='bold',
                     color='#0f172a', pad=14)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
        ax.legend(fontsize=10)
        ax.grid(color='white', linewidth=1.2, zorder=2)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors='#64748b')
        plt.tight_layout()

        return generate_chart(fig)

    def chart_category_pie(self):
        cats = Sales.objects.values(
            'variant__product__category__name'
        ).annotate(
            total_profit=Sum(
                F('sell_quantity') * F('sale_price') -
                F('sell_quantity') * F('variant__cost_price')
            )
        ).order_by('-total_profit')

        if not cats:
            return None

        labels  = [c['variant__product__category__name'] for c in cats]
        profits = [float(c['total_profit'] or 0) for c in cats]
        colors  = ['#1a56db','#3b82f6','#60a5fa','#93c5fd',
                   '#f59e0b','#10b981','#8b5cf6','#ef4444'][:len(profits)]

        fig, ax = plt.subplots(figsize=(7, 6))
        fig.patch.set_facecolor('#f8faff')

        wedges, texts, autotexts = ax.pie(
            profits,
            labels     = None,
            colors     = colors,
            autopct    = '%1.1f%%',
            startangle = 140,
            wedgeprops = dict(edgecolor='white', linewidth=2),
            pctdistance= 0.75,
        )

        for at in autotexts:
            at.set_fontsize(9)
            at.set_fontweight('bold')
            at.set_color('white')

        # Legend with profit values
        legend_labels = [
            f"{l}  ₹{p:,.0f}"
            for l, p in zip(labels, profits)
        ]
        ax.legend(wedges, legend_labels,
                  loc='lower center',
                  bbox_to_anchor=(0.5, -0.15),
                  ncol=2, fontsize=9,
                  framealpha=0.5)

        ax.set_title('Profit by Category',
                     fontsize=14, fontweight='bold',
                     color='#0f172a', pad=14)

        # Draw center circle for donut effect
        centre = plt.Circle((0, 0), 0.5,
                             fc='#f8faff', linewidth=2,
                             edgecolor='white')
        ax.add_patch(centre)
        ax.text(0, 0, 'Profit\nShare',
                ha='center', va='center',
                fontsize=10, fontweight='bold', color='#1e40af')

        plt.tight_layout()
        return generate_chart(fig)

def generate_chart(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',
                dpi=130, facecolor='#f8faff')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img



def binary_search(products, target):
    """
    Binary Search Algorithm
    Searches product name in sorted product list
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    steps = []
    low, high = 0, len(products) - 1
    target = target.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_val = products[mid]['name'].lower()

        steps.append({
            'low': low, 'mid': mid,
            'high': high, 'checked': mid_val,
        })

        if mid_val == target:
            return mid, steps
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, steps



def merge_sort(arr, key='profit'):
    """
    Merge Sort Algorithm
    Sorts products by profit in descending order
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid],  key)
    right = merge_sort(arr[mid:],  key)

    return merge(left, right, key)


def merge(left, right, key):
    result = []
    i = j  = 0

    while i < len(left) and j < len(right):
        # Descending order — higher profit first
        if left[i][key] >= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack_max_profit(products, budget):
    """
    0/1 Knapsack Algorithm
    Selects which products to stock to maximize profit
    within a given monthly budget (cost constraint)

    products: list of {name, cost, profit, stock}
    budget:   total monthly investment budget (₹)

    Time Complexity:  O(n × W)
    Space Complexity: O(n × W)
    """
    n   = len(products)
    W   = int(budget)

    # Build DP table
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost   = int(products[i-1]['cost'])
        profit = int(products[i-1]['profit'])

        for w in range(W + 1):
            # Don't pick item i
            dp[i][w] = dp[i-1][w]

            # Pick item i if it fits
            if cost <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i-1][w - cost] + profit
                )

    # Backtrack to find selected items
    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(products[i-1])
            w -= int(products[i-1]['cost'])

    return dp[n][W], selected, dp


#daa section
class DAAView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        search_query = request.GET.get('search', '')
        budget       = float(request.GET.get('budget', 5000))

        # ── Fetch Sales Data ──
        monthly_sales = Sales.objects.annotate(
            month=TruncMonth('sold_at')
        ).values(
            'variant__product__prod_name',
            'variant__brand',
            'variant__cost_price',
            'month',
        ).annotate(
            total_profit  = Sum(
                F('sell_quantity') * F('sale_price') -
                F('sell_quantity') * F('variant__cost_price')
            ),
            total_revenue = Sum(F('sell_quantity') * F('sale_price')),
            total_cost    = Sum(F('sell_quantity') * F('variant__cost_price')),
            total_qty     = Sum('sell_quantity'),
        ).order_by('month', '-total_profit')

        # ── Build Product List for Algorithms ──
        product_map = {}
        for row in monthly_sales:
            name = f"{row['variant__brand'] or ''} {row['variant__product__prod_name']}".strip()
            if name not in product_map:
                product_map[name] = {
                    'name':    name,
                    'profit':  float(row['total_profit']  or 0),
                    'cost':    float(row['total_cost']    or 0),
                    'revenue': float(row['total_revenue'] or 0),
                    'qty':     int(row['total_qty']       or 0),
                }
            else:
                product_map[name]['profit']  += float(row['total_profit']  or 0)
                product_map[name]['cost']    += float(row['total_cost']    or 0)
                product_map[name]['revenue'] += float(row['total_revenue'] or 0)
                product_map[name]['qty']     += int(row['total_qty']       or 0)

        all_products = list(product_map.values())


        sorted_for_search = sorted(all_products, key=lambda x: x['name'].lower())
        search_result     = None
        search_steps      = []
        search_time       = 0

        if search_query:
            start              = time.perf_counter()
            idx, search_steps  = binary_search(sorted_for_search, search_query)
            search_time        = round((time.perf_counter() - start) * 1000, 4)
            if idx != -1:
                search_result = sorted_for_search[idx]

        start            = time.perf_counter()
        sorted_products  = merge_sort(all_products, key='profit')
        sort_time        = round((time.perf_counter() - start) * 1000, 4)


        knapsack_products = [
            p for p in all_products
            if p['cost'] > 0 and p['profit'] > 0
        ]

        start                          = time.perf_counter()
        max_profit, selected, dp_table = knapsack_max_profit(
            knapsack_products, budget
        )
        knapsack_time = round((time.perf_counter() - start) * 1000, 4)

        chart_sort     = self.chart_merge_sort(sorted_products[:10])
        chart_knapsack = self.chart_knapsack(
            knapsack_products, selected, budget
        )
        chart_monthly  = self.chart_monthly_max(monthly_sales)
        chart_compare  = self.chart_algo_comparison(all_products)

        return render(request, 'store/daa.html', {
            # Data
            'all_products':    all_products,
            'sorted_products': sorted_products,
            'monthly_sales':   monthly_sales,
            # Search
            'search_query':    search_query,
            'search_result':   search_result,
            'search_steps':    search_steps,
            'search_time':     search_time,
            'sorted_for_search': sorted_for_search,
            # Sort
            'sort_time':       sort_time,
            # Knapsack
            'budget':          budget,
            'max_profit':      max_profit,
            'selected':        selected,
            'knapsack_time':   knapsack_time,
            'knapsack_products': knapsack_products,
            # Charts
            'chart_sort':      chart_sort,
            'chart_knapsack':  chart_knapsack,
            'chart_monthly':   chart_monthly,
            'chart_compare':   chart_compare,
        })


    def chart_merge_sort(self, sorted_products):
        if not sorted_products:
            return None

        names   = [p['name'][:12] + '…' if len(p['name']) > 12
                   else p['name'] for p in sorted_products]
        profits = [p['profit'] for p in sorted_products]
        colors  = plt.cm.Blues(
            [0.4 + 0.6 * p / max(profits) for p in profits]
        )

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f0f5ff')

        bars = ax.bar(names, profits, color=colors,
                      edgecolor='white', linewidth=1.5,
                      width=0.6, zorder=3)

        for bar, p in zip(bars, profits):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(profits) * 0.01,
                    f'₹{p:,.0f}',
                    ha='center', fontsize=8,
                    fontweight='bold', color='#1e40af')

        ax.set_title(
            'Merge Sort — Products Sorted by Profit (Descending)',
            fontsize=13, fontweight='bold', color='#0f172a', pad=14
        )
        ax.set_ylabel('Total Profit (₹)', fontsize=10, color='#64748b')
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
        ax.set_xlabel(
            'Products  →  Sorted by Merge Sort O(n log n)',
            fontsize=9, color='#64748b'
        )
        ax.tick_params(axis='x', rotation=25, colors='#64748b')
        ax.tick_params(axis='y', colors='#64748b')
        ax.grid(axis='y', color='white', linewidth=1.2, zorder=2)
        ax.spines[:].set_visible(False)

        # Add rank labels
        for i, bar in enumerate(bars):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() / 2,
                    f'#{i+1}',
                    ha='center', va='center',
                    fontsize=9, color='white', fontweight='bold')

        plt.tight_layout()
        return generate_chart(fig)


    def chart_knapsack(self, all_products, selected, budget):
        if not all_products:
            return None

        selected_names = {p['name'] for p in selected}
        names    = [p['name'][:10] + '…' if len(p['name']) > 10
                    else p['name'] for p in all_products[:12]]
        profits  = [p['profit'] for p in all_products[:12]]
        costs    = [p['cost']   for p in all_products[:12]]
        colors   = [
            '#1a56db' if all_products[i]['name'] in selected_names
            else '#cbd5e1'
            for i in range(len(all_products[:12]))
        ]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.patch.set_facecolor('#f8faff')

        # Left — Profit bars
        ax1.set_facecolor('#f0f5ff')
        bars1 = ax1.bar(names, profits, color=colors,
                        edgecolor='white', linewidth=1.5,
                        width=0.6, zorder=3)
        ax1.set_title(
            f'Knapsack — Max Profit within ₹{budget:,.0f} Budget',
            fontsize=11, fontweight='bold', color='#0f172a', pad=12
        )
        ax1.set_ylabel('Profit (₹)', fontsize=9, color='#64748b')
        ax1.tick_params(axis='x', rotation=35, colors='#64748b', labelsize=8)
        ax1.tick_params(axis='y', colors='#64748b')
        ax1.grid(axis='y', color='white', linewidth=1.2, zorder=2)
        ax1.spines[:].set_visible(False)
        ax1.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

        # Legend
        p1 = mpatches.Patch(color='#1a56db', label='✅ Selected by Knapsack')
        p2 = mpatches.Patch(color='#cbd5e1', label='❌ Not Selected')
        ax1.legend(handles=[p1, p2], fontsize=9, loc='upper right')

        # Right — Cost vs Profit scatter
        ax2.set_facecolor('#f0f5ff')
        scatter_colors = [
            '#1a56db' if all_products[i]['name'] in selected_names
            else '#94a3b8'
            for i in range(len(all_products[:12]))
        ]
        ax2.scatter(costs, profits, c=scatter_colors,
                    s=120, zorder=4, edgecolors='white', linewidth=1.5)

        for i, name in enumerate(names):
            ax2.annotate(name,
                         (costs[i], profits[i]),
                         textcoords='offset points',
                         xytext=(5, 5),
                         fontsize=7, color='#64748b')

        # Budget line
        ax2.axvline(x=budget, color='#ef4444', linewidth=2,
                    linestyle='--', label=f'Budget ₹{budget:,.0f}', zorder=3)
        ax2.set_title('Cost vs Profit Scatter',
                      fontsize=11, fontweight='bold',
                      color='#0f172a', pad=12)
        ax2.set_xlabel('Total Cost (₹)', fontsize=9, color='#64748b')
        ax2.set_ylabel('Total Profit (₹)', fontsize=9, color='#64748b')
        ax2.legend(fontsize=9)
        ax2.grid(color='white', linewidth=1.2, zorder=2)
        ax2.spines[:].set_visible(False)
        ax2.tick_params(colors='#64748b')

        plt.tight_layout()
        return generate_chart(fig)

    def chart_monthly_max(self, monthly_sales):
        monthly = {}
        for row in monthly_sales:
            month = row['month'].strftime('%b %Y')
            profit = float(row['total_profit'] or 0)
            name   = f"{row['variant__brand'] or ''} {row['variant__product__prod_name']}".strip()
            if month not in monthly or profit > monthly[month]['profit']:
                monthly[month] = {'product': name, 'profit': profit}

        if not monthly:
            return None

        months  = list(monthly.keys())
        profits = [monthly[m]['profit'] for m in months]
        names   = [monthly[m]['product'] for m in months]
        colors  = plt.cm.Blues(
            [0.45 + 0.55 * p / max(profits) for p in profits]
        )

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f0f5ff')

        bars = ax.bar(months, profits, color=colors,
                      edgecolor='white', linewidth=1.5,
                      width=0.55, zorder=3)

        for bar, name, profit in zip(bars, names, profits):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(profits) * 0.015,
                    f'₹{profit:,.0f}',
                    ha='center', fontsize=9,
                    fontweight='bold', color='#1e40af')
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() / 2,
                    (name[:12] + '…' if len(name) > 12 else name),
                    ha='center', va='center',
                    fontsize=8, color='white', fontweight='bold')

        ax.set_title(
            'Max Profit Product Per Month (Knapsack Greedy Insight)',
            fontsize=13, fontweight='bold', color='#0f172a', pad=14
        )
        ax.set_ylabel('Max Profit (₹)', fontsize=10, color='#64748b')
        ax.set_xlabel('Month', fontsize=10, color='#64748b')
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
        ax.grid(axis='y', color='white', linewidth=1.2, zorder=2)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors='#64748b')
        plt.tight_layout()
        return generate_chart(fig)

    # ──────────────────────────────────────────
    # CHART — Algorithm Complexity Comparison
    # ──────────────────────────────────────────
    def chart_algo_comparison(self, products):
        n      = max(len(products), 1)
        x      = list(range(1, n + 1))
        binary = [
            round(__import__('math').log2(i), 2) for i in x
        ]
        merge  = [
            round(i * __import__('math').log2(max(i, 1)), 2) for i in x
        ]
        knapsack = [i * 50 for i in x]  # O(n×W), W=50 approx

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f0f5ff')

        ax.plot(x, binary,   color='#10b981', linewidth=2.5,
                label='Binary Search  O(log n)',  marker='')
        ax.plot(x, merge,    color='#1a56db', linewidth=2.5,
                label='Merge Sort  O(n log n)',    marker='')
        ax.plot(x, knapsack, color='#f59e0b', linewidth=2.5,
                label='Knapsack  O(n × W)',        marker='', linestyle='--')

        ax.set_title('Algorithm Complexity Comparison',
                     fontsize=13, fontweight='bold',
                     color='#0f172a', pad=14)
        ax.set_xlabel(f'Input Size n  (current n = {n})',
                      fontsize=9, color='#64748b')
        ax.set_ylabel('Operations', fontsize=9, color='#64748b')
        ax.legend(fontsize=10)
        ax.grid(color='white', linewidth=1.2, zorder=2)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors='#64748b')

        # Mark current n
        ax.axvline(x=n, color='#ef4444', linewidth=1.5,
                   linestyle=':', label=f'n={n}')
        plt.tight_layout()
        return generate_chart(fig)



















