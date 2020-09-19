from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


from django.core.validators import RegexValidator
from django.db.models import Q

class UserProfileManager(BaseUserManager):
  """Helps django work with our custom user model."""
  
  def create_user(self, email, phone, name, password=None):
    """Creates a new user profile object."""
    if not email:
      raise ValueError('Users must have an email address.')
    if not phone:
      raise ValueError('Users must have an phone.')

    email = self.normalize_email(email)
    user = self.model(email=email, name=name, phone=phone)

    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, email, phone, name, password):
    """Creates and saves a new superuser with givent details."""
    user = self.create_user(email, phone, name, password)

    user.is_superuser = True
    user.is_staff = True

    user.save(using=self._db)
    return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
  """Represent a user profile inside out sys."""
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message='Phone number must be in format. upto 14 digits allowed.')

  email = models.EmailField(max_length=100, unique=True)
  phone = models.CharField(validators=[phone_regex], max_length=15, unique=False, default='0000000000')
  name = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  following_services = models.TextField(default='')

  def set_service_id(self, element):
    if self.following_services:
      self.following_services = self.following_services + ',' + element
    else:
      self.following_services = element

  def get_service_ids(self):
    if self.following_services:
      return self.following_services.split(',')
    else:
      None

  objects = UserProfileManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'phone',]

  def get_full_name(self):
    """Used to get a user's full name."""
    return self.name

  def get_short_name(self):
    """Used to get a user's short name."""
    return self.name

  def __str__(self):
    """Django use this when it need to convert the object into sting."""
    return self.email

class ServiceCategories(models.Model):
  """Service Category."""

  name = models.CharField(max_length=255)
  def __str__(self):
    """Return model as a string."""

    return self.name

class Service(models.Model):
  """Service."""

  name = models.CharField(max_length=255)
  providerName = models.CharField(max_length=255)
  providerFirstName = models.CharField(max_length=255)
  cat = models.ForeignKey(ServiceCategories, on_delete=models.CASCADE)
  short_description = models.CharField(max_length=255)
  rating = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  lat = models.DecimalField(max_digits=12, decimal_places=8, default=0)
  lon = models.DecimalField(max_digits=12, decimal_places=8, default=0)

  def __str__(self):
    """Return model as a string."""

    return self.name


class PhoneOTP(models.Model):
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14$', message='Phone number must be entered in proper format.')
  phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
  otp = models.CharField(max_length=9, blank=True, null=True)
  count = models.IntegerField(default=0, help_text='Number of otp sent')
  validated = models.BooleanField(default=False, help_text='If true => means user have validated otp correctly.')

  def __str__(self):
      return str(self.phone) + ' is sent ' + str(self.otp)
  
