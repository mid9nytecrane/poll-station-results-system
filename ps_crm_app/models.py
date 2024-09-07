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
        'Mahamudu Bawumia': 'Mahamudu Bawumia',
        'Nana Kwame Badiako': 'Nana Kwame Badiako',
        'Alan John Kyerematen': 'Alan John Kyerematen',
    }

    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
    }
    

   

    poll_station = models.ForeignKey(pollStations,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=CANDIDATES)
    party = models.CharField(max_length=50, choices=PARTY)
    votes = models.IntegerField()

    def __str__(self):
        return (f"{self.party} ~ {self.name}")
    
class parlResult(models.Model):
    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
    }

    poll_station = models.ForeignKey(pollStations,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    party = models.CharField(max_length=50, choices=PARTY)
    votes = models.IntegerField()


    def __str__(self):
        return (f"{self.party} ~ {self.name}")