import requests

from home.models import Transaction
from home.stripe_api import StripeAPI


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
