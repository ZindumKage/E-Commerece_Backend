import requests
from fastapi import HTTPException

from config.settings import settings


class FlutterwaveClient:
    BASE_URL = settings.FLUTTERWAVE_BASE_URL

    @staticmethod
    def initiate_payment(
        email: str,
        amount: float,
        tx_ref: str,
        currency: str = "NGN",
        redirect_url: str = ("http://localhost:3000/payment-success"),
    ):
        url = f"{FlutterwaveClient.BASE_URL}/payments"

        headers = {
            "Authorization": (f"Bearer " f"{settings.FLUTTERWAVE_SECRET_KEY}"),
            "Content-Type": "application/json",
        }

        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "redirect_url": redirect_url,
            "customer": {
                "email": email,
            },
            "customizations": {
                "title": "E-Commerce Payment",
                "description": (f"Payment for order {tx_ref}"),
            },
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        data = response.json()

        if data.get("status") != "success":
            raise HTTPException(
                status_code=400,
                detail="Failed to initialize payment",
            )

        return data

    @staticmethod
    def verify_payment(
        transaction_id: str,
    ):
        url = (
            f"{FlutterwaveClient.BASE_URL}" f"/transactions/" f"{transaction_id}/verify"
        )

        headers = {
            "Authorization": (f"Bearer " f"{settings.FLUTTERWAVE_SECRET_KEY}"),
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        data = response.json()

        if data.get("status") != "success":
            raise HTTPException(
                status_code=400,
                detail="Payment verification failed",
            )

        return data
