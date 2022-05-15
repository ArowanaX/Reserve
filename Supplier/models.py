import email
from unicodedata import category

from email.policy import default
from django.db import models
from django.forms import CharField
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

import uuid


from Customer.models import Profile

#---------------------------------Tags(hotel)----------------------

class Tag(models.Model):
    title = models.CharField(_("tags"), max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(_("create_at"), auto_now=False, auto_now_add=True)
    
        
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'tag'

#---------------------------------category(services and munes)----------------------  

class Category(models.Model):
    title = models.CharField(max_length=50)  
    published_at = models.DateTimeField(auto_now=False, auto_now_add=True)  
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'category' 
        

# from location_field.forms.plain import PlainLocationField

from Customer.models import Profile
from location_field.models.plain import PlainLocationField

    
#---------------------------------Residence(hotel)----------------------

class Residence(models.Model):
    
    USERNAME_FIELD = 'profile'
    REQUIRED_FIELDS = []
 
    username = None
    # is_authenticated = False
    # is_anonymous = False
    is_active = True
    #location = models.
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, unique=True, null=True, blank=True, related_name="residenceTOprofile")
    name = models.CharField(primary_key=True,max_length=20,verbose_name="res_name")
    # last_login = models.CharField(max_length=300,null=True,blank=True)
    address = models.TextField(verbose_name=_("address"))
    city = models.CharField(max_length=20,null=False,blank=False)
    img = models.ImageField(upload_to="supplier/",null=True, blank=True)
    TYPE_CHOICES = (
        ('lux', 'lux hotel'),
        ('h', 'hotel'),
        ('gh', 'guesthouse'),
    )
    type = models.CharField(max_length=10, choices = TYPE_CHOICES)
    TAG_CHOICES = (
        ('res', 'Restaurant'),
        ('lux', 'lux'),
        ('sh', 'Sports hall'),
    )
    tag = models.ManyToManyField(Tag, related_name='residenceTotag')
    service_hours_start = models.IntegerField()
    service_hours_end = models.IntegerField()
    max_reserve = models.IntegerField()
    detail = models.TextField(max_length=300,null=True,blank=True)
    # email =models.EmailField('email address')
    phone = models.CharField(max_length=12,unique=True,verbose_name="phone")
    status: models.CharField(max_length=50)
    location = PlainLocationField(based_fields=['city'], zoom=7,default=(35.687417812220446,51.37945175170898))


    def __str__(self):
        return self.name
        
    class Meta:
        db_table = 'residiance'

#------------------------------------- service card--------------------

class Service(models.Model):
    residence = models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="serviceTOroom",null=True,blank=True)
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(_("number of service"),null=True,blank=True)
    #second_id = models.IntegerField(unique=True,null=True,blank=True)
    title = models.CharField(max_length=30,null=True,blank=True)
    type = models.CharField(max_length=50,null=True,blank=True)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE ,related_name="serviceTOcategory",null=True,blank=True)
    #num_comments = models.ForeignKey(Comment, verbose_name=_("num_comments"), on_delete=models.CASCADE,related_name="servictTocomment")
    #rate = models.ForeignKey(Rate, verbose_name=_("rate"), on_delete=models.CASCADE, related_name="serviceTorate")
    img = models.ImageField(upload_to="supplier/",null=True,blank=True)
    # room_img2 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    # room_img3 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    STATE_CHOICES = (
        ('F', 'Full'),
        ('E', 'Empty'),
    )
    state = models.CharField(max_length=10, choices = STATE_CHOICES,null=True,blank=True)
    FACILITI_CHOICES = (
        ('lux', 'lux'),
        ('re', 'Refrigerator'),
        ('so', 'Sofa'),
    )
    faciliti = models.CharField(max_length=10, choices = FACILITI_CHOICES,null=True,blank=True)
    min_price = models.BigIntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'service' 

#---------------------------food menu----------------------------------
class RestaurantMenu(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=30,null=True,blank=True)
    describtion = models.TextField(null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE ,related_name="menuTOcategory",null=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name="menuTOservice",null=True,blank=True)
    residence = models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="menuTOroom",null=True,blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'menu'
        
#----------------------------Album of outdoor & indoor------------------------
    
class ResidenceOutdoorAlbum(models.Model):
    id = models.IntegerField(primary_key=True)
    residence=models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="outdootTOresident")
    img_outdoor=models.ImageField(upload_to="outdoor/",null=True, blank=True)
    img_name = models.CharField(max_length=50,null=True, blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name="outTOservice",null=True,blank=True)
    residence = models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="outTOroom",null=True,blank=True)
    menu = models.ForeignKey(RestaurantMenu,on_delete=models.CASCADE,related_name="outTOmenu",null=True,blank=True)
    
    def __str__(self):
        return self.img_name

    class Meta:
        db_table = 'outdooralbum'

class ResidenceIndoorAlbum(models.Model):
    id = models.IntegerField(primary_key=True)
    residence=models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="indootTOresident")
    img_indoor=models.ImageField(upload_to="indoor/",null=True, blank=True)
    img_name = models.CharField(max_length=50,null=True, blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name="inTOservice",null=True,blank=True)
    residence = models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="inTOroom",null=True,blank=True)
    menu = models.ForeignKey(RestaurantMenu,on_delete=models.CASCADE,related_name="inTOmenu",null=True,blank=True)
    
    def __str__(self):
        return self.img_name

    class Meta:
        db_table = 'indooralbum'
    #service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name="menuTOservice")


class Ticket(models.Model):
    title = models.CharField(max_length=30,null=False,blank=False)
    describtion = models.TextField(null=True,blank=True)
    att_file = models.FileField(upload_to = "supplier/ticket",null=True,blank=True)
    create_date = models.DateTimeField(auto_now=True,verbose_name=_('date and time'))
    status = models.BooleanField(default=True)
    residence = models.ForeignKey(Profile,on_delete=models.DO_NOTHING,related_name="TickToResidence")
    admin = models.ManyToManyField(Profile,blank=True)

    class Meta:
        verbose_name="Ticket"
        verbose_name_plural="Tickets"

    def __str__(self) -> str:
        return self.title  


class TickComment(models.Model):

    user=models.ForeignKey(Profile,null=True,on_delete=models.SET_NULL,related_name="CommentToUser",verbose_name=_("UserToTikComment"))   
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="CommentToTicket",verbose_name=_("TickToTikComment"))

    comment=models.CharField(max_length=255,verbose_name=_("comment"),help_text="کامنت خود را وارد کنید",null=True,blank=True)

    class Meta:
        verbose_name="TikComment"
        verbose_name_plural="TikComments"

    def __str__(self) -> str:
        return f"{self.user.last_name}"   


class rate(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="RateToUser",verbose_name=_("user"))
    hotel=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="RateToResidence",verbose_name=_("hotel"))
    RATE_CHOICES=[
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5")
    ] 
    rate=models.CharField(max_length=1,choices=RATE_CHOICES,verbose_name=_("rate"),help_text="امتیاز خود را وارد کنید",null=True,blank=True)

    class Meta:
        verbose_name="rate"
        verbose_name_plural="rates"

    def __str__(self) -> str:
        return f"{self.user.last_name}_{self.hotel.name}"        


class Comment(models.Model):
    user=models.ForeignKey(Profile,null=True,on_delete=models.SET_NULL,related_name="commenttouser",verbose_name=_("user"))   
    hotel=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="commenttohotel",verbose_name=_("hotel"))
    comment=models.CharField(max_length=255,verbose_name=_("comment"),help_text="کامنت خود را وارد کنید",null=True,blank=True)

    class Meta:
        verbose_name="comment"
        verbose_name_plural="comments"

    def __str__(self) -> str:
        return f"{self.user.last_name} To {self.hotel.residenceTOprofile}" 

