from app import app, db
from app.models import Record
from flask import render_template, request
from nslookup import Nslookup


@app.route("/", methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        domain = request.form.get('url')
        if domain is not None:
            dns = Nslookup()
            ips_record = dns.dns_lookup_all(domain)
            if ips_record.answer and Record.query.filter_by(url=domain).first() is None:
                db.session.add(Record(url=domain, IP=', '.join(ips_record.answer)))

        if request.form.get('del') is not None:
            to_be_deleted = Record.query.filter_by(url=request.form.get('del')).first()
            if to_be_deleted:
                db.session.delete(to_be_deleted)
        db.session.commit()

    ip_by_url = {record.url: record.IP for record in Record.query.all()}
    return render_template('hello.html', dict=ip_by_url, IP=', '.join(ip_by_url.values()))
