from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .shopier_service import ShopierService

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product_list.html', {
        'category': category, 'categories': categories, 'products': products
    })

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('shop:product_list')
    
    if request.method == 'POST':
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city')
        )
        for item in cart:
            OrderItem.objects.create(
                order=order, 
                product=item['product'],
                price=item['price'], 
                quantity=item['quantity']
            )
        
        shopier_service = ShopierService()
        callback_url = request.build_absolute_uri('/shopier-callback/')
        form_html = shopier_service.generate_payment_form(order, cart.get_total_price(), callback_url)
        
        cart.clear()
        return HttpResponse(form_html)
        
    return render(request, 'shop/order_create.html', {'cart': cart})

@csrf_exempt
def shopier_callback(request):
    if request.method == 'POST':
        shopier_service = ShopierService()
        success, order_id = shopier_service.verify_callback(request.POST)
        if success:
            try:
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.shopier_order_id = request.POST.get('shopier_order_id')
                order.save()
                return HttpResponse("OK", status=200)
            except Order.DoesNotExist:
                return HttpResponse("Order Not Found", status=404)
    return HttpResponse("Invalid Request", status=400)