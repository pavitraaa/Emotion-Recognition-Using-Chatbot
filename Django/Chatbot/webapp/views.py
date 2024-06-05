
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import users
from .models import accuracy
from .models import chat
from .models import *
from django.core import serializers
from django.template import Context
from .NBTrain import NBTrain
from .NNTrain import NNTrain
from .SVMTrain import SVMTrain
from .RFTrain import RFTrain
from .KNNTrain import KNNTrain
from .Testing import Testing
from .tf import tf
from .tf2 import tf2
import numpy as np
import xlrd
import matplotlib.pyplot as plt;
from .Prediction import Prediction
from django.utils.html import format_html_join
from django.db.models import F

def home(request):
	return render(request, 'index.html')
def userhomedef(request):
	if "useremail" in request.session:
		uid=request.session["useremail"]
		d=users.objects.filter(email__exact=uid)
		return render(request, 'user_home.html',{'data': d[0]})

	else:
		return render(request, 'user.html')

	
def adminhomedef(request):
	if "adminid" in request.session:
		uid=request.session["adminid"]
		return render(request, 'admin_home.html')

	else:
		return render(request, 'admin.html')

	
def training(request):
	if "adminid" in request.session:
		uid=request.session["adminid"]
		return render(request, 'training.html')

	else:
		return render(request, 'admin.html')
def testingpage(request):
	if "adminid" in request.session:
		uid=request.session["adminid"]
		return render(request, 'testing.html')

	else:
		return render(request, 'admin.html')

	

def userlogoutdef(request):
	try:
		del request.session['useremail']
	except:
		pass
	return render(request, 'user.html')
def adminlogoutdef(request):
	try:
		del request.session['adminid']
	except:
		pass
	return render(request, 'admin.html')	
	
def adminlogindef(request):
	return render(request, 'admin.html')

def userlogindef(request):
	return render(request, 'user.html')

def signupdef(request):
	return render(request, 'signup.html')
def usignupactiondef(request):
	email=request.POST['mail']
	pwd=request.POST['pwd']
	zip=request.POST['zip']
	name=request.POST['name']
	age=0
	gen=request.POST['gen']

		
	d=users.objects.filter(email__exact=email).count()
	if d>0:
		return render(request, 'signup.html',{'msg':"Email Already Registered"})
	else:
		d=users(name=name,email=email,pwd=pwd,zip=zip,gender=gen,age=age)
		d.save()
		return render(request, 'signup.html',{'msg':"Register Success, You can Login.."})

	return render(request, 'signup.html',{'msg':"Register Success, You can Login.."})
def userloginactiondef(request):
	if request.method=='POST':
		uid=request.POST['mail']
		pwd=request.POST['pwd']
		d=users.objects.filter(email__exact=uid).filter(pwd__exact=pwd).count()
		
		if d>0:
			d=users.objects.filter(email__exact=uid)
			request.session['useremail']=uid
			request.session['username']=d[0].name
			return render(request, 'user_home.html',{'data': d[0]})

		else:
			return render(request, 'user.html',{'msg':"Login Fail"})

	else:
		return render(request, 'user.html')
def adminloginactiondef(request):
	if request.method=='POST':
		uid=request.POST['uid']
		pwd=request.POST['pwd']
		
		if uid=='admin' and pwd=='admin':
			request.session['adminid']='admin'
			return render(request, 'admin_home.html')

		else:
			return render(request, 'admin.html',{'msg':"Login Fail"})

	else:
		return render(request, 'admin.html')

def train(request):
	if request.method=='POST':
		file=request.POST['file']
		algo=request.POST['algo']
		print(file)
		#file='D:\\Django\\Chatbot\\webapp\\'+str(file)

		
		if algo=='nb':
			NBTrain.train(file)
			
			return render(request, 'training.html',{'msg':"Naive Bayees Algorithm Trained Successfully.."})
		elif algo=='nn':
		
			NNTrain.train(file)
		
			return render(request, 'training.html',{'msg':"Nueral Network Algorithm Trained Successfully.."})
		elif algo=='svm':
		
			SVMTrain.train(file)
		
			return render(request, 'training.html',{'msg':"SVM Algorithm Trained Successfully.."})
		elif algo=='knn':
		
			KNNTrain.train(file)
		
			return render(request, 'training.html',{'msg':"KNN Algorithm Trained Successfully.."})
		elif algo=='rf':
		
			RFTrain.train(file)
		
			return render(request, 'training.html',{'msg':"Random Forest Algorithm Trained Successfully.."})

		

	else:
		return render(request, 'admin.html')

def testing(request):
	if request.method=='POST':
		file=request.POST['file']
		
		print(file)

		accuracy.objects.all().delete()



		nb=Testing.detecting(file, 'nb_model.sav')
		r=accuracy(algo='NB',accuracyv=nb)
		r.save()
		
		nn=Testing.detecting(file, 'nn_model.sav')
		r=accuracy(algo='NN',accuracyv=nn)
		r.save()
		
		svm=Testing.detecting(file, 'svm_model.sav')
		r=accuracy(algo='SVM',accuracyv=svm)
		r.save()
		
		rf=Testing.detecting(file, 'rf_model.sav')
		r=accuracy(algo='RF',accuracyv=rf)
		r.save()
		
		knn=Testing.detecting(file, 'knn_model.sav')
		r=accuracy(algo='KNN',accuracyv=knn)
		r.save()
		
		return render(request, 'testing.html',{'msg':"Testing of all algorithm completed successfully.."})

		

	else:
		return render(request, 'admin.html')



def accuracyview(request):
    if "adminid" in request.session:
        d = accuracy.objects.all()
        
        return render(request, 'viewaccuracy.html', {'data': d})

    else:
        return render(request, 'admin.html')


def viewgraph(request):
    if "adminid" in request.session:
        algos = []
        row = accuracy.objects.all()
        rlist = []
        for r in row:
            algos.append(r.algo)
            rlist.append(r.accuracyv)

        height = rlist
        # print(height)
        bars = algos
        y_pos = np.arange(len(bars))
        plt.bar(bars, height, color=['purple','blue','green','yellow', 'cyan'])
        # plt.plot( bars, height )
        plt.xlabel('Algorithms')
        plt.ylabel('Accuracy ')
        plt.title('Accuracy Measure')

        from PIL import Image 
        plt.savefig('g1.jpg')
        im = Image.open(r"g1.jpg") 
         
        im.show()
        return redirect('accuracyview')



def addq(request):
    if "adminid" in request.session:
        d = queries.objects.all()
        
        return render(request, 'queries.html', {'data': d})

    else:
        return render(request, 'admin.html')

def addquery(request):
	q=request.POST['q']
	a=request.POST['a']
	
		
	d=queries(q_n=q,an_s=a)
	d.save()
	
	d = queries.objects.all()
	return render(request, 'queries.html', {'data': d,'msg':'Query Added.'})


def chatpage(request):
	
	return render(request, 'chat0.html')

def chatpage2(request, op):

	print('--------------',op)

	request.session['imood']=op


	
	chat.objects.all().delete()
	d=chat.objects.filter().all()
	return render(request, 'chat.html',{'data': d})

def chataction(request):
	message=request.POST['message']
	uemail=request.session["useremail"]
	uname=request.session["username"]
	d=chat(name='user',email=uemail,message=message)
	d.save()


	ans='Sorry, Not Understood'

	cid=tf.calc(message)
	if cid!=-1:
		d=queries.objects.filter(id__exact=cid)
		for d1 in d:
			ans=d1.an_s

		d=chat(name='chatbot',email='chatbot',message=ans)
		d.save()

		d=chat.objects.filter().all()
		return render(request, 'chat.html',{'data': d})

	
	else:
		
		r=Prediction.do(message)
		print('.......................',r)
		r=r.strip()
		request.session['mood']=r


		
		if r=='joy':
			pass
		else:
			users.objects.filter(email = uemail).update(statu=F('statu')+1)
		if r=='joy':
			request.session['lvl']='all'
			ans="Good to know, to enhance your mood go with following link"
			d=chat(name='chatbot',email='chatbot',message=ans)
			d.save()
			users.objects.filter(email = uemail).filter(statu__gt=0).update(statu=F('statu')-1)
			request.session['type']='c'
			d=chat.objects.filter().all()
			return render(request, 'chat.html',{'data': d,'bt':True})


		else:
			d=users.objects.filter(email = uemail)
			for d1 in d:

				if int(d1.statu)>2:
					print('Consult')
					ans="I'm Sorry, Based on your situation You need to consult therapist. Please go with following URL"
					d=chat(name='chatbot',email='chatbot',message=ans)
					d.save()
					request.session['type']='t'
					d=chat.objects.filter().all()
					return render(request, 'chat.html',{'data': d,'bt':True})
				else:
					print('Content')
					if r=='anger':
						ans="Control your angry,Please go with following URL"

					elif r=='fear':
						ans="Don't fear, Please go with following URL"
					
					d=chat(name='chatbot',email='chatbot',message=ans)
					d.save()
					request.session['type']='c'
					
					
					d=chat.objects.filter().all()
					return render(request, 'chat.html',{'data': d,'bt':True})




def moredetails(request, op):

	t=request.session['type']

	if t=='t':
		d=tdetails.objects.filter().all()
		return render(request, 'therapist.html',{'data': d})
	else:
		r=request.session['mood']
		r2=request.session['imood']
		print(r,r2, t, op)
		from django.db.models import Q
		d = content.objects.filter(Q(category__icontains=r)|Q(category__icontains=r2)).filter(d_type='image').filter(category2=op).all()

		
		i=[]
		print(d)
		for d1 in d:
			d1=d1.data
			i.append(d1)

		d = content.objects.filter(Q(category__icontains=r)|Q(category__icontains=r2)).filter(d_type='music').filter(category2=op).all()
		m=[]
		for d1 in d:
			d1=d1.data
			m.append(d1)


		d = content.objects.filter(Q(category__icontains=r)|Q(category__icontains=r2)).filter(d_type='video').filter(category2=op).all()

		v=[]
		for d1 in d:
			d1=d1.data
			v.append(d1)

		print(i)


		return render(request, 'viewdata.html',{'i': i, 'm':m, 'v':v})
	return render(request, r)



def adddata(request):
	if request.method=='POST':
		cat=request.POST['cat']
		t_ype=request.POST['t_ype']
		title=request.POST['title']
		data=request.POST['data']
		cat2=request.POST['cat2']
		

		d=content(category=cat,d_type=t_ype,title=title,data=data, category2=cat2)
		d.save()

		d=content.objects.filter().all()
		return render(request, 'adddata.html',{'data': d})

	else:
		d=content.objects.filter().all()
		return render(request, 'adddata.html',{'data': d})

def addt(request):
	if request.method=='POST':
		name=request.POST['name']
		qua=request.POST['qua']
		addr=request.POST['addr']
		city=request.POST['city']
		

		d=tdetails(name=name,qualification=qua,address=addr,city=city)
		d.save()

		d=tdetails.objects.filter().all()
		return render(request, 'addt.html',{'data': d})

	else:
		d=tdetails.objects.filter().all()
		return render(request, 'addt.html',{'data': d})
