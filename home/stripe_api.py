import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY
baseUrl = settings.BASE_URL


class StripeAPI:
    
    @classmethod
    def create_customer(cls, name, email, phone, **kwargs):
        customer = stripe.Customer.create(
            name=name,
            phone=phone,
            email=email,
        )
        return customer
    
    @classmethod
    def retrieve_customer(cls, customer_id):
        customer = stripe.Customer.retrieve(customer_id)
        return customer

    @classmethod
    def create_payment_session(cls, name, amount, **kwargs):

        """
        Initiate a stripe transaction
        """
        try:
            return_url = kwargs.get('return_url', )
            customer_id = kwargs.get('customer_id', )
            stripe_payment = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": name,
                            },
                            "unit_amount": int(amount) * 100,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=return_url + '?reference={CHECKOUT_SESSION_ID}',
                cancel_url=f"{baseUrl}",
                customer=customer_id,
            )
            return True, stripe_payment
        except Exception as err:
            # traceback.print_exc()
            return False, f"{err}"

    @classmethod
    def retrieve_checkout_session(cls, session_id):
        result = stripe.checkout.Session.retrieve(session_id)
        return result
    
    @classmethod
    def retrieve_setup_intent(cls, setup_intent):
        result = stripe.SetupIntent.retrieve(setup_intent)
        return result
    
    @classmethod
    def retrieve_payment_method(cls, payment_method_id):
        result = stripe.PaymentMethod.retrieve(payment_method_id)
        return result

    @classmethod
    def auto_charge_with_payment_method(cls, amount, currency_code, payment_method_id, **kwargs):
        description = kwargs.get('description', )
        customer_id = kwargs.get('customer_id', )
        # metadata = kwargs.get('metadata', {})
        # if type(metadata) is not dict:
        #     return False, create_error_message('metadata', "metadata must be a dictionary")
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                payment_method=payment_method_id,
                currency=currency_code,
                confirm=True,
                # return_url=return_url,
                description=description,
                # metadata=metadata,
                payment_method_types=[
                    'card',
                ],
                setup_future_usage='off_session',
                customer=customer_id,
            )
            return True, intent
        except Exception as ex:
            return False, str(ex)
    
    @classmethod
    def retrieve_payment_intent(cls, payment_intent):
        return stripe.PaymentIntent.retrieve(payment_intent)






