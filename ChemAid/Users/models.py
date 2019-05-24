from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# accounts.models.py

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, student_number, contact_no, course, year_lvl, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not student_number:
            raise ValueError('Users must have a student number')
        if not contact_no:
            raise ValueError('Users must have a contact_no')
        if not course:
            raise ValueError('Users must have a course')
        if not year_lvl:
            raise ValueError('Users must have a year_lvl')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            student_number=student_number,
            contact_no=contact_no,
            course=course,
            year_lvl=year_lvl,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, student_number, contact_no, course, year_lvl, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name, 
            last_name, 
            student_number, 
            contact_no, 
            course, 
            year_lvl,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, student_number, contact_no, course, year_lvl, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name, 
            last_name, 
            student_number, 
            contact_no, 
            course, 
            year_lvl,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    YEAR_IN_SCHOOL_CHOICES = (
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
        ('Graduate', 'Graduate'),
    )
    COURSE_CHOICES = (
        ('Biology', 'Biology'),
        ('Computer Science', 'Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('Political Science', 'Political Science'),
        ('Psychology', 'Psychology'),
        ('Communications', 'Communications'),
        ('Fine Arts', 'Fine Arts'),
        ('Management', 'Management'),
    )
    first_name = models.CharField(max_length=100, blank = True, null=True)
    last_name = models.CharField(max_length=100, blank = True, null=True)
    student_number = models.CharField(max_length=20, blank = True, null=True)
    contact_no = models.CharField(max_length=11, blank = True, null=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    year_lvl = models.CharField(max_length=20, choices=YEAR_IN_SCHOOL_CHOICES)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(null=True) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'student_number', 'contact_no', 'course', 'year_lvl'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    objects = UserManager()
  
class updateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
    student_number = models.CharField(max_length=30, null = True)

    def __str__(self):
        return f'{self.user.username} Profile'  

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
    student_number = models.CharField(max_length=30, null = True)

    def __str__(self):
        return f'{self.user.email} Profile'  
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=2550)
    count = models.IntegerField(default=0)