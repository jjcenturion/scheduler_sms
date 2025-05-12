import logging
from celeryconfig import app
from send_message import send_sms
from datetime import datetime
from pytz import timezone, UTC

logger = logging.getLogger(__name__)

@app.task(name="schedule_today_checkouts")
def schedule_today_checkouts():
    ## esta funcion es llamada automaticamente por el contenedor de Celery beat
    # y mediante el decorador ejecuta la configuracion de periodicidad del cron
    
    # Seccion de consulta a la BD###############
    # extrae diariamente todos los huespedes que correspondan hacer el checkout
    #today = datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")).date()
    #guests = db_query_checkout_today(today)  # <- reemplazá esto por tu consulta real 
    
    logger.warning(f"[CRON] ejecución del cron a las : {datetime.now()}")

    # Mock de guests
    guests = [
    {"phone_number": "+541112345678", "guest_name": "Juan", "checkout_date": "2025-05-09"},
    {"phone_number": "+541198765432", "guest_name": "Lucía", "checkout_date": "2025-05-09"},
    # ...
    ]

    for guest in guests:
        
        checkout_str = guest.get("checkout_date") 
        checkout_dt = datetime.strptime(checkout_str, "%Y-%m-%d")
        
        ba = timezone("America/Argentina/Buenos_Aires")
        ba_dt = ba.localize(checkout_dt.replace(hour=16, minute=45, second=0))

        # Convertir a UTC
        scheduled_time = ba_dt.astimezone(UTC)

        # Programar SMS
        send_checkout_sms.apply_async(
            args=[guest.get("phone_number"), guest.get("guest_name")],
            eta=scheduled_time
        )


@app.task
def send_checkout_sms(phone_number: str, guest_name: str):
    message = f"Hello {guest_name}, check out our late checkout options here: https://checkout.example.com"
    send_sms(phone_number, message)
    print(f"[{datetime.now()}] SMS sent to {phone_number}")