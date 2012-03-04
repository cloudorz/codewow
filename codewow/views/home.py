# coding: utf-8

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
            page_obj=page_obj, 
            page_url=page_url)
