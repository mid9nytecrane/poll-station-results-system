from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .models import pollStations,presResult, parlResult
from .forms import pollStationForm,presResultForm,parlResultForm, SignupForm
from django.db.models import Sum,Q

# Create your views here.

def dashboard_page(request):
    poll_station = pollStations.objects.annotate(total_valid_votes=Sum('presresult__votes'))
    c_total_valid_votes= poll_station.aggregate(total_valid_votes_all=Sum('total_valid_votes')).get('total_valid_votes_all') or 0
    #total calculate the number of registered voters
    #it takes every number of registered votes from each poll station and sum them 
    #and stores them in total_registered_voters
    total_registered_voters = pollStations.objects.aggregate(total=Sum('reg_voters')).get('total') or 0
    #total rejected votes for all poll stations
    c_rejected_votes = total_registered_voters - c_total_valid_votes
    
    #getting the total valid for npp in presidential type election 
    npp_valid_votes = pollStations.objects.annotate(
    npp_valid_votes=Sum('presresult__votes', filter=Q(presresult__party='NPP'))
    ).aggregate(Sum('npp_valid_votes'))['npp_valid_votes__sum'] or 0
    
    #calculating the percentage for npp
    npp_percentage = (npp_valid_votes / c_total_valid_votes) * 100 

    #getting the total valid votes for ndc in presidential type election
    ndc_valid_votes = pollStations.objects.annotate(
    ndc_valid_votes=Sum('presresult__votes', filter=Q(presresult__party='NDC'))
    ).aggregate(Sum('ndc_valid_votes'))['ndc_valid_votes__sum'] or 0
    #calculating the percentage for ndc
    ndc_percentage = (ndc_valid_votes / c_total_valid_votes) * 100 


    #getting the total valid votes for new force in presidential type election
    new_force_valid_votes = pollStations.objects.annotate(
        new_force_valid_votes=Sum('presresult__votes', filter=Q(presresult__party='NEW FORCE'))
    ).aggregate(Sum('new_force_valid_votes'))['new_force_valid_votes__sum'] or 0 

    #new force percentage 
    new_force_percentage = (new_force_valid_votes / c_total_valid_votes) * 100

    
    #getting the total valid votes for movement for change 

    movement_for_change_valid_votes = pollStations.objects.annotate(
    movement_for_change_valid_votes=Sum('presresult__votes', filter=Q(presresult__party='MOVEMENT FOR CHANGE'))
    ).aggregate(Sum('movement_for_change_valid_votes'))['movement_for_change_valid_votes__sum'] or 0

    #MOVEMENT FOR CHANGE percentage
    movement_for_change_percentage = (movement_for_change_valid_votes / c_total_valid_votes) * 100

    #list of party percentages and labels for presidential type election
    party_data = [npp_percentage, ndc_percentage,new_force_percentage,movement_for_change_percentage]
    party_labels = ['NPP','NDC','NEW FORCE', 'MOVEMENT FOR CHANGE']


    #parliamentary type election
    

    parl_total_valid_votes = pollStations.objects.annotate(parl_total_valid_votes=Sum('parlresult__votes')).aggregate(Sum('parl_total_valid_votes'))['parl_total_valid_votes__sum'] or 0
    
    #getting the total valid votes for ndc in parliamentary type election
    parl_ndc_valid_votes = pollStations.objects.annotate(parl_ndc_valid_votes=Sum('parlresult__votes',filter=Q(parlresult__party='NDC'))).aggregate(Sum('parl_ndc_valid_votes'))['parl_ndc_valid_votes__sum'] or 0

    #NDC PERCENTAGE FOR PARLIAMENTARY 
    parl_ndc_percentage = (parl_ndc_valid_votes / parl_total_valid_votes)  * 100


    #getting the total valid votes for npp in parliamentary type election
    parl_npp_valid_votes = pollStations.objects.annotate(
        parl_npp_valid_votes=Sum('parlresult__votes', filter=Q(parlresult__party='NPP'))
    ).aggregate(Sum('parl_npp_valid_votes'))['parl_npp_valid_votes__sum'] or 0

    #NPP PERCENTAGE FOR PARLIAMENTARY
    parl_npp_percentage = (parl_npp_valid_votes / parl_total_valid_votes) * 100

    #getting the total votes for independent candidate for parliamentary type election
    independent = pollStations.objects.annotate(
        independent=Sum('parlresult__votes',filter=Q(parlresult__party='INDEPENDENT'))
    ).aggregate(Sum('independent'))['independent__sum'] or 0

    #percentage for independent candidate
    independent_percentage = (independent/parl_total_valid_votes) * 100


    #parliamentary data list and labels
    parl_party_data = [parl_npp_percentage,parl_ndc_percentage, independent_percentage]
    parl_party_labels = ['NPP','NDC','INDEPENDENT']

    #getting the total valid for PRESIDENTIAL
    total_pres_votes = npp_valid_votes + ndc_valid_votes + new_force_valid_votes + movement_for_change_valid_votes

    #getting the total valid for PARLIAMENTARY 
    #total_parl_votes = parl_npp_valid_votes + parl_ndc_valid_votes
    total_parl_votes = parl_total_valid_votes

    station = pollStations.objects.all()
    station_count = station.count
    p_results = presResult.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You have logged In as {user}'.title())
            return redirect('dashboard')
        else:   
            messages.success(request, 'Invalid username or password'.title())
            return redirect('dashboard')
    else:
        return render(request,'ps_crm_app/dashboard_page.html',{'station_count':station_count, 'p_results':p_results, 'total_registered_voters':total_registered_voters, 'c_total_valid_votes':c_total_valid_votes, 'c_rejected_votes':c_rejected_votes, 'parl_total_valid_votes':parl_total_valid_votes, 'party_data':party_data, 'party_labels':party_labels, 'parl_party_data':parl_party_data, 'parl_party_labels':parl_party_labels, 'total_pres_votes':total_pres_votes, 'total_parl_votes':total_parl_votes,})
    

def logout_user(request):
    logout(request)
    messages.success(request, 'You Have been logged out...'.title())
    return redirect('dashboard')


#registring a user 
def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been registered successfully'.title())
            return redirect('logout')
    return render(request, 'ps_crm_app/register.html', {'form':form})

#adding of polling stations 
def add_poll_stations(request):
    form = pollStationForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method ==  'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Poll station has been added'.title())
                return redirect('poll_station')
        else:        
            return render(request,'ps_crm_app/add_pollstation_form.html', {'form':form})
    else:
        messages.success(request, 'you must be logged in to add a poll station.title())')
        return redirect('poll_station') 


#showing polling station page
def poll_station(request):
    stations = pollStations.objects.all()
    
    context = {
        'stations':stations,
        
    }
    return render(request, 'ps_crm_app/poll_stations.html',context)


def poll_station_view(request, station_id):
    if request.user.is_authenticated:
        poll_station = pollStations.objects.get(id=station_id)
        
        data_entries = presResult.objects.filter(poll_station=poll_station)
        parl_results = parlResult.objects.filter(poll_station=poll_station)

        valid_votes = data_entries.aggregate(total_votes=Sum('votes'))
        

        
        if 'total_votes' in valid_votes and valid_votes['total_votes'] is not None:
            registered_voters = poll_station.reg_voters
            rejected_votes = registered_voters - valid_votes['total_votes']
        else:
            rejected_votes = 0
            valid_votes['total_votes'] = 0
        context = {
            'poll_station':poll_station,
            'data_entries':data_entries,
            'parl_results':parl_results,
            'valid_votes':valid_votes['total_votes'],
            'rejected_votes':rejected_votes,
           
            
        }
        
        return render(request,'ps_crm_app/poll_station_view.html',context)
    else:
        messages.success(request, 'you have to login to view this page')
        return redirect('dashboard')
    

#adding results for presidential type election
def add_pres_result(request, station_id):
    poll_station = pollStations.objects.get(id=station_id)
    #poll_station = get_object_or_404(pollStations.objects.get(id=station_id))
    if request.method == 'POST':
        form = presResultForm(request.POST)
        if form.is_valid():
            pres_data = form.save(commit=False)
            pres_data.poll_station = poll_station
            pres_data.save()
            messages.success(request, 'results have been added presidential'.title())
            return redirect('poll',station_id=poll_station.id)
       
    else:
        form = presResultForm()
        return render(request, 'ps_crm_app/pres_form.html',{
            'form':form,
            'poll_station':poll_station,
        })
    

#adding parliamentary results 

def add_parl_result(request, station_id):
    poll_station = pollStations.objects.get(id=station_id)
    #poll_station = get_object_or_404(pollStations.objects.get(id=station_id))
    if request.method == 'POST':
        form = parlResultForm(request.POST)
        if form.is_valid():
            parl_data = form.save(commit=False)
            parl_data.poll_station = poll_station
            parl_data.save()
            messages.success(request, f"results have been added to parliamentary".title())
            return redirect('poll',station_id=poll_station.id)
       
    else:
        form = parlResultForm()
        return render(request, 'ps_crm_app/parl_form.html',{
            'form':form,
            'poll_station':poll_station,
        })
    

#updating pollstations
def update_pollstation(request, station_id):
    
    if request.user.is_authenticated:
        current_poll_station = pollStations.objects.get(id=station_id)
        form = pollStationForm(request.POST or None, instance=current_poll_station)
        if form.is_valid():
            form.save()
            messages.success(request, f'{current_poll_station} poll station updated successfully'.title())
            return redirect('poll_station')
        else:
            return render(request, 'ps_crm_app/update_pollstation.html', {'form':form, 'current_poll_station': current_poll_station})
    else:
        messages.success(request, 'you have to be logged in before you can view this page'.title())
        return redirect('poll_station')
    
#deleting poll station
def delete_pollstation(request,station_id):
    if request.user.is_authenticated:
        poll_station = pollStations.objects.get(id=station_id)
        if request.method == 'POST':
            
            poll_station.delete()
            messages.success(request, f'{poll_station} poll station has been deleted'.title())
            return redirect('poll_station',)
        context = {
            'poll_station':poll_station,
        }
        return render(request, 'ps_crm_app/delete_pollstation.html', context)
    else:
        messages.success(request, 'you have to be logged in before you can view this page'.title())
        return redirect('poll_station')
    


#updating presidential content or record
def update_presidential(request, station_id, pres_id):
    if request.user.is_authenticated:
        poll_station = pollStations.objects.get(id=station_id)
        
        cp = presResult.objects.get(id=pres_id)
        form = presResultForm(request.POST or None, instance=cp)
        if form.is_valid():
            form.save()
            messages.success(request, f'{poll_station} presidential results updated successfully'.title())
            return redirect('poll',station_id=poll_station.id)
        else:
            return render(request,'ps_crm_app/updatePresidential.html', {'form':form, 'poll_station':poll_station})
    else:
        messages.success(request, 'you have to be logged in before you can view this page'.title())
        return redirect('poll',station_id=poll_station.id)


#deleting presidential content or record 
def delete_presidential(request, station_id, pres_id):
    
    if request.user.is_authenticated:
        current_presidential = pollStations.objects.get(id=station_id)
        delete_pres_record = presResult.objects.get(id=pres_id)
        if request.method == 'POST':
            delete_pres_record.delete()
            return redirect('poll',station_id=current_presidential.id)
        return render(request,'ps_crm_app/delete_pres_record.html', {'delete_pres_record':delete_pres_record, 'current_presidential':current_presidential})
    
    else:
        messages.success(request, 'you have to be logged in before you can view this page'.title())
        return redirect('poll',station_id=poll_station.id)
        


#updating parliamentary results 
def update_parliamentary(request, station_id, parl_id):
    if request.user.is_authenticated:
        poll_station = pollStations.objects.get(id=station_id)
        current_record = parlResult.objects.get(id=parl_id)
        form = parlResultForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, f'{poll_station} parliamentary results updated successfully'.title())
            return redirect('poll',station_id=poll_station.id)
        else:

            return render(request, 'ps_crm_app/update_parl_results.html',{
                'form':form,
                'poll_station':poll_station,
            })
    else:
        messages.success(request, 'you have to be logged in before you can view this page'.title())
        return redirect('poll',station_id=poll_station.id)
    

#deleting parliamentary results 
def delete_parliamentary(request, station_id, parl_id):
    if request.user.is_authenticated:
        current_parl = pollStations.objects.get(id=station_id)
        delete_parl_record = parlResult.objects.get(id=parl_id)
        if request.method == 'POST':
            delete_parl_record.delete()
            messages.success(request, f"{delete_parl_record} has been deleted ".title())
            return redirect('poll',station_id=current_parl.id)
       
        return render(request, 'ps_crm_app/delete_parl_record.html', {
            'delete_parl_record':delete_parl_record,
            'current_parl': current_parl,
        })
    else:
        messages.success(request, 'you have to be logged in before you can view this page'.title())
        return redirect('poll',station_id=poll_station.id)
        