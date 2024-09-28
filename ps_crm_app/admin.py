from django.contrib import admin
from .models import*
# Register your models here.
admin.site.register(pollStations)
admin.site.register(presResult)
admin.site.register(parlResult)

admin.site.register(regPollAgent)