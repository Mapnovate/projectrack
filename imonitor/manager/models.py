#creating models for the manager app.The models will be used as the heart of the system
from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
import datetime 
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from django.template.defaultfilters import slugify

def upload_taskreports(instance, filename):
   # return "title_images/%s" % (filename)
	return '/'.join(['task_reports', str(instance.task_no), filename])

def upload_taskdetails(instance, filename):
   # return "title_images/%s" % (filename)
	return '/'.join(['task_details', str(instance.task_no), filename])

def upload_projectreports(instance, filename):
   # return "title_images/%s" % (filename)
	return '/'.join(['project_reports', str(instance.project_no), filename])

def upload_projectdetails(instance, filename):
   # return "title_images/%s" % (filename)
	return '/'.join(['project_details', str(instance.project_no), filename])

class Profile(models.Model):
	user = models.OneToOneField(User)	
	website = models.CharField(max_length=50, null=True, blank=True)
	registration_no = models.CharField(max_length=255,blank=True,null=True)   
	phone_no = models.CharField(max_length=255,blank=True,null=True)
	mobile = models.CharField(max_length=255,blank=True,null=True)
	location = models.CharField(max_length=50, null=True, blank=True)      
	postal_address = models.CharField(max_length=255,blank=True,null=True)
	physical_address = models.CharField(max_length=255,blank=True,null=True)

	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name_plural = "Profiles"

	def get_url(self):
		website = self.website
		if "http://" not in self.website and "https://" not in self.website and len(self.website) > 0:
			website = "http://" + str(self.website)
		return website 

	def get_screen_name(self):
		try:
			if self.user.get_full_name():
				return self.user.get_full_name()
			else:
				return self.user.username
		except:
			return self.user.username

   

def create_user_profile(sender, instance, created, **kwargs):
	if created == True:
		p = Profile()
		p.user = instance
		p.save()

post_save.connect(create_user_profile, sender=User)

class Departments(models.Model):
	name = models.CharField(max_length=100)
	ref_number = models.CharField(max_length=50)
	member = models.ManyToManyField('Members', through='Membership')
	slug = models.SlugField(null=True, blank=True)

	def __unicode__(self):
		return self.name
		
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)

		super(Departments, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Departments"
		managed = True

class Members(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	id_number = models.IntegerField()
	staff_number = models.CharField(max_length=50,null=True, blank=True)
	email = models.EmailField()
	telephone = PhoneNumberField()
	address = models.CharField(max_length=50, null=True, blank=True)
	department = models.ForeignKey(Departments)
	slug = models.SlugField(null=True, blank=True)
	
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)

		super(Members, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Members"
		managed = True		
			
class Projecttype(models.Model):
	name = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Projects(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	objectives = models.CharField(max_length=100)
	projecttype = models.ForeignKey(Projecttype)
	project_no = models.CharField(max_length=50)
	manager = models.ForeignKey(Members, null=True, blank=True)
	department = models.ForeignKey(Departments, null=True, blank=True)
	project_area = models.CharField(max_length=100, null=True, blank=True)	
	exepected_results = models.CharField(max_length=170, null=True, blank=True)
	project_details = models.FileField(upload_to= upload_projectdetails, null=True, help_text="Upload project details", blank=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	#member = models.ManyToManyField(Members, through='Membership', null=True, blank=True)
	team = models.ManyToManyField("Teams",through='Teamship', blank=True)
	task = models.ManyToManyField("Tasks", through='Projectship', blank=True)
	project_reports = models.FileField(upload_to= upload_projectreports, null=True, help_text="Upload project reports", blank=True)
	location = models.PointField(srid=21037,null=True,blank=True)
	slug = models.SlugField(null=True, blank=True)


	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)

		super(Projects, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Project"
		verbose_name_plural = "Projects"
		managed = True

class Projectship(models.Model):
	task = models.ForeignKey('Tasks')
	project= models.ForeignKey(Projects)
	date_started = models.DateField()
	description = models.CharField(max_length=256, null=True, blank=True)


class Roles(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
	   return self.name

class Membership(models.Model):
	#departmentprojects = models.ForeignKey('Departmentprojects')
	member = models.ForeignKey(Members)
	department = models.ForeignKey(Departments)
	#role = models.CharField(max_length=20)
	role = models.ManyToManyField(Roles, blank=True)

	class Meta:
		unique_together = (("department", "member",),)

class Teams(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100,null=True, blank=True)
	#project = models.ManyToManyField(Projects)
	#head =models.ForeignKey("Members",null=True, blank=True)
	members = models.ManyToManyField(Members, through= 'Teamship', blank=True)
	formation_date = models.DateTimeField(auto_now_add=True)
	#description = models.CharField(max_length=256, null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)

		super(Teams, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Team"
		verbose_name_plural = "Teams"
		managed = True

class Teamship(models.Model):
	member = models.ForeignKey(Members, null=True, blank=True)
	task = models.ForeignKey('Tasks', null=True, blank=True)
	project = models.ForeignKey('Projects', blank=True)
	team = models.ForeignKey(Teams, null=True, blank=True)
	job_description = models.TextField(max_length=256, null=True, blank=True)


class Tasktype(models.Model):
	name = models.CharField(max_length=50, null=True)

	def __unicode__(self):
		return self.name


class Tasks(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	objectives = models.CharField(max_length=100)
	tasktype = models.ForeignKey(Tasktype)
	task_no = models.CharField(max_length=50,unique =True)
	project = models.ForeignKey(Projects)
	task_area = models.CharField(max_length=50, null=True, blank=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	description = models.TextField(max_length=256, null=True, blank=True)
	team = models.ManyToManyField(Teams, through='Teamship', blank=True)
	manager = models.ForeignKey(Members,null=True, blank=True)
	location = models.PointField(srid=21037,null=True,blank=True)
	reports = models.FileField(upload_to= upload_taskreports, null=True, help_text="Upload task reports", blank=True)
	slug = models.SlugField(null=True, blank=True)


	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)

		super(Tasks, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Task"
		verbose_name_plural = "Tasks"
		managed = True
'''
class Departmentprojects(models.Model):
	department = models.ForeignKey(Departments)
	projects = models.ForeignKey(Projects)
	members = models.ManyToManyField(Members, through='Membership')

'''
