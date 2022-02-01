# import
from data_parse import parse_data, get_keys
import requests, re, json, csv, sys
from time import time
from web3.auto import w3
from pathvalidate import ValidationError, validate_filename
from collections import OrderedDict

# get and check user input for address
while True:
    coll_address = input("Enter Contract Address(REQUIRED):\n")
    try:
        coll_address = w3.toChecksumAddress(coll_address)
    except:
        sys.stdout.write("Not a valid address")
        continue
    ofile_name = input("Enter Outfile Name(OPTIONAL): \n") + ".csv"
    if re.sub('\W', '', ofile_name.split(".")[0]) == (None or ''):
        sys.stdout.write(re.sub('\W', '', ofile_name.split(".")[0]))
        ofile_name = "{}.csv".format(coll_address)
        break
    else:
        try:
            validate_filename(ofile_name)
            break
        except:
            sys.stdout.write("Invalid filename '{}'".format(ofile_name))
            continue
start = time()
url = "https://api.opensea.io/api/v1/assets"

to_csv = []
for i in range(0, 9999):
    params = {
        "token_ids": list(range((i * 30), (i * 30) + 30)),
        "asset_contract_address": coll_address,
        "order_direction": "desc",
        "offset": "0",
        "limit": "30"
    }
    res = requests.request("GET", url, params=params)
    if res.status_code != 200:
        sys.stdout.write('ERROR, RESPONSE CODE:')
        sys.stdout.write(str(res.status_code))
        break
    elif not len(res.json()['assets']) > 0:
        break
    else:
        [to_csv.append(parse_data(asset)) for asset in res.json()['assets']]
        sys.stdout.write(f'{i} ')
        sys.stdout.flush()

keys = get_keys(to_csv)
with open(ofile_name, 'w', newline='') as outfile:
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(to_csv)

# 0xef0182dc0574cd5874494a120750fd222fdb909a