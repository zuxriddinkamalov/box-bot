import requests

import logging

from datetime import datetime
from client import telegram_models as models

logger = logging.getLogger()

async def create_order_billz(order: models.Order) -> None:
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJlY29tbWVyY2Utc2l0ZS51eiIsImlhdCI6MTY0MjkzNTMwMSwiZXhwIjoxODAwNzAxNzAxLCJzdWIiOiJhaXNoYWhvbWUuZWNvbW1lcmNldGdib3QifQ.RM2h-8d4KHJc_ellD2we7Ykr7qHqQ5x9L2Q45L3FHlQ"
    products = []
    for position in order.cart.positions.all():
        products.append(
            {
                "billzOfficeID": order.selected_branch.external_id,
                "billzProductID": position.product.external_id,
                "productID": position.product.id,
                "name": position.product.title,
                "sku": position.product.sku,
                "barCode": position.product.barcode,
                "qty": position.count,
                "subTotalPrice": position.get_price(),
                "discountAmount": 0,
                "totalPrice": position.get_price()
            }
        )
    content = {
        "jsonrpc": "2.0",
        "method": "orders.create",
        "params": {
            "orderID": 45,
            "dateCreated": f"{order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z",
            "datePaid": f"{order.paid_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z" if order.paysystem else f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z",
            "paymentMethod": order.paysystem.title if order.paysystem else 'Cash',
            "subTotalPrice": order.get_price(),
            "discountAmount": 0,
            "totalPrice": order.get_price(),
        "parked": False
        }
    }
    content["products"] = products
    logger.info(content)
    response = requests.post(
        "https://api.billz.uz/v1/",
        json=content,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    logger.info(response)
    logger.info(response.status_code)
    logger.info(response.content)

    