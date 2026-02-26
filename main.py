import json

from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Shared headers matching the browser request (cookies omitted; add if API requires them)
API_HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://classes.oregonstate.edu",
    "pragma": "no-cache",
    "referer": "https://classes.oregonstate.edu/",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

BASE_URL = "https://classes.oregonstate.edu/api"


def search(srcdb: str, crn: str):
    """Search for a class by term (srcdb) and CRN. Route: search."""
    url = f"{BASE_URL}/?page=fose&route=search&srcdb={srcdb}&crn={crn}"
    payload = {
        "other": {"srcdb": srcdb},
        "criteria": [
            {"field": "srcdb", "value": srcdb},
            {"field": "crn", "value": crn},
        ],
    }
    response = requests.post(url, headers=API_HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def get_details(crn: str, srcdb: str = "202603", group: str = "", dump_response: bool = False):
    """Get details for a class by CRN. Route: details."""
    url = f"{BASE_URL}/?page=fose&route=details"
    payload = {
        "key": f"crn:{crn}",
        "srcdb": srcdb,
        "group": group,
        "matched": "",
    }
    response = requests.post(url, headers=API_HEADERS, json=payload)
    response.raise_for_status()
    js = response.json()
    if dump_response:
        with open(f"response_crn_{crn}.json", "w", encoding="utf-8") as f:
            json.dump(js, f, indent=2, ensure_ascii=False)
    code = js.get("code")
    title = js.get("title")
    crn = js.get("crn") or ""
    section = js.get("section") or ""
    status = js.get("status") or ""
    campus = js.get("campus") or ""
    available = js.get("ssbsect_seats_avail")
    total = js.get("max_enroll")
    enrollment = js.get("enrollment")
    wait_count = js.get("ssbsect_wait_count")
    wait_cap = js.get("waitlist_capacity")
    wait_avail = js.get("ssbsect_wait_avail")
    available = int(available) if available is not None else 0
    total = int(total) if total is not None else 0
    wait_count = int(wait_count) if wait_count is not None else 0
    wait_cap = int(wait_cap) if wait_cap is not None else 0
    wait_avail = int(wait_avail) if wait_avail is not None else 0
    pct = f"({available * 100.0 / total:.2f}%)" if total != 0 else "NA"
    waitlist = f"{wait_count}/{wait_cap}" if wait_cap else "—"
    return {
        "code": code,
        "title": title,
        "crn": crn,
        "section": section,
        "status": status,
        "campus": campus,
        "seats": f"{available}/{total}",
        "seats_avail": available,
        "enrollment": enrollment or "",
        "max_enroll": total,
        "pct": pct,
        "waitlist_count": wait_count,
        "waitlist_capacity": wait_cap,
        "waitlist_avail": wait_avail,
        "waitlist": waitlist,
        "credits": js.get("hours_html") or "",
        "schedule_type": js.get("sche_type_clss_fild") or "",
        "inst_mthd": js.get("inst_mthd") or "",
        "grade_mode": js.get("grade_mode") or "",
        "session_html": js.get("session_html") or "",
        "meeting_html": js.get("meeting_html") or "",
        "instructordetail_html": js.get("instructordetail_html") or "",
        "description": js.get("description") or "",
        "attribute_description": js.get("attribute_description") or "",
        "registration_restrictions": js.get("registration_restrictions") or "",
    }


@app.route("/")
def root():
    crns = request.args.get("crn")
    if crns is None:
        return render_template("landing.html")
    dump = request.args.get("dump", "").lower() in ("1", "true", "yes")
    return render_template(
        "index.html",
        results=[get_details(c, dump_response=dump) for c in crns.split(",")],
    )


if __name__ == "__main__":
    # Example: search("202603", "56130") or get_details("56130", srcdb="202603")
    app.run()