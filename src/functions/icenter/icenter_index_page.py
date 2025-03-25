"""
Icenter主页
"""
from flask import render_template


def icenter_index():
    return render_template("icenter/icenter_login.html")