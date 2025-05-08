from fastapi import FastAPI
from datetime import datetime, timedelta
from pytz import timezone, UTC
from tasks import send_checkout_sms

app = FastAPI()

@app.post("/schedule_sms/")
async def schedule_sms(phone_number: str, guest_name: str, checkout_date: str):
    # Parse checkout_date (formato esperado: YYYY-MM-DD)
    checkout_dt = datetime.strptime(checkout_date, "%Y-%m-%d")

    # Localizar en hora de Buenos Aires (UTC-3)
    ba = timezone("America/Argentina/Buenos_Aires")
    ba_dt = ba.localize(checkout_dt.replace(hour=16, minute=40, second=0))

    # Convertir a UTC
    scheduled_time = ba_dt.astimezone(UTC)

    # Programar SMS
    send_checkout_sms.apply_async(
        args=[phone_number, guest_name],
        eta=scheduled_time
    )

    return {"status": "scheduled", "scheduled_time": scheduled_time.isoformat()}
