from django.db import models

# Create your models here.

class pollStations(models.Model):
    ps_name = models.CharField(max_length=50)
    ps_code = models.CharField(max_length=50)
    serial_num = models.CharField(max_length=50)
    reg_voters = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.ps_name}")
    

class presResult(models.Model):
    CANDIDATES = {
        'John Dramani Mahama': 'John Dramani Mahama',
        'Dr. Mahamudu Bawumia': 'Dr. Mahamudu Bawumia',
        'Nana Kwame Badiako': 'Nana Kwame Badiako',
        'Alan John Kyerematen': 'Alan John Kyerematen',
        'Daniel Augustus Lartey Jr': 'Daniel Augustus Lartey Jr',
        'Akua Donkor': 'Akua Donkor',
        'Christian Kwabena Andrews': 'Christian Kwabena Andrews',
        'Mohammed Frimpong': 'Mohammed Frimpong',
        'Nana Akusua Frimpomaa' : 'Nana Akusua Frimpomaa',
        'Hassan Ayariga': 'Hassan Ayariga',
        'Kofi Koranteng': 'Kofi Koranteng',
        'Liberal Party of Ghana': 'Liberal Party of Ghana',
        'George Twum-Barima-Adu':'George Twum-Barima-Adu',
        

    }

    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
        'GCPP': 'GCPP',
        'INDEPENDENT':'INDEPENDENT',
        'GUM': 'GUM',
        'CPP':'CPP',
        'APC':'APC',
        'LPG':'LPG',
        'GFP':'GFP',
        
    }
    

   

    poll_station = models.ForeignKey(pollStations,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=CANDIDATES)
    party = models.CharField(max_length=50, choices=PARTY)
    votes = models.IntegerField()
    #added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f"{self.party} ~ {self.name}")
    
class parlResult(models.Model):
    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
        'INDEPENDENT':'INDEPENDENT',
    }

    poll_station = models.ForeignKey(pollStations,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    party = models.CharField(max_length=50, choices=PARTY)
    votes = models.IntegerField()
    #added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f"{self.party} ~ {self.name}")
    




class regPollAgent(models.Model):

    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
        'INDEPENDENT':'INDEPENDENT',
    }

    GENDER = {
        'male': 'male',
        'female':'female'
    }

    poll_station = models.ForeignKey(pollStations,on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    v_id = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER)
    party = models.CharField(max_length=100, choices=PARTY)
    registered_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f"{self.fname} {self.lname}")