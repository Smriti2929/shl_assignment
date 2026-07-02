import json
import pprint

CATALOG_PATH = "data/shl_product_catalog.json"

with open (
    CATALOG_PATH, 
    "r",
    encoding = "utf-8"
) as f: 
    data = json.load(f)

    print("\nTYPE:")
    print(type(data))

    print("\nTOTAL RECORDS:")
    print(len(data))

    print("\nFIRST RECORD KEYS:")
    print(data[0].keys())

    print("\nFIRST RECORD:")
    pprint.pprint(data[0])

    print("\nFIELD SUMMARY\n")

    for key in data[0].keys():
        missing = 0

        for item in data:
            value = item.get(key)

            if value is None:
                missing += 1

            elif value == "":
                missing += 1

    print (
        f"{key}: "
        f"{missing}/{len(data)} missing"
    )   

    print("\nSAMPLE RECORDS\n")

    for i in range(5):
        print("=" * 80)
        pprint.pprint(data[i])             

