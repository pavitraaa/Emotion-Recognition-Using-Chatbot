from django.db import models
# Create your models here.


class users(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	pwd=models.CharField(max_length=100);
	zip=models.CharField(max_length=100);
	gender=models.CharField(max_length=100);
	age=models.CharField(max_length=100);
	statu=models.CharField(max_length=100);

class accuracy(models.Model):
	algo=models.CharField(max_length=100);
	accuracyv=models.FloatField(max_length=1000)

class queries(models.Model):
	q_n=models.CharField(max_length=1000);
	an_s=models.CharField(max_length=1000);

class chat(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	message=models.CharField(max_length=100);

class content(models.Model):
	category=models.CharField(max_length=100);
	d_type=models.CharField(max_length=100);
	title=models.CharField(max_length=100);
	data=models.CharField(max_length=100);
	category2=models.CharField(max_length=100)

class tdetails(models.Model):
	name=models.CharField(max_length=100);
	qualification=models.CharField(max_length=100);
	address=models.CharField(max_length=1000);
	city=models.CharField(max_length=100);
