import json

from flask import Flask, request, render_template
import requests

app = Flask(__name__)


def get_details(crn):
    payload = {"key": f"crn:{crn}"}
    print(payload)
    url = "https://classes.oregonstate.edu/api/?page=fose&route=details"

    response = requests.request("POST", url, data=json.dumps(payload))

    js = response.json()
    code = js.get('code')
    title = js.get('title')
    available = js.get("ssbsect_seats_avail")
    total = js.get("max_enroll")
    available = int(available) if available is not None else 0
    total = int(total) if total is not None else 0

    return code, title, f'{available}/{total}', '(%.2f%%)' % (available * 100.0 / total) if total != 0 else "NA"


@app.route('/')
def root():
    crns = request.args.get('crn')
    if crns is None:
        return 'Please include crns in this format. url?crn=123,423,543'

    return render_template('index.html', results=[get_details(crn) for crn in crns.split(',')])


if __name__ == '__main__':
    app.run()
