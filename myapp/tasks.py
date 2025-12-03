from celery import shared_task
from django.core.cache import cache
import requests
from decimal import Decimal

@shared_task
def update_usd_rate():
    url = "https://www.nbrb.by/api/exrates/rates/USD?parammode=2"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data.get("Cur_OfficialRate")
        if rate:
            # Для точности используем Decimal
            cache.set("usd_rate", Decimal(rate), timeout=None)
            print(f"USD обновлён: {rate}")
        else:
            print("Ошибка: поле Cur_OfficialRate отсутствует в ответе")
    except Exception as e:
        print("Ошибка обновления курса:\n", e)



