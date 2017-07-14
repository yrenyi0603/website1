
from django.conf.urls import url,include
from .models import *
from . import  views
from .forms import *
from django.contrib.auth.decorators import login_required

staff_info={
    'model':Staff,
    'form_class':StaffForm,
    'listview':views.StaffLIstView,
    'export':True,
    'list_template':True,
    #'editview':views.StaffEditView,
}
server_info={
    'model':Servers,
    'form_class':ServersForm,
    'listview':views.ServersListView,
    'export':True,
    'list_template':True,
}
zone_info={
    'model':Zone,
    'form_class':ZoneForm,
}

status_info={
    'model':Status,
    'form_class':StatusForm,
}

department_info={
    'model':Department,
    'form_class':DepartmentForm,
}
os_info={
    'model':OS,
    'form_class':OSForm,
}
manufacturer_info={
    'model':Manufacturer,
    'form_class':ManufacturerForm,
}
computer_info={
    'model':Computer,
    'form_class':ComputerForm,
    #'editview':views.ComputerEditView,
    'list_template':True,
    'export':True,
}
emailcheck_info={
    'model':EmailcheckModel,
    'addview':views.EmailcheckaddView,
    'form_class':EmailCheckModelForm,
    'edit_form_template':False,
    'add_form_template':True,
}

powercheck_info={
    'model':PowercheckModel,
    'addview':views.PowercheckaddView,
    'form_class':PowercheckForm,
    'edit_form_template':False,
    'add_form_template':True,
    # 'edit_form':'polls/form/',
}

urls=[]

models_info=[staff_info,server_info,zone_info,status_info,department_info,os_info,manufacturer_info,computer_info,emailcheck_info,powercheck_info]
for info in models_info:
    model=info['model']
    modelname = model._meta.verbose_name
    formclass=info['form_class']

    model_listview=info.get('listview',None) or views.MListView
    editview=info.get('editview',None) or views.MEditView
    addview=info.get('addview',None) or views.MAddView

    if info.get('export',False):
        urls.append(url('{0}/excel/$'.format(modelname),login_required(views.excelView.as_view(model=model)),name='excel_{0}'.format(modelname)))
    if info.get('list_template',False):
        urls.append(url('{0}/all/$'.format(modelname),login_required(views.MModelView.as_view(model=model,form_class=formclass)),name=modelname))
    else:
        urls.append(url('{0}/all/$'.format(modelname),
                        login_required(views.MModelView.as_view(model=model, form_class=formclass,template_name = 'polls/base_list.html')), name=modelname))

    urls.append(url('{0}/list/$'.format(modelname),login_required(model_listview.as_view(model=model)),name='{0}list'.format(modelname)))

    if  info.get('add_form_template',False):
        urls.append(url('{0}/add/$'.format(modelname), login_required(
            addview.as_view(model=model, form_class=formclass)),name='add{0}'.format(modelname)))
    else:
        urls.append(url('{0}/add/$'.format(modelname), login_required(addview.as_view(model=model,form_class=formclass,template_name='polls/base_form.html')),name='add{0}'.format(modelname)))
    if not info.get('edit_form_template',False):
        urls.append(url('{0}/update/$'.format(modelname), login_required(editview.as_view(model=model, form_class=formclass,template_name='polls/base_form.html')),name='update{0}'.format(modelname)))
    else:
        urls.append(url('{0}/update/$'.format(modelname), login_required(editview.as_view(model=model, form_class=formclass)),name='update{0}'.format(modelname)))

    urls.append(url('{0}/delete/$'.format(modelname), login_required(views.MDeleteView.as_view(model=model)),name='delete{0}'.format(modelname)))
    urls.append(url('{0}/history/$'.format(modelname), login_required(views.HisListView.as_view(model=model)),name='history{0}'.format(modelname)))

urlpatterns = [
    url(r'^$',login_required(views.HomeView.as_view()),name='home' ),
    url(r'^main/$',login_required(views.MainView.as_view({'get':'list'})),name='main' ),
    url(r'^emailtree/$',login_required(views.FieldTreeView.as_view(field='email',model=EmailcheckModel)),name='emailtree' ),
    url(r'^ipaddresstree/$',login_required(views.FieldTreeView.as_view(field='ipaddress',model=PowercheckModel)),name='iptree' ),
]
urlpatterns.extend(urls)
print(urlpatterns)
