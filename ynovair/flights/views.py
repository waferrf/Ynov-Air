from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Flight, Airport, Passenger, Booking, LostObject
import random
import string
from django.contrib.auth.decorators import login_required


def home(request):
    """Page d'accueil avec recherche de vols"""
    airports = Airport.objects.all()
    upcoming_flights = Flight.objects.filter(
        departure_time__gte=timezone.now(),
        status='SCHEDULED'
    ).order_by('departure_time')[:6]

    context = {
        'airports': airports,
        'upcoming_flights': upcoming_flights,
    }
    return render(request, 'flights/home.html', context)


def search_flights(request):
    """Recherche de vols"""
    flights = []

    if request.method == 'GET':
        origin_id = request.GET.get('origin')
        destination_id = request.GET.get('destination')
        date = request.GET.get('date')

        if origin_id and destination_id:
            flights = Flight.objects.filter(
                origin_id=origin_id,
                destination_id=destination_id,
                status='SCHEDULED'
            )

            if date:
                flights = flights.filter(departure_time__date=date)

            flights = flights.order_by('departure_time')

    airports = Airport.objects.all()
    context = {
        'flights': flights,
        'airports': airports,
    }
    return render(request, 'flights/search.html', context)


def flight_detail(request, flight_id):
    """Détails d'un vol"""
    flight = get_object_or_404(Flight, id=flight_id)
    context = {'flight': flight}
    return render(request, 'flights/flight_detail.html', context)

@login_required
def booking_create(request, flight_id):
    """Créer une réservation"""
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        # Créer le passager
        passenger = Passenger.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            passport_number=request.POST.get('passport_number'),
            date_of_birth=request.POST.get('date_of_birth')
        )

        # Générer une référence unique
        booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Créer la réservation
        number_of_passengers = int(request.POST.get('number_of_passengers', 1))

        if flight.available_seats >= number_of_passengers:
            booking = Booking.objects.create(
                booking_reference=booking_reference,
                flight=flight,
                passenger=passenger,
                user=request.user,
                number_of_passengers=number_of_passengers,
                total_price=flight.price * number_of_passengers,
                status='CONFIRMED'
            )

            messages.success(request, f'Réservation confirmée ! Référence: {booking_reference}')
            return redirect('booking_detail', booking_id=booking.id)
        else:
            messages.error(request, 'Pas assez de sièges disponibles.')

    context = {'flight': flight}
    return render(request, 'flights/booking_create.html', context)


def booking_detail(request, booking_id):
    """Détails d'une réservation"""
    booking = get_object_or_404(Booking, id=booking_id)
    context = {'booking': booking}
    return render(request, 'flights/booking_detail.html', context)


def my_bookings(request):
    """Liste des réservations"""
    bookings = Booking.objects.all().order_by('-booking_date')
    context = {'bookings': bookings}
    return render(request, 'flights/my_bookings.html', context)


# ============= LOST OBJECTS VIEWS =============

def lost_objects_list(request):
    """Liste de tous les objets perdus"""
    lost_objects = LostObject.objects.all()
    
    # Filtres
    category = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    if category:
        lost_objects = lost_objects.filter(category=category)
    if status:
        lost_objects = lost_objects.filter(status=status)
    if search:
        lost_objects = lost_objects.filter(
            item_name__icontains=search
        ) | lost_objects.filter(
            description__icontains=search
        ) | lost_objects.filter(
            reference_number__icontains=search
        )
    
    context = {
        'lost_objects': lost_objects,
        'categories': LostObject.CATEGORY_CHOICES,
        'statuses': LostObject.STATUS_CHOICES,
    }
    return render(request, 'flights/lost_objects_list.html', context)


def lost_object_detail(request, object_id):
    """Détails d'un objet perdu"""
    lost_object = get_object_or_404(LostObject, id=object_id)
    context = {'lost_object': lost_object}
    return render(request, 'flights/lost_object_detail.html', context)


@login_required
def lost_object_report(request):
    """Signaler un objet perdu/trouvé - Réservé aux superusers"""
    # Vérifier que l'utilisateur est un superuser
    if not request.user.is_superuser:
        messages.error(request, 'Seuls les administrateurs peuvent signaler des objets trouvés.')
        return redirect('lost_objects_list')
    
    if request.method == 'POST':
        lost_object = LostObject.objects.create(
            item_name=request.POST.get('item_name'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            color=request.POST.get('color'),
            brand=request.POST.get('brand'),
            location_found=request.POST.get('location_found'),
            flight_id=request.POST.get('flight') if request.POST.get('flight') else None,
            finder_name=request.POST.get('finder_name'),
            finder_email=request.POST.get('finder_email'),
            finder_phone=request.POST.get('finder_phone'),
            user=request.user,
            status='FOUND'
        )
        
        messages.success(request, f'Objet signalé avec succès ! Référence: {lost_object.reference_number}')
        return redirect('lost_object_detail', object_id=lost_object.id)
    
    flights = Flight.objects.filter(
        departure_time__gte=timezone.now() - timezone.timedelta(days=7)
    ).order_by('-departure_time')
    
    context = {
        'categories': LostObject.CATEGORY_CHOICES,
        'flights': flights,
    }
    return render(request, 'flights/lost_object_report.html', context)


@login_required
def lost_object_claim(request, object_id):
    """Réclamer un objet perdu"""
    lost_object = get_object_or_404(LostObject, id=object_id)
    
    # Vérifier que l'objet peut être réclamé
    if lost_object.status not in ['FOUND', 'REPORTED']:
        messages.warning(request, 'Cet objet a déjà été réclamé ou restitué.')
        return redirect('lost_object_detail', object_id=object_id)
    
    if request.method == 'POST':
        lost_object.claimer_name = request.POST.get('claimer_name')
        lost_object.claimer_email = request.POST.get('claimer_email')
        lost_object.claimer_phone = request.POST.get('claimer_phone')
        lost_object.claim_details = request.POST.get('claim_details')
        lost_object.claim_date = timezone.now()
        lost_object.status = 'CLAIMED'
        lost_object.save()
        
        messages.success(request, 'Réclamation enregistrée avec succès ! Vous serez contacté par notre équipe pour vérification.')
        return redirect('lost_object_detail', object_id=lost_object.id)
    
    context = {'lost_object': lost_object}
    return render(request, 'flights/lost_object_claim.html', context)


@login_required
def my_lost_objects(request):
    """Liste des objets perdus signalés par l'utilisateur - Réservé aux superusers"""
    # Vérifier que l'utilisateur est un superuser
    if not request.user.is_superuser:
        messages.error(request, 'Seuls les administrateurs peuvent accéder à cette page.')
        return redirect('lost_objects_list')
    
    lost_objects = LostObject.objects.filter(user=request.user).order_by('-date_found')
    context = {'lost_objects': lost_objects}
    return render(request, 'flights/my_lost_objects.html', context)
