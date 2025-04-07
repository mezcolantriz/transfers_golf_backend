import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")
ORS_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"

with open('locations.json', 'r', encoding='utf-8') as file:
    locations = json.load(file)

def get_travel_time(origen, destino):
    if origen not in locations or destino not in locations:
        return 0

    coords = {
        "locations": [
            [locations[origen]["lng"], locations[origen]["lat"]],
            [locations[destino]["lng"], locations[destino]["lat"]]
        ],
        "metrics": ["duration"]
    }

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(ORS_URL, json=coords, headers=headers)

    if response.status_code == 200:
        tiempo_segundos = response.json()["durations"][0][1]
        return round(tiempo_segundos / 60)
    else:
        return 0

def calculate_full_transfer(data):
    origen = data["origen"]
    destino = data["destino"]
    fecha = data["fecha"]
    tee_time = data.get("tee_time")
    numero_pax = int(data.get("numero_pax", 4))

    travel_time = get_travel_time(origen, destino)

    if travel_time == 0:
        return {"error": "Travel time unavailable"}

    result = {
        "fecha": fecha,
        "origen": origen,
        "destino": destino,
        "travel_minutes": travel_time,
        "numero_pax": numero_pax
    }

    airports = ["Alicante Airport", "Murcia Airport"]

    if destino in airports:
        flight_time = datetime.strptime(f"{fecha} {tee_time}", "%Y-%m-%d %H:%M")
        salida = flight_time - timedelta(minutes=(travel_time + 120))  # 2 horas antes si destino aeropuerto
        result.update({
            "salida": salida.strftime("%H:%M"),
            "flight_time": tee_time,
            "tipo": "departure"
        })
    elif origen in airports:
        result.update({
            "arrival_time": tee_time,
            "tipo": "arrival"
        })
    else:
        tee_datetime = datetime.strptime(f"{fecha} {tee_time}", "%Y-%m-%d %H:%M")
        salida = tee_datetime - timedelta(minutes=(travel_time + 60))
        base_duracion = timedelta(hours=5, minutes=15)
        bloques_adicionales = (numero_pax - 1) // 4
        extra = timedelta(minutes=10 * bloques_adicionales)
        regreso = tee_datetime + base_duracion + extra

        result.update({
            "salida": salida.strftime("%H:%M"),
            "regreso": regreso.strftime("%H:%M"),
            "tee_time": tee_time,
            "tipo": "golf"
        })

    return result
