import os
import csv
from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint, render_template, flash, url_for, request, redirect
import pyecharts.options as opts
from pyecharts.charts import Line

from .models import db, Product, SoloPiFile
from .utils import allowed_file, pathname, to_pinyin

bp_solo = Blueprint('solo', __name__)



@bp_solo.route('/product/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        name = request.form.get('productname')
        desc = request.form.get('productdesc')
        if Product.query.filter_by(name=name).first():
            flash("该项目已存在！", "danger")
            return redirect(request.referrer)
        product = Product(name=name, desc=desc)
        db.session.add(product)
        db.session.commit()
        flash("项目【%s】添加成功！" % name, "success")
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PAGE_SIZE']
    pagination = Product.query.order_by(Product.created.desc()).paginate(
        page, per_page=per_page)
    products = pagination.items
    return render_template('index.html',
                           pagination=pagination,
                           products=products)


@bp_solo.route('/product/<int:id>/', methods=["GET", "POST"])
def detail(id):
    """项目详情"""
    if request.method == "POST":
        files = request.files.getlist('inputfile')
        if not files:
            flash("文件上传失败", "danger")
            return redirect(request.referrer)
        for file in files:
            realname = secure_filename(file.filename)
            if file and allowed_file(realname):
                thepathname, filename = pathname(), to_pinyin(realname)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                        thepathname)
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                file.save(os.path.join(filepath, filename))
                solo_file = SoloPiFile(filename=filename,
                                       filepath=thepathname,
                                       product_id=id)
                db.session.add(solo_file)
        db.session.commit()
        return redirect(url_for('.detail', id=id))

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PAGE_SIZE']
    product = Product.query.get(id)
    pagination = SoloPiFile.query.with_parent(product).order_by(
        SoloPiFile.created.desc()).paginate(page, per_page)
    solo_files = pagination.items
    return render_template('detail.html',
                           product=product,
                           pagination=pagination,
                           solo_files=solo_files)


@bp_solo.route('/show/<int:id>/')
def show(id):
    return render_template('show.html', id=id)


@bp_solo.route('/chart/<int:id>/')
def chart(id):
    solo_file = SoloPiFile.query.get(id)
    if not solo_file:
        flash("没有找到文件数据", "danger")
        return redirect(request.referrer)
    _file = os.path.join(current_app.config['UPLOAD_FOLDER'],
                         solo_file.filepath, solo_file.filename)
    if not os.path.isfile(_file):
        flash("文件路径不存在", "danger")
        return redirect(request.referrer)
    try:
        with open(_file, 'r', encoding='GB2312') as f:
            data = list(csv.reader(f))
            title = data.pop(0)[1]
            numbers = [float(i[1]) for i in data]
    except Exception as e:
        flash("获取文件数据错误:{}".format(e), "danger")
        return redirect(request.referrer)

    c = (Line().set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    ).add_xaxis(xaxis_data=range(len(numbers))).add_yaxis(
        series_name=title,
        y_axis=numbers,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    ))
    return c.dump_options_with_quotes()
