from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from.models import UserDetails

# Create your views here.
def index (request):
    return render (request, 'Getcode/index.html')

def user_profile(request):
    try:
        user_details = request.user.userdetails
        user_id = user_details.unique_id
    except UserDetails.DoesNotExist:
        user_details = UserDetails.objects.create(user=request.user)
        user_id = user_details.unique_id
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return HttpResponse("An error occurred while processing your request.")

    return render(request, 'GetCode/profile.html', {'user_id': user_id})



def trade_now (request):
    return render (request, 'GetCode/trade_now.html')

@login_required
def my_center (request):
    unique_id = None  # Default to None if the user is not authenticated
    if request.user.is_authenticated:
        unique_id = request.user.unique_id

    username = request.user.username if request.user.is_authenticated else None
    return render (request, 'GetCode/my_center.html', {'unique_id':unique_id, 'username':username})


