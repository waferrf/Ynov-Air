from django.contrib import admin
from django.utils import timezone
from .models import Airport, Flight, Passenger, Booking, LostObject


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'price', 'available_seats', 'status')
    list_filter = ('status', 'origin', 'destination')
    search_fields = ('flight_number',)


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'flight', 'passenger', 'booking_date', 'total_price', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('booking_reference', 'passenger__first_name', 'passenger__last_name')


@admin.register(LostObject)
class LostObjectAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'item_name', 'category', 'status', 'location_found', 'date_found', 'flight')
    list_filter = ('status', 'category', 'date_found')
    search_fields = ('reference_number', 'item_name', 'description', 'claimer_name', 'finder_name')
    readonly_fields = ('reference_number', 'created_at', 'updated_at', 'date_found')
    actions = ['mark_as_returned', 'mark_as_found']
    
    fieldsets = (
        ('Informations sur l\'objet', {
            'fields': ('item_name', 'category', 'description', 'color', 'brand')
        }),
        ('Localisation', {
            'fields': ('location_found', 'flight', 'date_found')
        }),
        ('Statut', {
            'fields': ('status', 'reference_number')
        }),
        ('Découvreur', {
            'fields': ('finder_name', 'finder_email', 'finder_phone')
        }),
        ('Réclamation', {
            'fields': ('claimer_name', 'claimer_email', 'claimer_phone', 'claim_date', 'claim_details')
        }),
        ('Restitution', {
            'fields': ('returned_date',)
        }),
        ('Système', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
    )
    
    def mark_as_returned(self, request, queryset):
        """Marquer les objets sélectionnés comme restitués"""
        updated = queryset.filter(status='CLAIMED').update(
            status='RETURNED',
            returned_date=timezone.now()
        )
        self.message_user(request, f'{updated} objet(s) marqué(s) comme restitué(s).')
    mark_as_returned.short_description = "Marquer comme restitué"
    
    def mark_as_found(self, request, queryset):
        """Remettre les objets au statut 'Trouvé'"""
        updated = queryset.update(
            status='FOUND',
            claimer_name=None,
            claimer_email=None,
            claimer_phone=None,
            claim_date=None,
            claim_details=None,
            returned_date=None
        )
        self.message_user(request, f'{updated} objet(s) remis au statut trouvé.')
    mark_as_found.short_description = "Remettre au statut trouvé"
