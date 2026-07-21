import requests
from django.conf import settings
from django.urls import reverse
# ======================================================================================================================
# آدرس‌های API زرین‌پال بر اساس حالت sandbox/production
def get_zarinpal_urls():
    if settings.ZARINPAL_SANDBOX:
        return {
            "request": "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
            "verify": "https://sandbox.zarinpal.com/pg/v4/payment/verify.json",
            "startpay": "https://sandbox.zarinpal.com/pg/StartPay/",
        }
    return {
        "request": "https://api.zarinpal.com/pg/v4/payment/request.json",
        "verify": "https://api.zarinpal.com/pg/v4/payment/verify.json",
        "startpay": "https://www.zarinpal.com/pg/StartPay/",
    }
# ======================================================================================================================
# درخواست ایجاد تراکنش پرداخت به زرین‌پال
def zarinpal_request_payment(request, amount, description, mobile=None, email=None):
    urls = get_zarinpal_urls()
    callback_url = request.build_absolute_uri(reverse("payment:verify"))

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount * 10,  # تبدیل تومان به ریال (زرین‌پال ریال می‌گیره)
        "callback_url": callback_url,
        "description": description,
    }
    if mobile:
        data["metadata"] = {"mobile": mobile}
    if email:
        data.setdefault("metadata", {})["email"] = email

    try:
        response = requests.post(urls["request"], json=data, timeout=10)
        result = response.json()
    except requests.RequestException:
        return None, None

    data_result = result.get("data", {})
    if data_result and data_result.get("code") == 100:
        authority = data_result.get("authority")
        payment_url = urls["startpay"] + authority
        return authority, payment_url

    return None, None
# ======================================================================================================================
# تایید تراکنش پرداخت از زرین‌پال
def zarinpal_verify_payment(amount, authority):
    urls = get_zarinpal_urls()

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": amount * 10,  # تبدیل تومان به ریال
        "authority": authority,
    }

    try:
        response = requests.post(urls["verify"], json=data, timeout=10)
        result = response.json()
    except requests.RequestException:
        return False, None

    data_result = result.get("data", {})
    if data_result and data_result.get("code") in (100, 101):
        ref_id = data_result.get("ref_id")
        return True, ref_id

    return False, None
# ======================================================================================================================