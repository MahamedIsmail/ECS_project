import os
from flask import Flask, render_template, request, redirect, url_for, flash
from Getcerts import socket_connection
from Store_data import store_data, list_data, delet_data, status_of
from validator import clean_domain, resolve_public_ip, InvalidDomain

app = Flask(__name__)
app.json.sort_keys = False
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


@app.get("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.get("/dashboard")
def dashboard():
    items = [dict(item, status=status_of(item)) for item in list_data()]
    summary = {
        "total": len(items),
        "ok": sum(1 for i in items if i["status"] == "ok"),
        "warning": sum(1 for i in items if i["status"] == "warning"),
        "critical": sum(1 for i in items if i["status"] == "critical"),
        "failed": sum(1 for i in items if i["status"] == "failed"),
    }
    return render_template("dashboard.html", items=items, summary=summary)


@app.post("/submit")
def submit():
    raw = request.form.get("domain", "")
    try:
        domain = clean_domain(raw)
        ip = resolve_public_ip(domain)
    except InvalidDomain as err:
        flash(f"{raw or 'Empty input'}: {err}", "error")
        return redirect(url_for("dashboard"))

    store_data(socket_connection(domain, ip))
    flash(f"Checked {domain}", "success")
    return redirect(url_for("dashboard"))


@app.post("/DB/<item_id>/delete")
def delete_item(item_id):
    removed = delet_data(item_id)
    if removed is None:
        flash("Item not found", "error")
    else:
        flash(f"Deleted {removed['domain']}", "success")
    return redirect(url_for("dashboard"))


@app.get("/DB")
def Display_DB():
    return list_data()


@app.get("/Health")
def health_check():
    return {"status": "ok"}