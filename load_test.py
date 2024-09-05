import requests


def run():
    valid_sample = {
        "matching_from": {
            "unique_id": "1",
            "firstname1": "Lily",
            "lastname": "Robinson",
            "dob": "2009-07-06",
            "pnc": "2001/0141640Y",
        },
        "matching_to": [
            {
                "unique_id": "2",
                "firstname1": "Lily",
                "lastname": "Robibnson",
                "dob": "2009-07-06",
                "pnc": "2001/0141640Y",
            },
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    for _ in range(1000):
        response = requests.post("http://127.0.0.1:5000/person/match", headers=headers, json=valid_sample)
        print(response.status_code)

if __name__ == "__main__":
    run()
