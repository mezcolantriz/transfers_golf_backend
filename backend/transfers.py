from datetime import datetime, timedelta
from calculations import get_travel_time

def transfer_data(data, lang="en"):
    origen = data.get("origen")
    destino = data.get("destino")
    fecha = data.get("fecha")
    tee_time = data.get("tee_time")
    numero_pax = int(data.get("numero_pax", 4))
    
    # Ejemplo simplificado, añadir aquí tus lógicas específicas
    travel_time = get_travel_time(origen, destino)

    if tee_time:
        tee_datetime = datetime.strptime(f"{fecha} {tee_time}", "%Y-%m-%d %H:%M")
        salida = tee_datetime - timedelta(minutes=travel_time + 60)
        regreso = tee_datetime + timedelta(hours=5, minutes=15)

        if lang == "es":
            message = f"Salida: {salida.strftime('%H:%M')}, Regreso: {regreso.strftime('%H:%M')}"
        else:
            message = f"Departure: {salida.strftime('%H:%M')}, Return: {regreso.strftime('%H:%M')}"

        return {"message": message, "travel_minutes": travel_time}

    else:
        if lang == "es":
            return {"error": "Datos insuficientes para calcular tee time"}
        else:
            return {"error": "Insufficient data to calculate tee time"}
