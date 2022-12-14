import requests
import config
import math
import json

def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid):
    return {"error": error, "id": rid, "result": result}

def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()

def reward(height):
    halvings = height // 525960

    if halvings >= 10:
        return 0

    return int(satoshis(4) // (2 ** halvings))

def supply(height):
    reward = satoshis(4)
    halvings = 525960
    halvings_count = 0
    supply = reward

    while height > halvings:
        total = halvings * reward
        reward = reward / 2
        height = height - halvings
        halvings_count += 1

        supply += total

    supply = supply + height * reward

    return {
        "halvings": int(halvings_count),
        "supply": int(supply)
    }

def satoshis(value):
    return int(float(value) * math.pow(10, 8))

def amount(value, decimals=8):
    return round(float(value) / math.pow(10, decimals), decimals)
