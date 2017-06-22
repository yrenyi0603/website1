from django.views.generic.edit import FormView,UpdateView,CreateView,DeleteView,FormMixin
class ManyToManyMixin(object):
    def many_many(self,form):
        if self.object:
            obj=self.object
        else:
            obj=self.get_object()

        def _add_remove_many_object(many_to_many_objs, option, field_name=None):
            '''
                如果两个对象都有many to many子段且指向对方,则需要手动更新多对多关系;
                否则不需要手动更新对应关系
                many_to_many_objs 不能为空
            '''
            try:
                '''如果此对象也存在many to many子段类型，则取出相应的子段'''
                fmany = many_to_many_objs[0]._meta.many_to_many
            except:
                return 'error'
            # ffield = []
            if fmany:
                '''如果此对象的many  to many子段与self.object是同一个model，则取出'''
                ffield = [f for f in fmany if f.related_model._meta.model_name == self.model._meta.model_name]
                for many_many_obj in many_to_many_objs:
                    for t in ffield:
                        getattr(getattr(many_many_obj, t.name), option)(obj)
                        # getattr(getattr(self.get_object(), field_name),option)(many_many_obj)
                        # print(type(many_many_obj))

        for field in obj._meta.many_to_many:
            newobjs = set(form.clean().get(field.name))
            if  isinstance(self,(CreateView)):
                oldobjs = set([])
            else:
                oldobjs = set(getattr(obj, field.name).all())
            if newobjs and list(newobjs - oldobjs):
                _add_remove_many_object(list(newobjs - oldobjs), 'add')
            if oldobjs and oldobjs-newobjs:
                _add_remove_many_object( list(oldobjs - newobjs), 'remove')


