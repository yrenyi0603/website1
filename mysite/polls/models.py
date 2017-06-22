from django.db import models
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from field_history.tracker import FieldHistoryTracker
# Create your models here.
import reversion
from  reversion.signals import pre_revision_commit,post_revision_commit
@reversion.register(follow=['department_staff'])
class Department(models.Model):
    name=models.CharField(max_length=100,verbose_name=u'部门')
    email=models.EmailField(blank=True,null=True,verbose_name=u'部门邮箱')
    def colored_name(self):
        return format_html('<span style="color: #FF0000;">{}</span>', self.name)
    def __str__(self):
        return self.name
    def natural_key(self):
        return self.name

class StatusManager(models.Manager):
    def get_by_natural_key(self,status):
        return self.get(status=status)
@reversion.register()
class Status(models.Model):
    objects=StatusManager()
    status=models.CharField(max_length=100,verbose_name=u'状态')
    def natural_key(self):
        return (self.status)
    def __str__(self):
        return self.status
@reversion.register()
class Manufacturer(models.Model):
    manufacturer=models.CharField(max_length=100,verbose_name=u'品牌')
    def __str__(self):
        return self.manufacturer
    def natural_key(self):
        return self.manufacturer
@reversion.register()
class Zone(models.Model):
    zone=models.CharField(max_length=100,verbose_name=u'区域')
    def __str__(self):
        return self.zone
    def natural_key(self):
        return self.zone
@reversion.register()
class OS(models.Model):
    os=models.CharField(max_length=100,verbose_name=u'操作系统')
    def __str__(self):
        return self.os
    def natural_key(self):
        return self.os

@reversion.register(follow=['staff_computers'])
class Computer(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'计算机名')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'状态')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True,verbose_name=u'品牌')
    os = models.ForeignKey(OS, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u'操作系统')
    assert_number = models.CharField(max_length=100, verbose_name=u'资产编号',unique=True)
    cpu = models.CharField(max_length=100, verbose_name=u'CPU')
    memory = models.CharField(max_length=100, verbose_name=u'内存')
    ipaddress = models.GenericIPAddressField(verbose_name=u'IP地址', )
    purchase_time = models.DateField(verbose_name=u'采购日期', null=True, blank=True)
    #staffs = models.ManyToManyField('Staff', null=True, blank=True, verbose_name=u'使用人员',related_name='computers')
    staffs = models.ManyToManyField('Staff', null=True, blank=True, verbose_name=u'使用人员',related_name='computer_staffs')
    #department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL,verbose_name=u'所属部门')
    purpose = models.CharField(max_length=100, verbose_name=u'用途')
    remarks = models.TextField(max_length=200, null=True, blank=True, verbose_name=u'备注信息')
    #field_history = FieldHistoryTracker(['status','staffs'])
    def natural_key(self):
        return self.assert_number
    def __str__(self):
        return self.assert_number

#from datetime import datetime
#from django.core.urlresolvers import reverse
#from django.db import models
from simple_history.models import HistoricalRecords
@reversion.register(follow=['computer_staffs','department'])
class Staff(models.Model):
    name=models.CharField(max_length=100,verbose_name=u'姓名')
    tel=models.CharField(max_length=11,verbose_name=u'联系电话',null=True,blank=True)
    email=models.EmailField(help_text=u'邮箱地址',null=True,blank=True)
    ipaddress=models.GenericIPAddressField(verbose_name=u'IP地址',null=True,blank=True)
    entrydata=models.DateTimeField(verbose_name=u'入职日期',null=True,blank=True)
    department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL,verbose_name=u'所属部门',related_name='department_staff')
    #computer=models.ManyToManyField('Computer',verbose_name=u'主机信息',related_name='staffs',blank=True,null=True,)
    computers = models.ManyToManyField('Computer', verbose_name=u'主机信息',blank=True, null=True, related_name='staff_computers')

    #history = HistoricalRecords()
    #field_history=FieldHistoryTracker(['name','computer','tel'])
    '''
    def get_absolute_url(self):
        return reverse('updatestaff',kwargs={'pk':self.pk})
    '''
    def natural_key(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering=['ipaddress']
        unique_together = ('name','ipaddress')
@reversion.register()
class Servers(models.Model):
    name = models.CharField(max_length=100,verbose_name=u'服务器名')
    ipaddress = models.GenericIPAddressField(verbose_name=u'IP地址')
    assert_number = models.CharField(max_length=100,verbose_name=u'资产编号')
    status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True, blank=True,verbose_name=u'状态')
    manufacturer=models.ForeignKey(Manufacturer,on_delete=models.SET_NULL,null=True, blank=True,verbose_name=u'品牌')
    mmodel=models.CharField(max_length=100,verbose_name=u'型号')
    serial=models.CharField(max_length=100,verbose_name=u'序列号')
    purchase_time=models.DateField(verbose_name=u'采购日期')
    zone=models.ForeignKey(Zone,on_delete=models.SET_NULL,null=True, blank=True,verbose_name=u'所属区域')
    staff = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.SET_NULL,verbose_name=u'管理员')
    purpose=models.CharField(max_length=100,verbose_name=u'用途')
    os=models.ForeignKey(OS, null=True, blank=True, on_delete=models.SET_NULL,verbose_name=u'操作系统')
    remarks = models.TextField(max_length=200,null=True,blank=True,verbose_name=u'备注信息')
    def natural_key(self):
        return self.assert_number
    '''
    def get_absolute_url(self):
        return reverse('updatestaff',kwargs={'pk':self.pk})
    '''
    def __str__(self):
        return self.name
    '''
    class Meta:
        unique_together = ('name', 'ipaddress')
    '''
@reversion.register()
class EditHistory(models.Model):
    modelname=models.CharField(u'修改模型',max_length=100)
    item=models.CharField(u'修改条目',max_length=100)
    context=models.TextField(verbose_name=u'修改内容',max_length=1000)
    editTime=models.DateTimeField(auto_now=True,verbose_name=u'修改时间')
    class Meta:
        ordering = ['-editTime']


