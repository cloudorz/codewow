#!/usr/bin/env python
# coding: utf-8

from flask import Module, request, flash, abort, redirect, url_for, session
from codewow.ext import db

home = Module(__name__)

@home.route("/", methods=('GET',))
def index():
    return "hello world"
