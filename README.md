# OSU Class Watch

Live enrollment and waitlist for Oregon State classes. Enter CRNs, see seats and waitlist.

**Try it live:** [osuclass.bikcrum.com](https://osuclass.bikcrum.com)

## Run locally

```bash
git clone git@github.com:bikcrum/OSU-class-waitlist-count.git
cd OSU-class-waitlist-count
pip install -r requirements.txt
python main.py
```

Open **http://127.0.0.1:5000** — use `?crn=56130` or `?crn=56130,12345` with real CRNs from [classes.oregonstate.edu](https://classes.oregonstate.edu).

---

By [Bikram](https://bikcrum.com).
