from flask import Blueprint, render_template

faq_bp = Blueprint('faq', __name__, url_prefix='/faq')

@faq_bp.route('/')
def faq():
    return render_template('other/faq.html')