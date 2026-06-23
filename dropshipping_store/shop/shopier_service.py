import base64
import hmac
import hashlib
from django.conf import settings

class ShopierService:
    def __init__(self):
        self.api_key = settings.SHOPIER_API_KEY
        self.api_secret = settings.SHOPIER_API_SECRET
        self.platform_url = "https://www.shopier.com/ShowProduct/api_pay4.php"

    def generate_payment_form(self, order, total_amount, callback_url):
        # Shopier standart form parametreleri
        shopier_params = {
            'API_key': self.api_key,
            'website_index': 1,
            'platform_order_id': str(order.id),
            'product_name': f"Siparis #{order.id} Tahsilati",
            'product_type': 0,  # 0: Fiziksel Ürün
            'buyer_name': order.first_name,
            'buyer_surname': order.last_name,
            'buyer_email': order.email,
            'buyer_account_status': 1,
            'buyer_id_nr': "11111111111",
            'buyer_phone': "05555555555",
            'billing_address': order.address,
            'billing_city': order.city,
            'billing_country': "Turkiye",
            'billing_postcode': order.postal_code,
            'shipping_address': order.address,
            'shipping_city': order.city,
            'shipping_country': "Turkiye",
            'shipping_postcode': order.postal_code,
            'total_order_value': str(total_amount),
            'currency': "0",  # 0: TRY (String olarak tutuyoruz ki imzada hata olmasın)
            'current_language': 0,  # 0: TR
            'modul_version': "1.0.0",
            'random_nr': "987654"
        }

        # Dijital İmza (Signature) Hesaplanması
        data_to_sign = (
            shopier_params['random_nr'] + 
            shopier_params['platform_order_id'] + 
            shopier_params['total_order_value'] + 
            shopier_params['currency']
        )
        
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            data_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        shopier_params['signature'] = base64.b64encode(signature).decode('utf-8')
        shopier_params['callback_url'] = callback_url

        # Kullanıcıyı otomatik post ile Shopier'e yönlendiren HTML formu
        form_html = f'<form action="{self.platform_url}" method="post" id="shopier_form">'
        for key, value in shopier_params.items():
            form_html += f'<input type="hidden" name="{key}" value="{value}">'
        form_html += '</form><script>document.getElementById("shopier_form").submit();</script>'
        
        return form_html

    def verify_callback(self, post_data):
        platform_order_id = post_data.get('platform_order_id')
        random_nr = post_data.get('random_nr')
        status = post_data.get('status')
        signature_received = post_data.get('signature')

        if not platform_order_id or not random_nr:
            return False, None

        # Gelen verinin doğrulanması
        data_to_verify = random_nr + platform_order_id
        expected_signature = hmac.new(
            self.api_secret.encode('utf-8'),
            data_to_verify.encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_signature_b64 = base64.b64encode(expected_signature).decode('utf-8')

        if expected_signature_b64 == signature_received and status == "success":
            return True, platform_order_id
        return False, platform_order_id