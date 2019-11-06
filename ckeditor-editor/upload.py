# -*- coding: utf-8 -*-
from flask import Blueprint
import os,re,json,random,urllib,datetime
from flask import Flask, request, render_template, url_for, make_response
from application import app

route_ckupload = Blueprint('ckupload',__name__)
@route_ckupload.route("/",methods=['GET','POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname = fileobj.filename
        rnd_name = str("".join(random.sample('123456789zyxwvutsrqponmlkjihgfedcba', 10))) + "." + \
                       fname.split(".")[-1]

        filepath = os.path.join(app.static_folder, 'upload' ,'img', str(datetime.datetime.now().strftime("%Y-%m-%d")), rnd_name)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        print(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s%s%s%s%s' % ('upload','img' ,'/', str(datetime.datetime.now().strftime("%Y-%m-%d")),'/', rnd_name))
            print(url)
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response