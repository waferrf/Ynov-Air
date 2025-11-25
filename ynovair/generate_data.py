"""
Script pour générer des données de test pour l'application Ynov Air
Génère 50 entrées pour chaque modèle: Passenger, Flight, Booking, LostObject
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from flights.models import Airport, Flight, Passenger, Booking, LostObject


# Données pour la génération aléatoire
FIRST_NAMES = [
    'Mohammed', 'Sarah', 'Pierre', 'Marie', 'Lucas', 'Emma', 'Thomas', 'Léa',
    'Hugo', 'Chloé', 'Louis', 'Manon', 'Nathan', 'Camille', 'Maxime', 'Laura',
    'Alexandre', 'Julie', 'Antoine', 'Sophie', 'Julien', 'Amélie', 'Nicolas',
    'Charlotte', 'Romain', 'Mathilde', 'Théo', 'Zoé', 'Gabriel', 'Alice',
    'Arthur', 'Inès', 'Adam', 'Lola', 'Baptiste', 'Jade', 'Enzo', 'Anaïs',
    'Paul', 'Clara', 'Raphaël', 'Léna', 'Victor', 'Lucie', 'Clément', 'Marine',
    'Tom', 'Lisa', 'Valentin', 'Océane'
]

LAST_NAMES = [
    'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit',
    'Durand', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel',
    'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier', 'Morel',
    'Girard', 'André', 'Lefevre', 'Mercier', 'Dupont', 'Lambert', 'Bonnet',
    'François', 'Martinez', 'Legrand', 'Garnier', 'Faure', 'Rousseau', 'Blanc',
    'Guerin', 'Muller', 'Henry', 'Roussel', 'Nicolas', 'Perrin', 'Morin',
    'Mathieu', 'Clement', 'Gauthier', 'Dumont', 'Lopez', 'Fontaine', 'Chevalier',
    'Robin'
]

ITEM_NAMES = [
    'iPhone 15', 'Samsung Galaxy S24', 'MacBook Pro', 'iPad Air', 'AirPods Pro',
    'Sac à dos noir', 'Valise rouge', 'Portefeuille en cuir', 'Lunettes de soleil Ray-Ban',
    'Montre Rolex', 'Passeport français', 'Carte d\'identité', 'Livre "Le Petit Prince"',
    'Veste en jean', 'Parapluie bleu', 'Écharpe en laine', 'Clés de voiture',
    'Appareil photo Canon', 'Nintendo Switch', 'Kindle', 'Casque Bose',
    'Chargeur iPhone', 'Tablette Samsung', 'Ordinateur portable Dell', 'Souris sans fil',
    'Carte bancaire', 'Bijoux en or', 'Bague de fiançailles', 'Bracelet Pandora',
    'Parfum Chanel', 'Sac à main Louis Vuitton', 'Chemise blanche', 'Pantalon noir',
    'Chaussures Nike', 'Ceinture Hermès', 'Cravate en soie', 'Cahier moleskine',
    'Stylo Mont Blanc', 'Agenda 2025', 'Carte de transport', 'Badge entreprise',
    'Télécommande', 'Jouet enfant', 'Peluche', 'Casquette', 'Gants en cuir',
    'Foulard', 'Broche', 'Collier', 'Boucles d\'oreilles'
]

COLORS = ['Noir', 'Blanc', 'Rouge', 'Bleu', 'Vert', 'Jaune', 'Orange', 'Rose', 'Violet', 'Gris', 'Marron', 'Beige']

BRANDS = [
    'Apple', 'Samsung', 'Nike', 'Adidas', 'Louis Vuitton', 'Gucci', 'Hermès',
    'Chanel', 'Prada', 'Dior', 'Zara', 'H&M', 'Uniqlo', 'Lacoste', 'Boss',
    'Canon', 'Sony', 'Dell', 'HP', 'Lenovo', 'Bose', 'JBL', 'Ray-Ban',
    'Oakley', 'Rolex', 'Casio', 'Fossil', 'Michael Kors', 'Pandora'
]

LOCATIONS = [
    'Terminal 1 - Salle d\'embarquement', 'Terminal 2 - Porte 15', 'Terminal 3 - Zone d\'attente',
    'Salon VIP', 'Zone de récupération des bagages', 'Boutique duty-free',
    'Restaurant Terminal 1', 'Toilettes Terminal 2', 'Parking P3',
    'Zone d\'enregistrement', 'Contrôle de sécurité', 'Tapis roulant A',
    'Salle d\'attente porte 23', 'Passerelle d\'embarquement', 'Hall d\'arrivée',
    'Zone commerciale', 'Point information', 'Café Starbucks', 'McDo Terminal 2',
    'Pharmacie de l\'aéroport'
]


def create_passengers(count=50):
    """Créer des passagers"""
    print(f"Création de {count} passagers...")
    passengers = []
    
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        
        passenger = Passenger.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}{i}@email.com",
            phone=f"0{random.randint(600000000, 799999999)}",
            passport_number=f"{random.choice(['FR', 'BE', 'ES', 'IT', 'DE'])}{random.randint(100000, 999999)}",
            date_of_birth=datetime.now().date() - timedelta(days=random.randint(6570, 25550))  # 18-70 ans
        )
        passengers.append(passenger)
    
    print(f"✓ {len(passengers)} passagers créés")
    return passengers


def create_flights(count=50):
    """Créer des vols"""
    print(f"Création de {count} vols...")
    
    # Récupérer tous les aéroports
    airports = list(Airport.objects.all())
    if len(airports) < 2:
        print("⚠ Pas assez d'aéroports. Création d'aéroports de test...")
        airports = create_airports()
    
    flights = []
    statuses = ['SCHEDULED', 'BOARDING', 'DEPARTED', 'LANDED', 'CANCELLED']
    
    for i in range(count):
        origin = random.choice(airports)
        destination = random.choice([a for a in airports if a != origin])
        
        # Date de départ aléatoire (entre -7 et +30 jours)
        days_offset = random.randint(-7, 30)
        departure_time = timezone.now() + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        # Durée du vol (1h à 12h)
        duration = timedelta(hours=random.randint(1, 12), minutes=random.choice([0, 15, 30, 45]))
        arrival_time = departure_time + duration
        
        # Sièges
        total_seats = random.choice([150, 180, 200, 250, 300])
        available_seats = random.randint(0, total_seats)
        
        # Prix
        price = Decimal(random.randint(50, 800))
        
        # Statut (plus de vols programmés que d'autres statuts)
        if days_offset > 0:
            status = 'SCHEDULED'
        elif days_offset == 0:
            status = random.choice(['SCHEDULED', 'BOARDING'])
        else:
            status = random.choice(statuses)
        
        flight = Flight.objects.create(
            flight_number=f"YA{random.randint(1000, 9999)}",
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration,
            available_seats=available_seats,
            total_seats=total_seats,
            price=price,
            status=status
        )
        flights.append(flight)
    
    print(f"✓ {len(flights)} vols créés")
    return flights


def create_airports():
    """Créer des aéroports de base si nécessaire"""
    airports_data = [
        {'code': 'CDG', 'name': 'Charles de Gaulle', 'city': 'Paris', 'country': 'France'},
        {'code': 'ORY', 'name': 'Orly', 'city': 'Paris', 'country': 'France'},
        {'code': 'LYS', 'name': 'Lyon-Saint Exupéry', 'city': 'Lyon', 'country': 'France'},
        {'code': 'MRS', 'name': 'Marseille Provence', 'city': 'Marseille', 'country': 'France'},
        {'code': 'NCE', 'name': 'Côte d\'Azur', 'city': 'Nice', 'country': 'France'},
        {'code': 'TLS', 'name': 'Toulouse-Blagnac', 'city': 'Toulouse', 'country': 'France'},
        {'code': 'BCN', 'name': 'Barcelona-El Prat', 'city': 'Barcelona', 'country': 'Spain'},
        {'code': 'MAD', 'name': 'Adolfo Suárez Madrid-Barajas', 'city': 'Madrid', 'country': 'Spain'},
        {'code': 'FCO', 'name': 'Leonardo da Vinci-Fiumicino', 'city': 'Rome', 'country': 'Italy'},
        {'code': 'LHR', 'name': 'Heathrow', 'city': 'London', 'country': 'United Kingdom'},
    ]
    
    airports = []
    for data in airports_data:
        airport, created = Airport.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        airports.append(airport)
    
    return airports


def create_bookings(passengers, flights, count=50):
    """Créer des réservations"""
    print(f"Création de {count} réservations...")
    bookings = []
    
    # Créer un utilisateur de test si nécessaire
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    statuses = ['PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED']
    
    for i in range(count):
        passenger = random.choice(passengers)
        flight = random.choice(flights)
        
        number_of_passengers = random.randint(1, 4)
        total_price = flight.price * number_of_passengers
        
        # Statut basé sur le statut du vol
        if flight.status == 'SCHEDULED':
            status = random.choice(['PENDING', 'CONFIRMED'])
        elif flight.status in ['DEPARTED', 'LANDED']:
            status = random.choice(['CONFIRMED', 'COMPLETED'])
        else:
            status = random.choice(statuses)
        
        # Générer une référence unique
        booking_ref = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        
        booking = Booking.objects.create(
            booking_reference=booking_ref,
            flight=flight,
            passenger=passenger,
            user=user,
            number_of_passengers=number_of_passengers,
            total_price=total_price,
            status=status,
            seat_number=f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
        )
        bookings.append(booking)
    
    print(f"✓ {len(bookings)} réservations créées")
    return bookings


def create_lost_objects(flights, count=50):
    """Créer des objets perdus"""
    print(f"Création de {count} objets perdus...")
    
    # Créer un superuser si nécessaire
    superuser, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@ynovair.com', 'is_superuser': True, 'is_staff': True}
    )
    if created:
        superuser.set_password('admin123')
        superuser.save()
    
    lost_objects = []
    categories = [choice[0] for choice in LostObject.CATEGORY_CHOICES]
    statuses = [choice[0] for choice in LostObject.STATUS_CHOICES]
    
    for i in range(count):
        item_name = random.choice(ITEM_NAMES)
        category = random.choice(categories)
        
        # Description plus détaillée
        descriptions = [
            f"{item_name} en bon état, trouvé dans {random.choice(LOCATIONS)}",
            f"{item_name} avec quelques rayures, couleur {random.choice(COLORS).lower()}",
            f"{item_name} neuf, encore dans son emballage",
            f"{item_name} usagé mais fonctionnel",
            f"{item_name} avec accessoires inclus"
        ]
        
        # Date de découverte (entre -30 et aujourd'hui)
        days_ago = random.randint(0, 30)
        
        # Statut (plus d'objets trouvés que réclamés)
        status_weights = [0.1, 0.6, 0.25, 0.05]  # REPORTED, FOUND, CLAIMED, RETURNED
        status = random.choices(statuses, weights=status_weights)[0]
        
        lost_object = LostObject(
            item_name=item_name,
            category=category,
            description=random.choice(descriptions),
            color=random.choice(COLORS) if random.random() > 0.3 else None,
            brand=random.choice(BRANDS) if random.random() > 0.4 else None,
            location_found=random.choice(LOCATIONS),
            flight=random.choice(flights) if random.random() > 0.3 else None,
            status=status,
            finder_name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            finder_email=f"finder{i}@email.com",
            finder_phone=f"0{random.randint(600000000, 799999999)}",
            user=superuser
        )
        
        # Sauvegarder pour générer le numéro de référence
        lost_object.save()
        
        # Modifier la date de découverte
        lost_object.date_found = timezone.now() - timedelta(days=days_ago)
        
        # Si l'objet a été réclamé, ajouter les infos du réclamant
        if status in ['CLAIMED', 'RETURNED']:
            lost_object.claimer_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            lost_object.claimer_email = f"claimer{i}@email.com"
            lost_object.claimer_phone = f"0{random.randint(600000000, 799999999)}"
            lost_object.claim_date = lost_object.date_found + timedelta(days=random.randint(1, 5))
            lost_object.claim_details = f"C'est bien mon {item_name}. Je l'ai perdu le {lost_object.date_found.strftime('%d/%m/%Y')}. Il a un {random.choice(['autocollant', 'scratch', 'marque distinctive', 'numéro de série'])} spécifique."
        
        # Si l'objet a été restitué, ajouter la date
        if status == 'RETURNED':
            lost_object.returned_date = lost_object.claim_date + timedelta(days=random.randint(1, 3))
        
        lost_object.save()
        lost_objects.append(lost_object)
    
    print(f"✓ {len(lost_objects)} objets perdus créés")
    return lost_objects


def main():
    """Fonction principale"""
    print("="*60)
    print("GÉNÉRATION DE DONNÉES DE TEST POUR YNOV AIR")
    print("="*60)
    print()
    
    # Créer les données
    passengers = create_passengers(50)
    flights = create_flights(50)
    bookings = create_bookings(passengers, flights, 50)
    lost_objects = create_lost_objects(flights, 50)
    
    print()
    print("="*60)
    print("RÉSUMÉ")
    print("="*60)
    print(f"Passagers créés      : {len(passengers)}")
    print(f"Vols créés           : {len(flights)}")
    print(f"Réservations créées  : {len(bookings)}")
    print(f"Objets perdus créés  : {len(lost_objects)}")
    print()
    print("✓ Génération terminée avec succès!")
    print("="*60)


if __name__ == '__main__':
    main()
