import pyotp
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail 
from django.template.loader import render_to_string




def send_otp(request):
    username = request.POST.get('username') 
    
    #generate otp
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    otp = totp.now()
    template = render_to_string('ps_crm_app/emai-template.html', {'username': username, 'otp':otp})
    send_mail(
    "OTP for login",
    template,
    settings.EMAIL_HOST_USER,
    ["sheriffsakara112@gmail.com"],
    fail_silently=False,
    )

    # send the otp via email
    '''
    subject = 'OTP for login'
    message = f'{User.username} your otp code for login is: {otp} and it expires in 2minutes'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['sheriffsakara112@gmail.com']
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
    
    '''
    

    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_date)

    #print(f'this your otp code {otp}')