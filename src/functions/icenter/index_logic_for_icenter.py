from flask import render_template


def return_icenter_index_templates():
    return render_template('icenter/icenter_index.html')

def return_icenter_execute_sql_templates():
    return render_template('icenter/icenter_sql_execution.html')

def return_icenter_editor():
    return render_template('icenter/icenter_editor.html')