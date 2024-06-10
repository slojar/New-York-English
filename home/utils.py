import datetime

import requests
from django.conf import settings
from home.models import Transaction
from home.stripe_api import StripeAPI

baseUrl = settings.BASE_URL


def transcribe_audio(file_path, file_name):
    url = "https://whisper-speech-to-text1.p.rapidapi.com/speech-to-text"
    payload = {}
    files = [('file', (f'{file_name}', open(f'{file_path}', 'rb'), 'audio/wav'))]
    headers = {
        'X-RapidAPI-Key': "0f43aba653msha66145151f241e9p160427jsn3d36e8ad9e0d",
        'X-RapidAPI-Host': "whisper-speech-to-text1.p.rapidapi.com"
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    result = ""
    if response.status_code == 200:
        response = response.json()
        result = response["text"]

    # response = {
    #     "success": True,
    #     "text": "What is your name"
    # }
    # result = response["text"]
    return result


def complete_payment(ref_number):
    try:
        trans = Transaction.objects.get(transaction_id=ref_number, status="pending")
    except Transaction.DoesNotExist:
        return False, f'Reference Number ({ref_number}) not found'

    reference = str(ref_number)

    if str(ref_number).lower().startswith('cs_'):
        try:
            result = StripeAPI.retrieve_checkout_session(session_id=reference)
            reference = result.get('payment_intent')
        except Exception as ex:
            pass

    result = dict()
    if str(reference).lower().startswith('pi_'):
        result = StripeAPI.retrieve_payment_intent(payment_intent=reference)
    if str(reference).lower().startswith('cs_'):
        result = StripeAPI.retrieve_checkout_session(session_id=reference)

    if result.get('status') and str(result.get('status')).lower() in ['succeeded', 'success', 'successful']:
        trans.status = "success"
        trans.save()
        # update user to subscribed
        trans.user.userprofile.subscribed = True
        trans.user.userprofile.save()
        return True, "Payment updated"
    else:
        trans.status = "failed"
        trans.save()
        return False, ""


def payment_checkout(user_profile):
    success = False
    amount = float(1.0)
    callback_url = f"{baseUrl}/payment-verify"
    stripe_customer_id = ""
    if not user_profile.stripe_customer_id:
        customer = StripeAPI.create_customer(
            name=user_profile.user.get_full_name(),
            email=user_profile.user.email,
            phone=user_profile.phone_number
        )
        user_profile.stripe_customer_id = customer.get('id')
        user_profile.save()
        stripe_customer_id = customer.get('id')
    description = f"Course Payment for {datetime.datetime.now().strftime('%B %Y')}"

    while True:
        # payment_reference = payment_link = None
        succeeded, response = StripeAPI.create_payment_session(
            name=user_profile.user.get_full_name(),
            amount=amount,
            return_url=callback_url,
            # customer_id=stripe_customer_id,
        )
        if not succeeded:
            pass
        if not response.get('url'):
            pass
        payment_reference = response.get('payment_intent')
        if not payment_reference:
            payment_reference = response.get('id')
        payment_link = response.get('url')
        break

    # Create Transaction
    Transaction.objects.create(
        user=user_profile.user, amount=amount, detail=description, transaction_id=payment_reference
    )
    success = True
    return success, payment_link

