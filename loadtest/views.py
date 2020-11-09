import os
import sys
import csv
import time
import base64
from math import ceil
from io import BytesIO
from itertools import islice
import matplotlib.pyplot as plot

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
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
        paginator = Paginator(products,10)
        products_page = paginator.get_page(page)
        return render(request, 'loadtest/product.html', {'products_page':products_page})

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
        objects = SoloPiFile.objects.filter(product=product).order_by('-created_time')
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


class ChartView(View):
    """图表视图"""

    def solo_tags(self, name):
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

    def get(self, request, name):
        solo_tag = self.solo_tags(name)
        if not solo_tag:
            messages.error(request, "获取的文件数据是空的！")
            return render(request, 'loadtest/show.html', locals())

        try:
            title = solo_tag.csv_title
            cn_name = solo_tag.cn_name
        except AttributeError:
            messages.error(request, "获取字段值错误！{}".format(solo_tag))
        else:
            with open(name, 'r', encoding='GB2312') as f:
                csv_data = csv.reader(f)
                numbers = [float(number) for _, number, _ in islice(csv_data, 1, None)]
                max_number = ceil(max(numbers)) + 10
                min_number = ceil(min(numbers)) - 10 if (ceil(min(numbers)) - 10) < 0 else 0
                messages.warning(request, "最大值：%s，最小值：%s" % (max_number, min_number))
                messages.info(request, "X轴详细数据：%s" % numbers)
                # 设置字体
                if 'win' in sys.platform:
                    plot.rcParams['font.sans-serif'] = ['Songti SC']  # 用来正常显示中文标签
                else:
                    plot.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
                # 显示负数符号
                plot.rcParams['axes.unicode_minus'] = False
                # 设置图版
                plot.figure(dpi=128)
                plot.title(cn_name)
                # X，Y最大值
                plot.xlim((0, len(numbers)))  # X轴界限
                plot.ylim((min_number, max_number))  # Y轴界限
                # X，Y名称
                plot.xlabel('time axis')
                plot.ylabel(title)
                # 绘图
                plot.plot(range(len(numbers)), numbers, 'r', label=title)
                plot.legend()
                # 生成图片
                save_file = BytesIO()
                plot.savefig(save_file, format='png')
                save_file.seek(0)
                save_file_base64 = base64.b64encode(save_file.getvalue())
                plot.close()
                if save_file_base64:
                    img_str = "data:image/png;base64,%s" % save_file_base64.decode('utf-8')
                    return render(request, 'loadtest/show.html', {'img_str': img_str})
                else:
                    messages.error(request, "{}图片不存在！".format(cn_name))
                    return render(request, 'loadtest/show.html')
