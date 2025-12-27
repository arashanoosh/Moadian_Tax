import requests
import json
import base64
import jwt
from datetime import datetime, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

url = "https://tp.tax.gov.ir/requestsmanager/api/v2/nonce"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    Nonce = data["nonce"]
    ExpDate = data["expDate"]
    print("Nonce: ", Nonce )

else:
    print("Error cannot Get Nonce:", response.status_code)

clientid=123123234
now_utc = datetime.now(timezone.utc)
sig_t = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
x5c = [
"MIIDejCCAmKgAwIBAgIUV27QXqJjK2EgFy9zeYkpsX+ISPswDQYJKoZIhvcNAQELBQAwcTELMAkGA1UEBhMCSVIxDDAKBgNVBAgMA1RlaDEMMAoGA1UEBwwDVGVoMREwDwYDVQQKDAhNb2hheW1lbjEMMAoGA1UECwwDVGF4MSUwIwYJKoZIhvcNAQkBFhZtLm1hbHZlcmRpQG1vaGF5bWVuLmlyMB4XDTIzMDMyNDEzMjgyM1oXDTI0MDMyMzEzMjgyM1owTTEPMA0GA1UEAwwGQW56YWxpMRcwFQYDVQQKDA5RdW9WYWRpcyBHcm91cDELMAkGA1UEBhMCSVIxFDASBgNVBAUTCzE0MDAzNzc4OTkwMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzLgyk5KO6+j9d1ud0ilJArrZ3Whw/w9wEzHB9yXwENRa5fm5AbRukMF5b6VGeKzD6LZuL9+tfdFfWyPcjI++gGNywzRmEHKpTnzP1t6NyuXKfm4nBVAblsugSw8Y5DEXRfTqILgBWN/pZ4zGlifEALMcGAs7ADcjnv7b/tM2wxr9rHxsCvW4HvlzQasK8Qr1CrKgT0EI66rSXCHep/uIONDWp0W2OelMlZtM6AAjWXRLGcshPIHuK+ZLfAFxWtoGonf6qN9ypos2B18D/EFa8WHON62eYKT0kW3jBVa3yPEkRwkdDjDu/3CPzymhf3WFYwxpb4t35oWb/qUXGVIdvwIDAQABoy4wLDAfBgNVHSMEGDAWgBSx+Oq+RO3x/FmyCp+jcmfOH+Fn9TAJBgNVHRMEAjAAMA0GCSqGSIb3DQEBCwUAA4IBAQAgKATXlnS+pPtAiRIYGtydVU5Vi7Aq+D6QW07uFqcB7vBhddN3yX2lVVcwpTNJzhv8UCM+mDMvlmsRVKVtMoo5fHfII92/Wo8rUz1RP+yhyCk0Vz8I11v+bjLwVur/agC/s5Rf0m66pNNjFZ9J3S2N3lChXYwz2vvA8pdAYvWTu9g5u4FMFqlsaLwMGC+WaA0g3KYzRkdWRy1vd23hLTUcVsWM8wpgZ11wEGE1khca/Sd0mCU2HG5vIbqFfTjA6to0fY07CE5fD8aR3UcXjNduosVO52ZqCX5SabrhFS3AGHFRjpFnI5LZespiCXSA8Sv3kOSCSRQKqFbiwSFM8Zjg"
]
PRIVATEKEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMuDKTko7r6P13W53SKUkCutndaHD/D3ATMcH3JfAQ1Frl+bkBtG6QwXlvpUZ4rMPotm4v36190V9bI9yMj76AY3LDNGYQcqlOfM/W3o3K5cp+bicFUBuWy6BLDxjkMRdF9OoguAFY3+lnjMaWJ8QAsxwYCzsANyOe/tv+0zbDGv2sfGwK9bge+XNBqwrxCvUKsqBPQQjrqtJcId6n+4g40NanRbY56UyVm0zoACNZdEsZyyE8ge4r5kt8AXFa2gaid/qo33KmizYHXwP8QVrxYc43rZ5gpPSRbeMFVrfI8SRHCR0OMO7/cI/PKaF/dYVjDGlvi3fmhZv+pRcZUh2/AgMBAAECggEACPpC7YnNzram9ucDosXAt+ftyfHckrLgnVbfRLFbN8G4QsGSxWpeNublJmo/Due0p63oYx0SBKR75AlMkLV1CzhRPhI8L5h3qEN88dVMrospOCYoe+kpbJF9dA0zcD5e4Oh+o/StynH3UF0yED+qLsWsA7nqWnYQj9ZpW2Fz01Z1i5NRX4YgyIopHfqcLWJWpOR8n4HwDY18BL7tMi31f0sZXz56EUgBPxq5RMi+1iKWpyZdwy4TrJL/Sj4tWkKJ7ELVd47VunizAqeLDy8bLlPBX0PewRvR37P9axHLjsj/d1Iw/xvqgVEWZTyUXzg4qgFU5Na5u6xIW8JyqejdEQKBgQD2QlDdoPOtG1URyuuo4HJlQ85ZfEWWA0vvp8esvJLJ7t73Rz28RkKAMHW/njr23ExxV3eek9J1lGENJUZFKsNNtjRWMgCxUicO0MGTJuraWHrEma00YNNjpVd3pIi68p51CZNzMRLn2J8F+7CPeGiynKEvKU43KcJr6KOkWP14FQKBgQDU0T3SNr7af4y3rO3ds2DMaoKEG531tuLunrZNnL4a/i2r3AlI5K470UkmAXDD1kgGf235KxrRm7x7VVp5SZLgOPqgJ2OKKk9bHLvuAdxCeUlnDfJWrAmYcmyLLCSDHBudN/evF6WiNaQi074MhdbaxYdLiiXdS3VVflQ/8m6/gwKBgD4ijXTeX52V/+j1YnDB8RtL+IzrpkMrocVeeCtFiWQaOXf7KcCPmcfuckdfDVGsVD1k7HG+qqOwRKykcw6Qs6awCpSVGUekiuZaFf2jHC7rlE522BUXOT8zQNaXVUiWXxT4zZOLFlIZfkZsMyiAISqwCptzuKCCkOPZVzDoo0vhAoGBAMo82XnVyoKLKWc2r4i6OOeo48S1FeP12yuVqXqR1FqEZ1RlMnGR1z1DAjdasRV5oVKDcDeTzdWZIIE3uFWAJFJt80WUiNQ4ptbXtINWQ0DsT2PebggNTsUPH7UVytDJOjiqgfZjC2TdgtAR1g3Cdk3J3mtbqeXlGmiXN2rZcIMPAoGADfTonaehrsnscUcH4DgsqZdyZm9JRmoNyisLBmbGkTNxoYO9Vm/03u3NMsohkjopt2ly38ZMYXl4FyXKEKcI977r33JD9PxRcovqFhcPR3WuQrPf6ND3IX6eB5p8d7m6fmFYSe/0NhWoeH99a6/ccsAr2hPMOb/R3GdRewkSGgQ=
-----END PRIVATE KEY-----"""

#def base64url_encode(data: bytes) -> str:
   # return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')


Header = {
    "alg" : "RS256",
    "x5c" : x5c,
    "sigT": sig_t,
    "crit":["sigT"]
}

#header_bytes = json.dumps(Header, separators=(',', ':')).encode('utf-8')
#encoded_header = base64url_encode(header_bytes)

peyload = {
    "nonce":Nonce,
    "Clinetid":clientid
}


token = jwt.encode(
    payload=peyload,
    key=PRIVATEKEY,
    algorithm="RS256",
    headers=Header
)

print("JWS Token:")
print(token)

#peyload_bytes = json.dumps(Header, separators=(',', ':')).encode('utf-8')
#encoded_peydload = base64url_encode(peyload_bytes)

#signing_input = f"{encoded_header}.{encoded_payload}"


print(sig_t)


url_info=  "https://tp.tax.gov.ir/requestsmanager/api/v2/server-information"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(response.text)