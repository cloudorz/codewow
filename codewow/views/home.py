# coding: utf-8

import re

from flask import Module, request, flash, abort, redirect, url_for, session, render_template, g

from codewow.ext import db
from codewow.models import Gist

home = Module(__name__)

@home.route("/", methods=('GET',))
@home.route("/<int:p>", methods=('GET',))
def index(p=1):
    if p<1: p=1

    page_obj = Gist.query.descending(Gist.mongo_id).\
            paginate(page=p, per_page=Gist.PERN, error_out=False)
    page_url = lambda pn: url_for("home.index", p=pn)

    return render_template("index.html",
            page_obj=page_obj, 
            page_url=page_url)


@home.route("/<tag>/", methods=('GET',))
@home.route("/<tag>/<int:p>", methods=('GET',))
def tag(tag, p=1):
    if p<1: p=1

    page_obj = Gist.query.in_(Gist._tags, tag).\
            descending(Gist.mongo_id).\
            paginate(page=p, per_page=Gist.PERN, error_out=False)
    page_url = lambda pn: url_for("home.index", p=pn)

    return render_template("index.html",
            tag=tag,
            page_obj=page_obj, 
            page_url=page_url)


@home.route("/s", methods=('GET',))
def search():
    # TODO support other full text search
    q = request.args.get('q', "")
    p = int(request.args.get('p', 1))
    if p<1: p=1
    rqs = [e for e in re.split('\s+', q) if e]
    page_obj = Gist.query.in_(Gist._tags, *rqs).\
            descending(Gist.mongo_id).\
            paginate(page=p, per_page=Gist.PERN, error_out=False)
    page_url = lambda pn: url_for("home.index", p=pn)

    return render_template("index.html",
            page_obj=page_obj, 
            page_url=page_url,
            q=q,
            )
