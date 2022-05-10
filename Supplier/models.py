
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password


from Customer.models import Profile


    
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
    tag = models.CharField(max_length=10, choices = TAG_CHOICES,null=True,blank=True)
    service_hours_start = models.IntegerField()
    service_hours_end = models.IntegerField()
    max_reserve = models.IntegerField()
    detail = models.TextField(max_length=300,null=True,blank=True)
    # email =models.EmailField('email address')
    phone = models.CharField(max_length=12,unique=True,verbose_name="phone")


    def __str__(self):
        return self.name
        
    class Meta:
        db_table = 'residiance'
        
#----------------------------Album of outdoor & indoor------------------------
class ResidenceOutdoorAlbum(models.Model):
    residence=models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="outdootTOresident")
    img_outdoor=models.ImageField(upload_to="outdoor/",null=True, blank=True)

class ResidenceIndoorAlbum(models.Model):
    residence=models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="indootTOresident")
    img_indoor=models.ImageField(upload_to="indoor/",null=True, blank=True)



#------------------------------------- service card--------------------

class Service(models.Model):
    residence = models.ForeignKey(Residence,on_delete=models.CASCADE,related_name="serviceTOroom")
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=30,null=False,blank=False)
    # room_img1 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    # room_img2 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    # room_img3 = models.ImageField(upload_to="supplier/",null=True,blank=True)
    STATE_CHOICES = (
        ('F', 'Full'),
        ('E', 'Empty'),
    )
    state = models.CharField(max_length=10, choices = STATE_CHOICES)
    FACILITI_CHOICES = (
        ('lux', 'lux'),
        ('re', 'Refrigerator'),
        ('so', 'Sofa'),
    )
    faciliti = models.CharField(max_length=10, choices = FACILITI_CHOICES)
    # price = models.BigIntegerField()

    class Meta:
        db_table = 'service'

#---------------------------food menu----------------------------------
class RestaurantMenu(models.Model):
    title = models.CharField(max_length=30,null=False,blank=False)
    describtion = models.TextField(null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name="menuTOservice")


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

