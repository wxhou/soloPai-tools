import os
import csv
import time
from itertools import islice
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask import Blueprint, render_template, flash, url_for, request, redirect
from flask.views import MethodView
import pyecharts.options as opts
from pyecharts.charts import Line

from .models import Product, SoloPiTag, SoloPiFile
from .extensions import db

solo_bp = Blueprint('solo', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@solo_bp.route('/product', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        name = request.form.get('productname')
        desc = request.form.get('productdesc')
        if Product.query.filter_by(name=name).first():
            return redirect(request.referrer)
        product = Product(name=name, desc=desc)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']
    pagination = Product.query.order_by(
        Product.created.desc()).paginate(page, per_page=per_page)
    products = pagination.items
    return render_template('index.html', pagination=pagination, products=products)


@solo_bp.route('/product/<int:id>/', methods=["GET", "POST"])
def detail(id):
    """项目详情"""
    if request.method == "POST":
        files = request.files.getlist('inputfile')
        if not files:
            flash("文件上传失败")
            return redirect(request.referrer)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                        str(time.strftime("%Y%m%d%H%M%S",
                                                          time.localtime())))
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                file.save(os.path.join(filepath, filename))
                solo_file = SoloPiFile(
                    filename=filename, filepath=filepath, product_id=id)
                db.session.add(solo_file)
        db.session.commit()
        return redirect(url_for('.detail', id=id))

    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']
    product = Product.query.get(id)
    pagination = SoloPiFile.query.with_parent(product).order_by(
        SoloPiFile.created.desc()).paginate(page, per_page)
    solo_files = pagination.items
    return render_template('detail.html', product=product, pagination=pagination, solo_files=solo_files)


@solo_bp.route('/show/<int:id>/')
def show(id):
    return render_template('show.html', id=id)


@solo_bp.route('/chart/<int:id>/')
def chart(id):
    solo_file = SoloPiFile.query.get(id)
    tag = SoloPiTag.query.filter(
        SoloPiTag.en_name.in_(solo_file.filename)).first()
    if not tag:
        title = "default"
    else:
        title = tag.csv_title
    if not solo_file:
        flash("没有对应的文件数据")
        return redirect(request.referrer)
    _file = os.path.join(solo_file.filepath, solo_file.filename)
    try:
        with open(_file, 'r', encoding='GB2312') as f:
            data = csv.reader(f)
            app.logger.warning(list(data))
            numbers = [float(i[1]) for i in islice(data, 1)]
    except AttributeError:
        flash("获取文件数据错误")
        return redirect(request.referrer)
    c = (
        Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    return c.dump_options_with_quotes()
