# coding: utf-8

from flask import Module, request, flash, abort, redirect, url_for, session, render_template, g

from codewow.ext import db
from codewow.models import Gist

home = Module(__name__)

@home.route("/", methods=('GET',))
@home.route("/<int:page>", methods=('GET',))
def index(page=1):
    if page<1: page=1

    page_obj = Gist.query.descending(Gist.mongo_id).paginate(page=page, per_page=20, error_out=False)
    page_url = lambda p: url_for("home.index", page=p)

    return render_template("index.html",
            page_obj=page_obj, 
            page_url=page_url)
