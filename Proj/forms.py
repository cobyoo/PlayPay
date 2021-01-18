from django import forms
from Proj.models import *


class JoinForm(forms.Form):
    your_id = forms.EmailField(label='아이디', max_length=100)
    your_pw = forms.CharField(label='비밀번호', max_length=100, widget = forms.PasswordInput)
    your_ph = forms.IntegerField(label='전화번호(숫자만)')
    your_name = forms.CharField(label='이름', max_length=10)
    your_age = forms.IntegerField(label='나이')
    your_sex = forms.IntegerField(label='성별(안내문 참조)')
    your_avg_time = forms.IntegerField(label='하루 평균 PC방 이용시간(안내문 참조)')
    your_food_choice = forms.IntegerField(label='음식 주문 여부(안내문 참조)')

class LoginForm(forms.Form):
    your_id = forms.EmailField(label='아이디', max_length=100)
    your_pw = forms.CharField(label='비밀번호', max_length=100, widget = forms.PasswordInput)

class AdminForm(forms.Form):
    your_id = forms.EmailField(label='학생 ID', max_length=100)

class EditForm(forms.Form):
    your_pw = forms.CharField(label='비밀번호', max_length=100, widget = forms.PasswordInput)
    your_ph = forms.CharField(label='전화번호', max_length=11)
    your_name = forms.CharField(label='이름', max_length=10)

class BoardForm(forms.Form):
    your_board = forms.ChoiceField(widget = forms.Select(), choices = ([('1','리뷰 게시판')]), initial='1', label='게시판 선택', required = True)
    your_title = forms.CharField(max_length=200, label='제목')
    your_content = forms.CharField(widget=forms.Textarea, label='내용')
    your_star = forms.ChoiceField(widget = forms.Select(), choices = ([('1','★'), ('2','★★'),('3','★★★'), ('4','★★★★'), ('5','★★★★★')]), initial='1', label='별점 선택', required = True)
    your_tag = forms.CharField(max_length=200, label='태그', required=False, widget=forms.TextInput(attrs={'placeholder': 'comma-separated'}))

class NoticeForm(forms.Form):
    your_board = forms.ChoiceField(widget = forms.Select(), choices = ([('1','리뷰 게시판'), ('2','공지사항')]), initial='1', label='게시판 선택', required = True)
    your_title = forms.CharField(max_length=200, label='제목')
    your_content = forms.CharField(widget=forms.Textarea, label='내용')

class BoardManageForm(forms.Form):
    your_boardnum = forms.IntegerField(label='게시판번호')
    your_board = forms.CharField(label='게시판명', max_length=100)

class SearchForm(forms.Form):
    your_search = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter HashTags..'}))

class SettingForm(forms.Form):
    your_settingnum = forms.IntegerField(label='시간설정')

class FoodForm(forms.Form):
    your_con1 = forms.ChoiceField(widget = forms.Select(), choices = ([('0','갈비만두'), ('1','감자튀김'),('2','떡볶이'), ('3','레몬에이드'), ('4','불닭볶음면'), ('5','소떡소떡'), ('6','수제소시지'), ('7','스프라이트'), ('8','슬라이스 치즈'), ('9','신라면'), ('10','아메리카노'), ('11','자몽에이드'), ('12','제육덮밥'), ('13','짜파게티'), ('14','참치김밥'), ('15','청포도에이드'), ('16','치킨마요덮밥'), ('17','코카콜라'), ('18','펩시'), ('19','포스틱'), ('20','포카칩'), ('21','핫도그'), ('22','핫바'), ('23','햇반'), ('24','허니버터칩'), ('25','홈런볼')]), initial='0', label='메뉴 선택', required = True)
