from django import forms
from django.forms import ModelForm,Textarea
from .models import *
from django.forms.extras.widgets import SelectDateWidget
from django.forms import DateTimeInput,DateInput,TextInput,CharField,Select

from django.forms import widgets

class MModelForm(ModelForm):
    def __init__(self,*agrs,**kwargs):
        super(MModelForm, self).__init__(*agrs, **kwargs)
        for key,value in self.fields.items():
            value=self.fields[key].widget
            validType=None
            css = 'easyui-textbox'
            other_option = None
            if isinstance(value, forms.widgets.Select ):
                css='easyui-combobox'
            elif isinstance(value,forms.widgets.DateInput):
                css='easyui-datebox'
                other_option = "formatter:myformatter,parser:myparser"
            elif isinstance(value, forms.widgets.DateTimeInput):
                css='easyui-datetimebox'
            elif isinstance(value,forms.widgets.Textarea):
                self.fields[key].widget.attrs.pop('cols')
                self.fields[key].widget.attrs.pop('rows')
                other_option='multiline:true'
                #print(self.fields[key].widget.__dict__)
            elif isinstance(value, forms.widgets.EmailInput):
                validType = "email"
            else:
                pass

            if isinstance(self.fields[key],forms.fields.GenericIPAddressField):
                validType = "ipaddress"
                #print(self.fields[key].__dict__)
            else:
                pass
            css = 'easyui-validatebox {0}'.format(css)
            if validType:
                data_option='validateOnCreate: false, validateOnBlur: true,{0}'.format('validType:\'{0}\''.format(validType))
            else:
                data_option = 'validateOnCreate: false, validateOnBlur: true'
            if other_option:
                #pass
                data_option=','.join((data_option,other_option))
            else:
                pass

            self.fields[key].widget.attrs.update({'class': ','.join((self.fields[key].widget.attrs.get('class', ''), css)).strip(',')})
            self.fields[key].widget.attrs.update({'data-options': data_option})
            self.fields[key].widget.attrs.update({'style':','.join((self.fields[key].widget.attrs.get('style',''), 'width:100%;')).strip(',')})

class StaffForm(MModelForm):
    mtype = forms.CharField(disabled=True, widget=forms.HiddenInput, initial='staff')
    class Meta:
        model = Staff
        fields=['name','tel','email','ipaddress','department','entrydata','computers']
        '''
        widgets={
            'name':forms.widgets.TextInput(attrs={'class':'easyui-textbox'}),
            'tel': forms.widgets.NumberInput(attrs={'class': 'easyui-textbox'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'easyui-textbox'}),
            'ipaddress': forms.widgets.TextInput(attrs={'class': 'easyui-textbox'}),
            'department': forms.widgets.Select(attrs={'class': 'easyui-combobox'}),
            'entrydata': forms.widgets.DateTimeInput(attrs={'class': 'easyui-datetimebox'}),
        }
        '''
class DepartmentForm(MModelForm):
    class Meta:
        model = Department
        fields=['name','email']

class StatusForm(MModelForm):
    class Meta:
        model = Status
        fields = ['status']
class ZoneForm(MModelForm):
    class Meta:
        model = Zone
        fields = ['zone']
class OSForm(MModelForm):
    class Meta:
        model = OS
        fields = ['os']
class ManufacturerForm(MModelForm):
    class Meta:
        model = Manufacturer
        fields = ['manufacturer']

class MdataFormFied(forms.DateField):
    def widget_attrs(self, widget):
        return {'class': 'easyui-datebox', 'style': "width:60%,text-align:center"}
class MinputFormFied(forms.CharField):
    def widget_attrs(self, widget):
        return {'class': 'easyui-textbox', 'style': "width:60%,text-align:center"}
class MSelectFormFied(forms.ModelChoiceField):
    def widget_attrs(self, widget):
        return {'class':'easyui-combobox','style':"width:60%"}
class MIPFormFied(forms.GenericIPAddressField):
    def widget_attrs(self, widget):
        return {'class':'easyui-textbox','style':"width:60%"}

class ServersForm(MModelForm):
    mtype=forms.CharField(disabled=True,widget=forms.HiddenInput,initial='server')
    class Meta:
        model = Servers
        fields = '__all__'
        '''
        field_classes={
            'purchase_time':MdataFormFied,
            'ipaddress':MIPFormFied,
            'name': MinputFormFied,
            'os':MSelectFormFied,
            'zone': MSelectFormFied,
            'staff': MSelectFormFied,
            'manufacturer': MSelectFormFied,
            'status': MSelectFormFied,
        }
        '''
        '''
        widgets = {
            'name':forms.widgets.Input(attrs={'class': 'easyui-textbox'}),
        }
        '''

class ComputerForm(MModelForm):
    mtype=forms.CharField(disabled=True,widget=forms.HiddenInput,initial='computer')
    class Meta:
        model = Computer
        fields = '__all__'

class PowercheckForm(MModelForm):
    class Meta:
        model = Powercheck
        fields = '__all__'
class EmailCheckModelForm(MModelForm):

    class Meta:
        model = Emailcheck
        fields = '__all__'
    #
    # def save(self, commit=True):
    #
    #     #print(self.cleaned_data)
    #     if  not self.cleaned_data['name']:
    #         try:
    #             #opts = self._meta
    #             #print('111111111111111111:{0}'.format(opts))
    #             #self.instance = self._meta.model()
    #             print(self.cleaned_data['email'])
    #             obj=Staff._default_manager.get(email__exact = self.cleaned_data['email'])
    #             self.
    #         except Exception as e:
    #             print('----------------------')
    #             print(e)
    #             print('----------------------')
    #     return  super(EmailCheckModelForm,self).save(commit=True)