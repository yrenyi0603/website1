from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import ListView,DetailView,View,TemplateView
from django.core.serializers import serialize
from .models import *
from django.views.generic.edit import FormView,UpdateView,CreateView,DeleteView,FormMixin
from .forms import *
from reversion.views import RevisionMixin
from django.db.models.fields.related import ManyToManyField, ForeignKey
from .mixin.manytomany import ManyToManyMixin
import reversion
'''
from django.core import serializers
from django.core.paginator import Page
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
'''
from django.core.files.uploadedfile import  InMemoryUploadedFile
# from django.http import HttpResponse
SUCCESS=0
FAIED=1
histag={
    'form':'update',
    'add':'add',
    'delete':'delete',
}
from django.core.urlresolvers import reverse
from django.forms import ModelForm
class HomeView(View):
    def get(self,request):
        return render(request,'base.html')
from .tasks import *
from django.core.exceptions import ImproperlyConfigured
class MModelView(ListView,FormMixin):
    model = None
    # template_name = 'manufacturers.html'
    form_class = None

    def get_context_data(self, **kwargs):
        context=super(MModelView,self).get_context_data(**kwargs)
        mname = self.model._meta.verbose_name
        context['url'] = {
            # 'addurl': reverse('add{0}'.format(self.model.__name__.lower())),
            'addurl': reverse('add{0}'.format(mname)),
            'editurl': reverse('update{0}'.format(mname)),
            'deleteurl': reverse('delete{0}'.format(mname)),
            'historyurl': reverse('history{0}'.format(mname)),
            'objlist': reverse('{0}list'.format(mname))
        }
        context['form']=self.get_form()
        # sendEmailList.delay()
        # print('result:{0}'.format(r.get(timeout=100)))
        return context

    def get_template_names(self):
        names = super(MModelView, self).get_template_names()
        opts = self.model._meta
        names.append("%s/list/%s%s.html" % (opts.app_label, opts.model_name, self.template_name_suffix))
        return names


class MEditView(ManyToManyMixin,RevisionMixin,UpdateView):
    model = None
    form_class = None

    def form_valid(self, form):

        if form.changed_data:
            self.many_many(form=form)
            self.object = form.save()
            reversion.set_comment(histag.get('form'))
        return JsonResponse(data={'status':SUCCESS})

    def form_invalid(self, form):
        return JsonResponse(data={'status': FAIED})
    def get(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg]=request.GET['pk']
        return super(MEditView, self).get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = request.POST['pk']
        return super(MEditView,self).post(request,*args,**kwargs)
    # def get_context_data(self, **kwargs):
    #     form=super(MEditView,self).get_context_data(**kwargs)
    #     form['form'] = self.form_class(instance=self.get_object())
    #     return form
    def get_template_names(self):
        names = super(MEditView, self).get_template_names() or []
        names.append("%s/form/%s%s.html" % (
                    self.model._meta.app_label,
                    self.model._meta.model_name,
                    self.template_name_suffix
                ))
        return names

class StaffEditView(MEditView):
    def form_valid(self, form):
        return super(StaffEditView,self).form_valid(form=form)

class ComputerEditView(MEditView):
    def form_valid(self, form):
        return super(ComputerEditView,self).form_valid(form=form)

class MAddView(ManyToManyMixin,CreateView):
    model = None
    form_class = None

    def form_valid(self, form):
        # print(form)
        '''记录add相关子段的revevision'''
        with reversion.create_revision():
            self.object=form.save()
            reversion.set_comment(histag.get('add'))
        '''记录update相关子段的revevision'''
        with reversion.create_revision():
            self.many_many(form=form)
            reversion.set_comment(histag.get('form'))
        return JsonResponse(data={'status':SUCCESS})

    def form_invalid(self, form):
        print(form.cleaned_data)
        print('=========================invalid:{0}'.format(form.errors.as_json()))
        return JsonResponse(data={'status': FAIED})
    def get_template_names(self):
        names=super(MAddView,self).get_template_names()
        names.append("%s/form/%s%s.html" % (
                    self.model._meta.app_label,
                    self.model._meta.model_name,
                    self.template_name_suffix
                ))
        print(names)
        return names
    # def get(self, request, *args, **kwargs):
    #
    #     return render(request,template_name='base_form.html',context={'form':self.form_class})
    # def get_context_data(self, **kwargs):
    #     context=super(MAddView,self).get_context_data(**kwargs)
    #     context['form']=self.form_class
    #     return context

class EmailcheckaddView(MAddView):
    def form_valid(self, form):
        try:
            email=form.cleaned_data.get('email',None)
            email=[email] if email  else []
            staffemails = form.cleaned_data.get('staffemails', [])
            email.extend(staffemails)
            with reversion.create_revision():
                for i in email:
                    try:
                        if email.index(i) == 0:
                            self.model(email=i,name=form.cleaned_data['name'],
                                       lastcgdate=form.cleaned_data['lastcgdate'],
                                       remarks=form.cleaned_data['remarks']).save()
                        else:
                            self.model(email=i).save()
                        reversion.set_comment(histag.get('add'))
                    except Exception as e:
                        return  super(EmailcheckaddView,self).form_invalid(form=form)

        except Exception as e:
            pass
        return JsonResponse(data={'status': SUCCESS})
class PowercheckaddView(MAddView):
    def form_valid(self, form):
        try:
            ipaddress=form.cleaned_data.get('ipaddress',None)
            ipaddress=[ipaddress] if ipaddress  else []
            temp=ipaddress.copy()
            staffipadderss = form.cleaned_data.get('staffipadderss', [])
            ipaddress.extend(staffipadderss)
            with reversion.create_revision():
                for i in ipaddress:
                    try:
                        if temp:
                            self.model(ipaddress=i,name=form.cleaned_data['name'],
                                       email=form.cleaned_data['email'],status=form.cleaned_data['status'],
                                       remarks=form.cleaned_data['remarks']).save()
                        else:
                            self.model(ipaddress=i,status=form.cleaned_data['status']).save()
                        reversion.set_comment(histag.get('add'))
                    except Exception as e:
                        print(e)
                        return  super(PowercheckaddView,self).form_invalid(form=form)

        except Exception as e:
            pass
        return JsonResponse(data={'status': SUCCESS})

class MDeleteView(RevisionMixin,DeleteView):
    model = None
    def delete(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = request.POST['pk']
        self.object=self.get_object()
        with reversion.create_revision():
            self.object.save()
            reversion.set_comment(histag.get('delete'))
        self.object.delete()

        return JsonResponse(data={'status': SUCCESS})


from django.forms import formset_factory

import json
class MListView(ListView):
    model = None
    def get_objlist(self,request):
        page = request.POST['page']
        rows = request.POST['rows']
        objects = self.get_queryset()
        result = self.get_paginator(objects, per_page=rows)

        # a=result.page(page).object_list
        #print(help(a))
        #b=serialize('json',result.page(page),use_natural_foreign_keys=True, use_natural_primary_keys=True)
        rjson = serialize('json', result.page(page), use_natural_foreign_keys=True)
        #print(rjson)
        total=result.count
        return total,rjson

    def post(self,request):
        total, rlist = self.get_objlist(request)
        r=[dict(**{'pk':i['pk']},**i['fields']) for i  in json.loads(rlist)]
        #print(r)
        return JsonResponse(data={"total": total, "rows": r})

class ServersListView(MListView):
    def get_queryset(self):
        try:
            queryset = self.model._default_manager.all()

            status=self.request.POST['status']
            zone=self.request.POST['zone']
            ipaddress=self.request.POST['ipaddress'].strip()
            assert_number=self.request.POST['assert_number'].strip()

            queryset = queryset.filter(status=status) if status else queryset
            queryset = queryset.filter(zone=zone) if zone else queryset
            queryset =  queryset.filter(ipaddress__contains=ipaddress) if ipaddress else queryset
            queryset = queryset.filter(assert_number__contains=assert_number) if assert_number else queryset
            return  queryset
            # return queryset.filter(ipaddress__contains=ipaddress,assert_number__contains=assert_number)
        except Exception as e:
            return super(ServersListView,self).get_queryset()
class StaffLIstView(MListView):
    def get_queryset(self):
        try:
            name=self.request.POST['name'].strip()
            ipaddress = self.request.POST['ipaddress'].strip()
            queryset = self.model._default_manager.all()
            department=self.request.POST['department']

            queryset = queryset.filter(department=department) if department else queryset
            queryset = queryset.filter(name__contains=name) if name else  queryset
            queryset = queryset.filter(ipaddress__contains=ipaddress) if ipaddress else queryset
            return queryset
            # return queryset.filter(name__contains=name,ipaddress__contains=ipaddress)
        except:
            return super(StaffLIstView,self).get_queryset()

from reversion.models import Version


class HisListView(DetailView):
    def get_history(self):
        from dateutil import tz
        from django.conf import settings
        to_zone=tz.gettz(settings.TIME_ZONE)

        version = Version.objects.get_for_object(obj=self.get_object())
        '''
            如果有外键或者Many-Many Field被删除，则需要手动更新一下version
        '''
        if version[0].revision.comment == histag.get('delete'):
            with reversion.create_revision():
                obj=self.get_object()
                obj.save()
                reversion.set_comment(histag.get('form'))
            version = Version.objects.get_for_object(obj=self.get_object())

        context = []
        versions = list(version)

        for index, i in enumerate(versions):
            diffs = {}
            diff_context = ''
            '''获取更新值'''
            if i.revision.comment == histag.get('form'):
                '''获取更新子段'''
                diff = [k for k in i.field_dict if i.field_dict[k] != versions[index + 1].field_dict[k]]
                if diff:
                    for c in diff:
                        value_new = i.field_dict[c]
                        value_old = versions[index + 1].field_dict[c]

                        if isinstance(self.model._meta.get_field(c), (ManyToManyField, ForeignKey)):
                            if isinstance(self.model._meta.get_field(c), (ForeignKey)):
                                value_old = [value_old ] if value_old else []
                                value_new = [value_new] if value_new else []
                            model_relate = self.model._meta.get_field(c).related_model
                            value_new = self.get_relate_fields(model=model_relate, values=value_new)
                            value_old = self.get_relate_fields(model=model_relate, values=value_old)
                        diff_context = '<br>'.join([diff_context, '修改子段："{0}",由 "{2}" 修改为 "{1}" ;'.format(
                            self.model._meta.get_field(c).verbose_name, value_new, value_old)])
                    diffs['time'] = i.revision.date_created.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')
                    diffs['context'] = diff_context.strip('<br>')
                    context.append(diffs)
                else:
                    pass
        '''获取初始化值'''
        if versions[-1].revision.comment == histag.get('add'):
            context.append({'time':versions[-1].revision.date_created.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S'),'context':'添加'})
        return context
    def get_relate_fields(self, model, values):
        temp = []
        for value in values:
            try:
                t = model.objects.get(pk=value)
                temp.append(t)
            except:
                delete_objs=Version.objects.get_deleted(model=model)
                for delete_obj in delete_objs:
                    if int(delete_obj.object_id) == value:
                        temp.append(delete_obj.object_repr)
        return [str(i) for i in temp]

    def post(self,request):
        self.kwargs.setdefault(self.pk_url_kwarg, self.request.POST['pk'])
        context=self.get_history()
        page = int(request.POST['page'])
        rows = int(request.POST['rows'])
        begin=(page-1)*rows if page>1 else 0
        end=page*rows if page*rows < len(context) else len(context)
        return JsonResponse(data={"total": len(context), "rows": context[begin:end]})
from django.utils.timezone import utc
import  pandas as pd
import numpy as np
from django_pandas.io import read_frame
from rest_framework import viewsets
from rest_framework.response import Response
class MainView(viewsets.ViewSet):
    def list(self,request):
        a=json.loads(self.get_server_status())
        b={}
        b['status']={}
        b['status']['items']=a.keys()
        b['status']['values']=[]
        b['count']={}
        b['count']['items']=['计算机主机','服务器主机']
        pc_count=Computer.objects.count()
        server_count = Servers.objects.count()
        b['count']['values'] = [pc_count,server_count]
        for i,j in a.items():
            temp={}
            temp['name']=i
            temp['value']=j
            b['status']['values'].append(temp)
        return Response(b)
    def get_server_status(self):
        from .models import Servers
        model=Servers
        from .serializer.modelserializer import ServerSerializer
        serializer=ServerSerializer(model.objects.all(),many=True)
        df=pd.DataFrame(serializer.data,index=[i['id'] for i in serializer.data])
        if  df.empty:
            return '{}'
        df['status']=df['status'].fillna('other')
        return df.groupby('status').size().to_json()
from .serializer.modelserializer import *
class FieldTreeView(View):
    model=None
    field=None
    def gettree(self,field):

        serializer = StaffSerializer(self.get_queryset(), many=True)
        df=pd.DataFrame(data=serializer.data)
        tree = {}
        tree['id'] = 0
        tree['text'] = "wosign"
        tree['children'] = []
        root = tree.copy()
        if df.empty:
            pass
        else:
            groupd=df.groupby(['department'])
            n=1
            for i ,j in groupd:
                subtree={}
                subtree['id']=n
                n+=n
                subtree['text']=i
                subtree['children']=[]
                if getattr(j,field,pd.DataFrame()).empty:
                    raise TypeError('field {0}  not exist'.format(field))
                for m in getattr(j,field):
                    tree_item={}
                    tree_item['id']=n
                    n+=1
                    tree_item['text']=m
                    subtree['children'].append(tree_item)
                    #print(subtree)
                root['children'].append(subtree)
        return root
    def get_queryset(self):
        return Staff.objects.getcheck(self.model,self.field)
    def get(self,request):
        item=[]
        item.append(self.gettree(field=self.field))
        """
            JsonResponse默认只接受dict，要使其接受list，传入safe=False即可
        """
        return JsonResponse(item,safe=False)
    # def post(self):
    #     return JsonResponse({'status':1})

# class EmailTreeView(TemplateView):
#     template_name = 'tree.html'


from io import  StringIO

class excelView(View):
    model=None
    def get(self,request):
        # serializer = StaffSerializer(self.get_queryset(), many=True)
        # df = pd.DataFrame(data=serializer.data)
        rjson = serialize('json', self.get_queryset(), use_natural_foreign_keys=True)
        print(rjson)
        r = [dict( **{'id': i['pk']},**i['fields']) for i in json.loads(rjson)]
        # r = [dict(i['fields']) for i in json.loads(rjson)]
        import xlwt
        from datetime import datetime
        # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        #                      num_format_str='#,##0.00')
        # style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
        style2 = xlwt.easyxf('font: color-index red, bold on,height 200')
        pattern=xlwt.Pattern()
        pattern.pattern=xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 5
        style3=xlwt.XFStyle()
        font=xlwt.Font()
        font.colour_index = 4
        font.bold = True
        font.shadow = True
        style3.font=font
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet1')

        title=[i.verbose_name for i in self.model._meta.get_fields() if i.concrete]
        values=[i.values() for i in r]
        print(values)
        ws.panes_frozen = True
        ws.horz_split_pos = 1
        ws.horzi_split_fiHst_visibl = 3

        for i,j in enumerate(title):
            ws.write(0,i,j,style2)
            ws.col(i).width= 5000
        for i,j in enumerate(values):
            for m,n in enumerate(j):
                if i %2 == 0 :
                    style3.pattern = pattern
                else:
                    style3.pattern = xlwt.Pattern()
                ws.write(i+1,m,n,style3)

        # f=StringIO()
        # wb.save(f)
        response=HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="somefilename.xls"'
        wb.save(response)
        return response
        # return HttpResponse('status:1')

    def get_queryset(self):
        return  self.model._default_manager.all()
    # def post(self,request):
    #     from io import  StringIO
    #     f=StringIO()




