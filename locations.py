import random

COUNTRIES = [
"United States",
"England"
]

# these are real but arbitrary addresses within countries
ADDRESSES = {
    "United States": [
        {"street": "1000 5th Ave", "city":"New York", "state":"New York", "postal":"10028"},
        {"street": "81 Central Park West", "city":"New York", "state":"New York", "postal":"10023"}
    ],
    "England": [
        {"street":"372 Strand", "city":"London", "state":"Strand", "postal":"WC2R 0JJ"}
    ]
}


def random_address():
    """ returns street address, state/province, country, postal code """
    country = COUNTRIES[random.randint(0, len(COUNTRIES) - 1)]
    addresses = ADDRESSES[country]
    # randomly grab an address
    address = addresses[random.randint(0, len(addresses) - 1)]
    return address["street"], address["city"], address["state"], country, address["postal"]
