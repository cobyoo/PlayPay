from django.views.generic import ListView, FormView
from django.views import View
from Proj.models import *
from taggit.models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from Proj.forms import *
import json
import hashlib
from django.db.models import Q
import joblib
import pandas as pd


class Login(FormView):
    form_class = LoginForm
    template_name ="Proj/login.html"

    def get(self,request,*args,**kwargs):
        form = self.form_class(initial= self.initial)
        #request.session['login'] = False # 추가 session
        return render(request,self.template_name,{'form':form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['your_id']
            new_pw = form.cleaned_data['your_pw']
            m = hashlib.sha256()
            m.update(new_pw.encode('UTF-8'))
            x = m.hexdigest()
            
            try:
                 data = User.objects.get(my_id=new_id)
            except Exception:
                return redirect('proj:login')

            if x == data.pw:
                request.session['login'] = True # 추가 로그인 성공시 True 설정
                request.session['my_id'] = data.my_id
                request.session['time'] = data.time
                request.session['name'] = data.name

                return redirect('proj:main')
            else:
                return redirect('proj:login')
        
        return render(request,self.template_name,{'form':form})
    

class Main(View):

    def get(self, request, *args, **kwargs):
        #if not request.session.get('login', False):
        #    return HttpResponseRedirect('/')
        
        userdata = request.session.get('my_id')
        context = {'model_list':['Board'], 'userdata':userdata}

        return render(request, 'Proj/main.html', context=context)

class Join(FormView):
    form_class = JoinForm
    template_name ="Proj/join.html"

    def get(self,request,*args,**kwargs):
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self,request,*args,**kwargs):                  #my_id, pw, name, number, prof
        form = self.form_class(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['your_id']
            new_pw = form.cleaned_data['your_pw']
            new_ph = form.cleaned_data['your_ph']
            new_name = form.cleaned_data['your_name']
            new_sex = form.cleaned_data['your_sex']
            new_age = form.cleaned_data['your_age']
            new_avg_time = form.cleaned_data['your_avg_time']
            new_food_choice = form.cleaned_data['your_food_choice']
            m = hashlib.sha256()
            m.update(new_pw.encode('UTF-8'))
            x = m.hexdigest()
            try:
                User.objects.create(my_id=new_id, pw=x, name=new_name, ph=new_ph, sex = new_sex, region = 6., avg_time = new_avg_time, food_choice=new_food_choice, age=new_age)
            except:
                return redirect('proj:join')
            request.session['login'] = False
            return HttpResponseRedirect('/')
        
        return render(request,self.template_name,{'form':form})


class Edit(FormView):
    form_class = EditForm
    template_name = 'Proj/edit.html'

    def get(self,request,*args,**kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        new_my_id = request.session.get('my_id')
        form = self.form_class(initial= {'your_id':new_my_id})

        return render(request,self.template_name,{'form':form, 'my_id':new_my_id}) #, 'new_id':new_id
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_my_id = request.session.get('my_id')
            new_pw = form.cleaned_data['your_pw']
            new_ph = form.cleaned_data['your_ph']
            new_name = form.cleaned_data['your_name']
            try:
                data = User.objects.get(my_id=new_my_id)
            except Exception:
                return HttpResponse(Exception)

            m = hashlib.sha256()
            m.update(new_pw.encode('UTF-8'))
            x = m.hexdigest()
            if new_name != data.name or new_ph != data.ph or x != data.pw:
                data.pw=x
                data.ph=new_ph
                data.name=new_name
                data.save()
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/edit/')
        request.session['login'] = False

        return render(request,self.template_name,{'form':form})        


class Logout(View):

    def get(self, request, *args, **kwargs):
        request.session['login'] = False
        request.session['my_id'] = {}
        request.session['name'] = {}
        request.session['time'] = {}
        return HttpResponseRedirect('/')


class Admin(FormView):
    form_class = AdminForm
    template_name = 'Proj/admin.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['your_id']
            new_prof = form.cleaned_data['your_prof']
            try:
                post_instance = User.objects.filter(my_id=new_id)
                post_instance.update(prof=new_prof)
            except Exception:
                return render(request, 'Proj/admin.html', {'form':form})

            return HttpResponseRedirect('/admin/')

        return render(request, 'Proj/admin.html', {'form':form})

class Maps(View):
    
    def get(self, request, name):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        pcname = name
        return render(request, 'Proj/maps.html', {'name':pcname})           

class Setting(FormView):
    form_class = SettingForm
    template_name = 'Proj/main.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = SettingForm
        return render(request, 'Proj/setting.html' ,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)    
        if form.is_valid():
            new_boardnum = form.cleaned_data['your_settingnum']
            time = new_boardnum
            return render(request, self.template_name ,{'form':form})

class Distance(View):
    
    def get(self, request):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        
        return render(request, 'Proj/distance.html')  

class Boarding(View):
    
    def get(self, request):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        val = request.session.get('my_id')
        userdata = User.objects.get(my_id = val)
        boarddata1 = Board.objects.all()

        return render(request, 'proj/board.html', {'userdata':userdata, 'boarddata':boarddata1})


class BoardManage(FormView):
    form_class = BoardManageForm
    template_name = 'Proj/boardmanage.html'
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_boardnum = form.cleaned_data['your_boardnum']
            new_board = form.cleaned_data['your_board']
            Board.objects.create(boardnum=new_boardnum, title=new_board)                

        return redirect('proj:main')

class ContentList(View):

    def get(self, request, boardnum):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        data = Text.objects.filter(boardnumber=boardnum).order_by('-id')
        form = SearchForm
        bn = boardnum
        return render(request, 'proj/contentlist.html', {'data':data, 'bn':bn, 'form':form})

    def post(self, request, boardnum):
    
        data = Text.objects.filter(boardnumber=boardnum).order_by('-star')
        bn = boardnum
        form = SearchForm
        return render(request, 'proj/contentlist.html', {'data':data, 'bn':bn, 'form':form})


class SearchContent(FormView):
    form_class = SearchForm
    template_name = 'Proj/contentlist.html'
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self, request, boardnum):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_search = form.cleaned_data['your_search']
            data = Text.objects.filter(boardnumber=boardnum).filter(tags__name=new_search)
            bn = boardnum
            return render(request, 'Proj/contentlist.html', {'data':data, 'bn':bn, 'form':form})

        return redirect('proj:main')


class Food(FormView):
    form_class = FoodForm
    template_name = 'Proj/food.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        form = self.form_class(initial= self.initial)
        return render(request,self.template_name,{'form':form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_con1 = float(form.cleaned_data['your_con1'])
            data = User.objects.filter(my_id=request.session.get('my_id'))
            for qs in data.iterator():
                new_sex = float(qs.sex)
                new_region = float(qs.region)
                new_avg_time = float(qs.avg_time)
                new_food_choice = float(qs.food_choice)
                new_age = float(qs.age)
            arr = [[new_sex, new_region, new_avg_time, new_food_choice, new_con1, new_age]]
            file_name = 'object_01.pkl'
            obj = joblib.load(file_name)
            y_pred = int(obj.predict(arr))
            return render(request, 'Proj/foodResult.html', {'food':y_pred})

        return redirect('proj:food')


class Content(View):
    def get(self, request, boardnum, textnum):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        data = Text.objects.get(id=textnum)
        bn = boardnum
        tn = textnum
        return render(request, 'proj/content.html', {'data':data, 'bn':bn, 'tn':tn})


class Write(FormView):
    form_class = BoardForm
    template_name = 'Proj/write.html'


    def get(self, request):
        mid = request.session.get('my_id')
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')
        if mid != 'admin@admin.admin':
            form = self.form_class(initial= self.initial)
            return render(request,self.template_name,{'form':form})
        else:
            form = NoticeForm
            return render(request, self.template_name, {'form':form})

    def post(self, request):
        mid = request.session.get('my_id')
        if mid != 'admin@admin.admin':
            form = self.form_class(request.POST)
            if form.is_valid():            
                new_board = form.cleaned_data['your_board']
                me = Board.objects.get(boardnum=new_board)
                new_title = form.cleaned_data['your_title']
                new_content = form.cleaned_data['your_content']
                new_star = form.cleaned_data['your_star']
                new_tag = form.cleaned_data['your_tag'].split(',')
                new_user = request.session.get('my_id')

                data = Text.objects.create(id=None,boardnumber=me, text_title=new_title, content=new_content, star=new_star, user=new_user)    
                if new_tag != None:
                    for tag in new_tag:
                        tag = tag.strip()
                        data.tags.add(tag)            

            return HttpResponseRedirect('/board/1/')

        else:
            form = NoticeForm(request.POST)
            if form.is_valid():            
                new_board = form.cleaned_data['your_board']
                me = Board.objects.get(boardnum=new_board)
                new_title = form.cleaned_data['your_title']
                new_content = form.cleaned_data['your_content']
                new_star = request.POST.get('star_')

                Text.objects.create(id=None,boardnumber=me, text_title=new_title, content=new_content, star=new_star)

            return HttpResponseRedirect('/board/')            


class Delete(View):
    def get(self, request, boardnum, textnum):
        if not request.session.get('login', False):
            return HttpResponseRedirect('/')

        data = Text.objects.get(id=textnum)
        data.delete()

        return HttpResponseRedirect('/board/1/')

def Fox(request):
    name1 = 'fox'
    return render(request, 'pc/fox.html', {'name1':name1})

def Ghostcastle(request):
    name2 = 'ghostcastle'
    return render(request, 'pc/ghostcastle.html', {'name2':name2})

def Lime(request):
    name3 = 'lime'
    return render(request, 'pc/lime.html', {'name3':name3})

def Ocelot(request):
    name4 = 'ocelot'
    return render(request, 'pc/ocelot.html', {'name4':name4})

def Pop(request):
    name5 = 'pop'
    return render(request, 'pc/pop.html', {'name5':name5})

def Skybridge(request):
    name6 = 'skybridge' 
    return render(request, 'pc/skybridge.html', {'name6':name6})

def Pclist(request):
    name1='fox'
    name2='ghostcastle'
    name3='lime'
    name4='ocelot'
    name5='pop'
    name6='skybridge'
    context = {'name1':name1,'name2':name2,'name3':name3,'name4':name4,'name5':name5,'name6':name6}
    return render(request, 'pc/pclist.html', context=context)


def Payment(request):
    try:
        new_id = request.session.get('my_id')
        info = User.objects.get(my_id=new_id)
        info.time += 30
        info.save()
        request.session['time'] = info.time
    except Exception:
        return redirect('proj:main')
    return redirect('proj:main')
    
def Refund(request):
    try:
        new_id = request.session.get('my_id')
        info = User.objects.get(my_id=new_id)
        info.time -= 30
        if (info.time < 0):
            info.time += 30
            return redirect('proj:main')
        else:
            info.save()
        request.session['time'] = info.time
    except Exception:
        return redirect('proj:main')
    return redirect('proj:main')