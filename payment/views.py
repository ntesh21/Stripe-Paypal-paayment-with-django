# payments/views.py
import stripe 

from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from datetime import datetime
# from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
import pdb

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render 

stripe.api_key = settings.STRIPE_SECRET_KEY 

class HomePageView(TemplateView):
    template_name = 'home.html'

class PackagesView(TemplateView):
    template_name = 'packages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request): 
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=50000,
            currency='usd',
            description= 'TNT Payment',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')

def paypal_pay(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        # "password":settings.PAYPAL_API_PASSWORD,
        # "signature":settings.PAYPAL_API_SIGNATURE,
        "amount": "100",
        "item_name": "TNT Listing",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('done')),
        "cancel_return": request.build_absolute_uri(reverse('canceled')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "home.html", context)

@csrf_exempt
def pay_done(request):
    
    # Creating a context dictionary with user information
    context_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "100",
        "item_name": "TNT Listing",
    }
    
    return render(request, 'pay-done.html', context_dict)


@csrf_exempt
def pay_canceled(request):
    return render(request, 'canceled.html')


# calling function for response from paypal API
# valid_ipn_received.connect(show_me_the_money)

# invalid_ipn_received.connect(show_me_the_money)