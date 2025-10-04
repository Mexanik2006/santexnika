from django.forms import formset_factory
from django.urls import reverse
import qrcode
import json
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.utils import timezone
from xhtml2pdf import pisa
from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import Sale
from .forms import SaleForm, SaleItemForm
from clients.models import Account
from products.models import Product

@login_required
def sale_list(request):
    try:
        sales = Sale.objects.all().select_related('product', 'client', 'seller').order_by('-sale_date')
        
        # Statistics
        total_sales = sales.count()
        total_revenue = sales.aggregate(total=Sum('final_price'))['total'] or 0
        today_sales = sales.filter(sale_date__date=timezone.now().date())
        today_revenue = today_sales.aggregate(total=Sum('final_price'))['total'] or 0
        
        context = {
            'sales': sales,
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'today_sales': today_sales.count(),
            'today_revenue': today_revenue,
        }
        return render(request, 'sell/sale_list.html', context)
    except Exception as e:
        # Agar hali jadval yaratilmagan bo'lsa
        context = {
            'sales': [],
            'total_sales': 0,
            'total_revenue': 0,
            'today_sales': 0,
            'today_revenue': 0,
        }
        return render(request, 'sell/sale_list.html', context)

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                # Get common sale data
                sale_data = form.cleaned_data
                client = sale_data['client']
                discount = sale_data['discount']
                payment_method = sale_data['payment_method']
                
                # Parse multiple items from POST
                product_ids = request.POST.getlist('product')
                quantities = request.POST.getlist('quantity')
                unit_prices = request.POST.getlist('unit_price')
                
                # Debug print
                print(f"DEBUG POST: products={product_ids}, quantities={quantities}, unit_prices={unit_prices}")
                
                total_final_price = Decimal('0')
                saved_sales = []
                
                # Process each item
                for i in range(len(product_ids)):
                    if i >= len(quantities) or i >= len(unit_prices):
                        print(f"Skipping item {i}: Lists mismatch")
                        continue
                    
                    product_id = product_ids[i].strip()
                    quantity_str = quantities[i].strip()
                    unit_price_str = unit_prices[i].strip()
                    
                    if not product_id or not quantity_str:
                        print(f"Skipping item {i}: missing product or quantity")
                        continue
                    
                    try:
                        product = Product.objects.get(id=product_id)
                        quantity = Decimal(quantity_str)
                        if quantity <= 0:
                            print(f"Skipping item {i}: quantity <= 0")
                            continue
                        
                        # Check stock here too, but model will validate
                        if quantity > product.quantity:
                            form.add_error(None, f"Mahsulot '{product.name}' uchun yetarli miqdor yo'q. Mavjud: {product.quantity}")
                            continue
                            
                        unit_price = Decimal(unit_price_str) if unit_price_str else product.price
                        
                        # Calculate item totals
                        total_price = quantity * unit_price
                        discount_amount = total_price * (discount / Decimal('100'))
                        final_price = total_price - discount_amount
                        total_final_price += final_price
                        
                        # Create and save Sale for each item
                        sale = Sale(
                            client=client,
                            product=product,
                            quantity=quantity,
                            unit_price=unit_price,
                            total_price=total_price,
                            discount=discount,
                            final_price=final_price,
                            payment_method=payment_method,
                            seller=request.user
                        )
                        sale.save()  # Model will re-validate and update stock
                        saved_sales.append(sale)
                        print(f"Saved sale {sale.id} for {product.name}")
                        
                    except Product.DoesNotExist:
                        print(f"Item {i}: Product {product_id} not found")
                        form.add_error(None, f"Mahsulot {product_id} topilmadi")
                        continue
                    except ValidationError as ve:
                        print(f"Item {i}: Validation error {ve}")
                        form.add_error(None, str(ve))
                        continue
                    except ValueError:
                        print(f"Item {i}: ValueError in Decimal conversion")
                        form.add_error(None, "Miqdor yoki narx noto'g'ri formatda")
                        continue
                    except Exception as item_error:
                        print(f"Item {i}: Unexpected error {item_error}")
                        form.add_error(None, f"Item {i} saqlashda xato: {str(item_error)}")
                        continue
                
                if saved_sales:
                    print(f"Successfully saved {len(saved_sales)} sales")
                    return redirect('sale_list')
                else:
                    form.add_error(None, "Hech qanday mahsulot saqlanmadi. Miqdor va mahsulotni tekshiring.")
                    
            except Exception as e:
                print(f"Overall error in sale_create: {e}")
                form.add_error(None, f"Sotuvni saqlashda xatolik: {str(e)}")
        else:
            # Form errors
            print("Form invalid:", form.errors)
    else:
        form = SaleForm()
    
    # Products for dropdown - only available
    all_products = Product.objects.filter(quantity__gt=0).order_by('name')
    recent_products = Product.objects.filter(quantity__gt=0).order_by('-created_at')[:10]
    
    print(f"DEBUG: Total available products: {all_products.count()}")
    
    return render(request, 'sell/sale_form.html', {
        'form': form,
        'all_products': all_products,
        'recent_products': recent_products
    })

@login_required
def sale_detail(request, id):
    sale = get_object_or_404(Sale, id=id)
    return render(request, 'sell/sale_detail.html', {'sale': sale})

@login_required
def sale_receipt(request, id):
    sale = get_object_or_404(Sale, id=id)
    
    # Generate PDF receipt using xhtml2pdf
    html_string = render_to_string('sell/receipt_pdf.html', {'sale': sale})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="chek_{sale.id}.pdf"'
    
    # Create PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('PDF yaratishda xatolik')
    return response

# ... (imports and sale fetch stay the same)

@login_required
def sale_qr_code(request, id):
    sale = get_object_or_404(Sale, id=id)
    
    # Build the full URL to the receipt—portable and precise!
    receipt_url = request.build_absolute_uri(reverse('sale_receipt', args=[sale.id]))
    print(f"DEBUG: QR encoding URL: {receipt_url}")  # For your console curiosity—what does it look like?
    
    # Generate QR code with the URL (no JSON needed now—pure action!)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(receipt_url)  # Etch the invitation!
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')

# AJAX views for dynamic functionality
@login_required
def get_client_discount(request):
    client_id = request.GET.get('client_id')
    try:
        client = Account.objects.get(id=client_id)
        discount = getattr(client, 'skidka', 0)
        return JsonResponse({'discount': discount})
    except Account.DoesNotExist:
        return JsonResponse({'discount': 0})

@login_required
def get_product_info(request):
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'price': str(product.price),  # String for JS
            'quantity': str(product.quantity),
            'unit': product.unit,
            'name': product.name,
            'brand': product.brand
        })
    except Product.DoesNotExist:
        return JsonResponse({'price': '0', 'quantity': '0', 'unit': '', 'name': '', 'brand': ''})