import os
import csv
import time
from itertools import islice

from django.shortcuts import render, redirect, reverse, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages
from django.conf import settings

from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader('./templates'))
import pyecharts.options as opts
from pyecharts.charts import Line
from loadtest.models import SoloPitTag, SoloPiFile, Product


# Create your views here.
def add_tag(request):
    data = SoloPitTag.objects.all()
    if data:
        messages.warning(request, "csv Tag数据已存在！")
        return redirect(reverse('loadtest:product'))
    data = [SoloPitTag(cn_name=key, en_name=value, csv_title=settings.CSV_TITLE_EN[value])
            for key, value in settings.CSV_TITLE_CN.items()]
    SoloPitTag.objects.bulk_create(data)
    messages.success(request, "csv Tag数据已创建！")
    return redirect(reverse('loadtest:product'))


class ProductView(View):
    """项目视图"""

    def get(self, request):
        page = request.GET.get('page')
        products = Product.objects.all().order_by('-created_time')
        paginator = Paginator(products, 10)
        products_page = paginator.get_page(page)
        return render(request, 'loadtest/product.html', {'products_page': products_page})

    def post(self, request):
        productname = request.POST.get('productname')
        productdesc = request.POST.get('productdesc')
        try:
            Product.objects.get(name=productname)
            messages.warning(request, "项目名称已存在！")
        except Product.DoesNotExist:
            Product.objects.create(name=productname,
                                   producter=request.user,
                                   desc=productdesc)
            messages.success(request, "添加项目成功！")
        return redirect(reverse('loadtest:product'))

    def put(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        product.objects.update(*args, **kwargs)
        messages.info(request, "项目%s更新成功" % product.name)
        product.save()
        return redirect(reverse('loadtest:product'))

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        messages.warning(request, "项目%s删除成功" % product.name)
        return redirect(reverse('loadtest:product'))


class IndexView(View):
    """首页类视图"""

    def get(self, request, pk):
        page = request.GET.get('page')
        product = Product.objects.get(pk=pk)
        objects = SoloPiFile.objects.filter(
            product=product).order_by('-created_time')
        paginator = Paginator(objects, 10)
        all_path = paginator.get_page(page)
        return render(request, 'loadtest/index.html', locals())

    def post(self, request, pk):
        files = request.FILES.getlist('inputfile', None)
        if not files:
            messages.error(request, '文件上传失败！')
            return redirect(reverse('loadtest:index', args=(pk,)))
        filepath = os.path.join(settings.MEDIA_ROOT,
                                str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
        os.makedirs(filepath)
        for file in files:
            _path = os.path.join(filepath, file.name)
            with open(_path, 'wb+') as fp:
                for chunk in file.chunks():
                    fp.write(chunk)
            product = Product.objects.get(pk=pk)
            SoloPiFile.objects.create(product=product,
                                      filename=file.name,
                                      filepath=os.path.join(filepath, file.name))
        messages.info(request, "文件全部上传成功！")
        return redirect(reverse('loadtest:index', args=(pk,)))


def solo_tags(name):
    name = name[name.rfind('/') + 1:]
    new_name = []
    for i in name.split('_'):
        new_name += i.split('-')
    solo_tag = SoloPitTag.objects.filter(cn_name__contains=new_name[0])
    if len(solo_tag) == 1:
        return solo_tag.first()
    else:
        solo_tag2 = solo_tag.filter(cn_name__contains=new_name[1])
        return solo_tag2.first()


def chart(request, name):
    solo_tag = solo_tags(name)
    if not solo_tag:
        messages.error(request, "获取的文件数据是空的！")
        return render(request, 'loadtest/shows.html')
    try:
        title = solo_tag.csv_title
        cn_name = solo_tag.cn_name
        with open(name, 'r', encoding='GB2312') as f:
            csv_data = csv.reader(f)
            numbers = [float(number)
                       for _, number, _ in islice(csv_data, 1, None)]
    except AttributeError:
        messages.error(request, "获取字段值错误！{}".format(solo_tag))
        return render(request, 'loadtest/shows.html')
    c = (
        Line()
            .set_global_opts(
            title_opts=opts.TitleOpts(title=cn_name),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(xaxis_data=range(len(numbers)))
            .add_yaxis(
            series_name=title,
            y_axis=numbers,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    return HttpResponse(c.render_embed())


def shows(request, name):
    return render(request, 'loadtest/shows.html', {'name': name})
