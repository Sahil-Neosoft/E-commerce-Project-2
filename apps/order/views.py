from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Order, Address
from apps.product.models import Product, Size, Color
from apps.cart.models import CartItem
from apps.cart.views import get_or_create_cart
from .districts import districts

def checkout_view(request):
    """Checkout process"""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    # Check stock availability for all items
    for item in cart.items.all():
        if not item.product.can_order(item.quantity):
            messages.error(
                request,
                f'Sorry, {item.product.name} is out of stock or has insufficient quantity.'
            )
            return redirect('cart')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        district = request.POST.get('district')

        if name == '' or email == '' or phone == '' or address == '' or district == '':
            messages.error(request, 'Please fill in all required fields.')
            return redirect('checkout')

        # Create address
        address = Address.objects.create(
            name=name,
            email=email,
            phone=phone,
            district=district,
            address=address,
        )
        # Calculate shipping 
        shipping_cost = settings.SHIPPING_COST_DHAKA if district == 'Dhaka' else settings.SHIPPING_COST 
        
        # Create order
        order = Order.create_from_cart(cart, address, shipping_cost)
        
        if order:
            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('confirmation', order_number=order.order_number) 
        else:
            messages.error(request, 'Error placing order. Please try again.')
    
    context = {
        'cart': cart,
        'districts': districts,
        'cart_items': cart.items.select_related('product').all(),
        'subtotal': cart.get_total_price(),
    }
    return render(request, 'order/checkout.html', context)

def buy_now(request):
    """Buy now view for quick purchase"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        
        # Get the product and check if it can be ordered
        product = get_object_or_404(Product, id=product_id, is_active=True)
        if product.sizes.exists():
            if not size_id == '':
                size = get_object_or_404(Size, id=size_id, product=product)
            else:
                messages.error(request, 'Please select a size.')
                return redirect('product_detail', slug=product.slug)
        if product.colors.exists():
            if not color_id == '':
                color = get_object_or_404(Color, id=color_id, product=product)
            else:
                messages.error(request, 'Please select a color.')
                return redirect('product_detail', slug=product.slug)

        if not product.can_order(quantity):
            messages.error(request, f'Sorry, {product.name} is out of stock or has insufficient quantity.')
            return redirect('product_detail', slug=product.slug)
        
        # Create a temporary cart item
        cart_item = CartItem.objects.create(
            product=product,
            quantity=quantity,
            user=request.user
        )
        
        # Redirect to checkout with the temporary cart item
        return redirect('checkout')
    
    messages.error(request, 'Invalid request.')
    return redirect('home')


def confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'order/confirmation.html', {'order': order})

# ============================================================================
# ORDER VIEWS
# ============================================================================

@login_required
def order_list_view(request):
    """List user's orders"""
    orders = request.user.get_orders()
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
    }
    return render(request, 'store/order_list.html', context)


@login_required
def order_detail_view(request, order_number):
    """Order detail view"""
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )
    
    order_items = order.items.select_related('product', 'size', 'color').all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_detail.html', context)


@login_required
@require_POST
def cancel_order(request, order_number):
    """Cancel an order"""
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )
    
    if order.cancel_order():
        messages.success(request, f'Order {order.order_number} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('order_detail', order_number=order.order_number)
