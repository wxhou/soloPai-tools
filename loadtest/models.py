from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='项目名称')
    desc = models.CharField(max_length=256, verbose_name='项目描述')
    producter = models.CharField(max_length=64, verbose_name='负责人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '项目管理'


class SoloPitTag(models.Model):
    cn_name = models.CharField(verbose_name='中文名称', max_length=128)
    en_name = models.CharField(verbose_name='英文名称', max_length=128)
    csv_title = models.CharField(verbose_name='CSV标题', max_length=128)

    def __str__(self):
        return self.cn_name

    class Meta:
        verbose_name = verbose_name_plural = 'CSV标题'


class SoloPiFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='项目名称')
    filename = models.CharField(max_length=128, verbose_name='文件名称')
    filepath = models.CharField(max_length=512, verbose_name='文件路径')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = verbose_name_plural = '性能测试文件'