from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

"""Read about the difference between lazy and nonlazy translation"""


class CustomUserManager(BaseUserManager):
    
    
    def create_user(self,email,password,**extra_fields):
        """Create and save a user(can be client or worker) with email and password"""
        
        if not email:
            raise ValueError(_('The Email is not provided'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self,email,password, **extra_fields):
        
        """ Create super user for admin things"""
        
        extra_fields.setdefault('is_staff',True)        
        extra_fields.setdefault('is_active',True)   # wont login if its true        
        extra_fields.setdefault('is_superuser',True)        
        
        # if extra_fields.get('is_staff',True):
        #     raise ValueError(_('SuperUser is_staff is not True'))
        
        # if extra_fields.get('is_superuser',True):
        #     raise ValueError(_('SuperUser is_superuser is not True'))  
        
        return self.create_user(email,password,**extra_fields)      