from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer  # ensure this matches your actual model name
from products.models import products  # ensure this matches your actual Product model
from .models import order, orderdItem

def show_cart(request):
    user = request.user
    customer, _ = Customer.objects.get_or_create(user=user)
    cart_obj, _ = order.objects.get_or_create(
        owner=customer,
        order_status=order.CART_STAGE
       
    )
   
    subtotal = 0
    for item in cart_obj.added_items.all():
        subtotal += item.product.price * item.quantity

    tax = subtotal * 0.05  # Example: 5% tax
    total = subtotal + tax
    
    context = {
        'cart': cart_obj,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    # return render(request, 'cart.html', { 'cart': cart_obj })
    return render(request, 'cart.html',context)


def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        customer, _ = Customer.objects.get_or_create(user=user)

        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart_obj, _ = order.objects.get_or_create(
            owner=customer,
            order_status=order.CART_STAGE
        )

        # Retrieve the product; wrap in try/except if needed
        product = products.objects.get(pk=product_id)

        ordered_item = orderdItem.objects.create(
            product=product,
            owner=cart_obj,
            quantity=quantity
        )
        cart_obj.update_total()
        return redirect('cart')

    return redirect('products:list')


def remove_from_cart(request, item_id):
    user = request.user
    customer, _ = Customer.objects.get_or_create(user=user)
    
    cart_obj, _ = order.objects.get_or_create(
        owner=customer,
        order_status=order.CART_STAGE
    )

    item = get_object_or_404(orderdItem, id=item_id, owner=cart_obj)
    item.delete()
    cart_obj.update_total()
    return redirect('cart')



def payment(request):
    user = request.user
    customer, _ = Customer.objects.get_or_create(user=user)
    cart_obj, _ = order.objects.get_or_create(
        owner=customer,
        order_status=order.CART_STAGE
    )
    subtotal = sum(item.product.price * item.quantity for item in cart_obj.added_items.all())
    tax = subtotal * 0.05  # e.g., 5% tax
    total = subtotal + tax
    

    return render(request, 'payment.html', {
        'cart': cart_obj,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    })
def process_payment(request):
    if request.method == "POST":
        user = request.user
        customer = Customer.objects.get(user=user)
        cart_obj = order.objects.get(owner=customer, order_status=order.CART_STAGE)
        cart_obj.update_total()
        # Here you would integrate Stripe, Razorpay, etc.
        # For now, just mark it as completed:
        cart_obj.order_status = order.ORDER_PROCESSED  # Example status
        # cart_obj.order_status = 'Processing'
        cart_obj.save()
        return redirect('order_status')
    return redirect('cart')



@login_required
def order_status(request):
    """Show all orders for the logged-in user"""
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = order.objects.filter(owner=customer).order_by('created_at')

    context = {
        'orders': orders
    }
    return render(request, 'my_orders.html', context)

