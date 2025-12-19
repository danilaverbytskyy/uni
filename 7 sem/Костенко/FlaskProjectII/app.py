from __future__ import annotations
import os
from flask import Flask, render_template, request
from rdflib import URIRef
from ontology_utils import CleaningKB, CLEAN

APP_DIR = os.path.dirname(os.path.abspath(__file__))
OWL_PATH = os.path.join(APP_DIR, "data", "cleaning.owl")

app = Flask(__name__)
kb = CleaningKB(OWL_PATH)

def _uri(u: str) -> URIRef:
    return URIRef(u)

def _all_tasklists_cards(match_uris=None):
    match_uris = set(match_uris or [])
    all_tls = kb.get_tasklists()
    matches = [(u, n) for (u, n) in all_tls if u in match_uris]
    non_matches = [(u, n) for (u, n) in all_tls if u not in match_uris]

    matches.sort(key=lambda x: x[1])
    non_matches.sort(key=lambda x: x[1])

    cards = []
    for uri, name in matches + non_matches:
        cards.append({
            "uri": uri,
            "name": name,
            "is_match": uri in match_uris
        })
    return cards


@app.get("/")
def index():
    return render_template(
        "index.html",
        zone_lists=kb.get_zone_lists(),
        tasklists=kb.get_tasklists(),
        traffic=kb.get_traffic()
    )

@app.post("/recommend")
def recommend():
    zone_list_uri = request.form.get("zone_list")
    mode = request.form.get("mode", "auto")
    explicit_tasklist_uri = request.form.get("tasklist")
    traffic_uri = request.form.get("traffic")

    add_emergency = request.form.get("add_emergency") == "on"
    add_windows = request.form.get("add_windows") == "on"
    add_deep = request.form.get("add_deep") == "on"

    chosen = []
    if mode == "explicit" and explicit_tasklist_uri:
        chosen.append(_uri(explicit_tasklist_uri))
    elif zone_list_uri:
        chosen.extend(kb.tasklists_by_zone_list(_uri(zone_list_uri)))

    if add_emergency:
        chosen.append(CLEAN.ex_tasklist_emergency_spill)
    if add_windows:
        chosen.append(CLEAN.ex_tasklist_weekly_windows)
    if add_deep:
        chosen.append(CLEAN.ex_tasklist_deep_cleaning)

    seen=set()
    chosen2=[]
    for x in chosen:
        if str(x) not in seen:
            chosen2.append(x)
            seen.add(str(x))
    chosen = chosen2

    recs = []
    for tl in chosen:
        tasks = kb.tasks_for_tasklist(tl)
        p, sch, res_pack = kb.find_planning_for_tasklist(tl)
        recs.append({
            "package": kb.label(tl),
            "tasks": [{"type": t.task_type, "label": t.label} for t in tasks],
            "planning": kb.label(p) if p else None,
            "schedule": kb.label(sch) if sch else None,
            "resources_pack": kb.label(res_pack) if res_pack else None,
            "resources_items": kb.resource_items(res_pack) if res_pack else []
        })

    safety = kb.recommend_safety(chosen)
    traffic_label = kb.label(_uri(traffic_uri)) if traffic_uri else None
    notes=[]
    if traffic_label and ("пиков" in traffic_label.lower() or "высок" in traffic_label.lower()):
        notes.append("Высокий/пиковый поток людей: рекомендуем увеличить частоту уборки входной зоны и санузлов.")
    if not recs:
        notes.append("Не удалось подобрать пакет по выбранным параметрам. Выберите зону или пакет вручную.")

    return render_template("result.html", recommendations=recs, safety=safety, traffic=traffic_label, notes=notes)

@app.get("/packages")
def packages():
    items=[]
    for uri, _ in kb.get_tasklists():
        tl=_uri(uri)
        tasks = kb.tasks_for_tasklist(tl)
        items.append({
            "name": kb.label(tl),
            "tasks": [f"{t.task_type}: {t.label}" for t in tasks]
        })
    return render_template("packages.html", items=items)


@app.route("/filter/1-zone", methods=["GET", "POST"])
def filter1_zone():
    zone_lists = kb.get_zone_lists()
    selected = ""
    submitted = False
    match_uris = []
    if request.method == "POST":
        submitted = True
        selected = request.form.get("zone_list") or ""
        if selected:
            match_uris = [str(u) for u in kb.tasklists_by_zone_list(_uri(selected))]
    cards = _all_tasklists_cards(match_uris) if submitted else []
    return render_template("filter1_zone.html", zone_lists=zone_lists, selected=selected, submitted=submitted, cards=cards)

@app.route("/filter/2-tasktypes", methods=["GET", "POST"])
def filter2_tasktypes():
    submitted = False
    want_dry = want_wet = want_dis = False
    mode = "all"
    match_uris = []
    if request.method == "POST":
        submitted = True
        want_dry = request.form.get("want_dry") == "on"
        want_wet = request.form.get("want_wet") == "on"
        want_dis = request.form.get("want_dis") == "on"
        mode = request.form.get("mode", "all")
        tls = kb.tasklists_with_task_types(want_dry, want_wet, want_dis, require_all=(mode=="all"))
        match_uris = [str(u) for u in tls]
    cards = _all_tasklists_cards(match_uris) if submitted else []
    return render_template("filter2_tasktypes.html",
                           submitted=submitted, want_dry=want_dry, want_wet=want_wet, want_dis=want_dis,
                           mode=mode, cards=cards)

@app.route("/filter/3-schedule", methods=["GET", "POST"])
def filter3_schedule():
    submitted = False
    schedule_keyword = ""
    match_uris = []
    if request.method == "POST":
        submitted = True
        schedule_keyword = (request.form.get("schedule_keyword") or "").strip()
        tls = kb.tasklists_with_schedule(schedule_keyword)
        match_uris = [str(u) for u in tls]
    cards = _all_tasklists_cards(match_uris) if submitted else []
    return render_template("filter3_schedule.html", submitted=submitted, schedule_keyword=schedule_keyword, cards=cards)

@app.route("/filter/4-resources", methods=["GET", "POST"])
def filter4_resources():
    submitted = False
    resource_category = ""
    must_have = "yes"
    match_uris = []
    if request.method == "POST":
        submitted = True
        resource_category = request.form.get("resource_category") or ""
        must_have = request.form.get("must_have", "yes")
        cls = None
        if resource_category == "Chemicals":
            cls = CLEAN.Chemicals
        elif resource_category == "Equipment":
            cls = CLEAN.Equipment
        elif resource_category == "Staff":
            cls = CLEAN.Staff
        if cls:
            tls = kb.tasklists_by_resource_category(cls, must_have=(must_have == "yes"))
            match_uris = [str(u) for u in tls]
    cards = _all_tasklists_cards(match_uris) if submitted else []
    return render_template("filter4_resources.html",
                           submitted=submitted, resource_category=resource_category, must_have=must_have, cards=cards)


@app.route("/filter/5-diverse", methods=["GET", "POST"])
def filter5_diverse():
    submitted = False
    keyword = ""
    match_uris = []
    if request.method == "POST":
        submitted = True
        keyword = (request.form.get("keyword") or "").strip()
        tls = kb.tasklists_by_tasklist_label_keyword(keyword) if keyword else []
        match_uris = [str(u) for u in tls]
    cards = _all_tasklists_cards(match_uris) if submitted else []
    return render_template("filter5_diverse.html", submitted=submitted, keyword=keyword, cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
