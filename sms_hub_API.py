import requests

from config import HUB_API_TOKEN


API_Link = f"https://smshub.org/stubs/handler_api.php?api_key={HUB_API_TOKEN}"


def get_Ballance():
    res = requests.get(
        f"{API_Link}&action=getBalance")
    return res.text.replace('ACCESS_BALANCE:', '')


def get_phone(country):
    res = requests.get(
        f"{API_Link}&action=getNumber&service=fb&country={country}")
    return res.text


def chancel_phone(activateID):
    res = requests.get(
        f"{API_Link}&action=setStatus&status=8&id={activateID}")
    return res.text


def get_status(activateID):
    res = requests.get(
        f"{API_Link}&action=getStatus&id={activateID}")
    return res.text


def confirm_code(activateID):
    res = requests.get(
        f"{API_Link}&action=setStatus&status=6&id={activateID}")
    return res.text
