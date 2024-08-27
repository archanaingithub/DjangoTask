import requests
import json
def get_khalti_payment_url(
    order_id,
    user,
    amount=100000
):
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://example.com/",
        "website_url": "https://example.com/",
        "amount": int(amount),
        "purchase_order_id": order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": self.full_name,
        "email": self.email,
        "phone": "9800000001"
        }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # if response.status_code == 200:
    #     return response.json()["payment_url"]
    # return response.json()

# def get_khalti_payment_status(pidx)

#     print(response.text)