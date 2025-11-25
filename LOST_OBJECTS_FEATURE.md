# Lost Objects Management Feature

## Overview
A complete lost and found objects management system has been added to the Ynov-Air application, allowing users to report found items and claim lost belongings.

## Features

### 1. **Database Model - LostObject**
Located in `flights/models.py`, includes:
- **Item Information**: name, category, description, color, brand
- **Location Details**: location found, associated flight, date found
- **Status Tracking**: REPORTED, FOUND, CLAIMED, RETURNED
- **Contact Information**: 
  - Finder details (name, email, phone)
  - Claimer details (name, email, phone, claim details)
- **Reference System**: Auto-generated unique reference number (LO + 6 digits)
- **Timestamps**: created_at, updated_at, date_found, claim_date, returned_date
- **User Association**: Links to Django User model

### 2. **Categories**
- Electronics (Électronique)
- Documents
- Luggage (Bagages)
- Clothing (Vêtements)
- Accessories (Accessoires)
- Jewelry (Bijoux)
- Books (Livres)
- Other (Autre)

### 3. **Views & Functionality**
Located in `flights/views.py`:
- **`lost_objects_list`**: Browse all lost objects with filters (category, status, search)
- **`lost_object_detail`**: View detailed information about a specific object
- **`lost_object_report`**: Report a found object (requires login)
- **`lost_object_claim`**: Claim a lost object with proof of ownership (requires login)
- **`my_lost_objects`**: View user's reported objects (requires login)

### 4. **URL Routes**
Added to `flights/urls.py`:
- `/lost-objects/` - List all lost objects
- `/lost-objects/<id>/` - View object details
- `/lost-objects/report/` - Report a found object
- `/lost-objects/<id>/claim/` - Claim an object
- `/my-lost-objects/` - View my reported objects

### 5. **Templates**
Created in `templates/flights/`:
- `lost_objects_list.html` - Browse and filter lost objects
- `lost_object_detail.html` - Detailed view with claim option
- `lost_object_report.html` - Form to report found objects
- `lost_object_claim.html` - Form to claim an object
- `my_lost_objects.html` - User's reported objects dashboard

### 6. **Admin Interface**
Enhanced admin panel (`flights/admin.py`) with:
- List display: reference, item name, category, status, location, date
- Filters: status, category, date found
- Search: reference number, item name, description, claimer/finder names
- Organized fieldsets for easy management
- Read-only fields: reference_number, timestamps

### 7. **Navigation**
Updated `base.html` to include:
- "Objets perdus" link in main navigation
- Easy access from any page

## User Workflow

### For Finding Objects:
1. User logs in
2. Navigates to "Objets perdus"
3. Clicks "Signaler un objet trouvé"
4. Fills in object details, location, and contact info
5. Receives unique reference number
6. Object appears in lost objects list

### For Claiming Objects:
1. User browses lost objects list
2. Finds their item
3. Clicks "Réclamer cet objet"
4. Provides contact info and proof of ownership
5. Status changes to "CLAIMED"
6. Staff reviews and contacts user for verification

### For Staff:
1. Access Django admin panel
2. View all lost objects
3. Manage claims and update statuses
4. Mark as RETURNED when object is given back

## Database Migration
- Migration file: `flights/migrations/0003_lostobject.py`
- Successfully applied to database

## Key Features
✅ Complete CRUD operations
✅ User authentication integration
✅ Advanced filtering and search
✅ Status workflow (FOUND → CLAIMED → RETURNED)
✅ Contact information management
✅ Flight association
✅ Auto-generated reference numbers
✅ Responsive design
✅ Admin panel integration

## Technical Details
- Uses Django's built-in User model
- Leverages Django ORM for queries
- Bootstrap 5 for responsive UI
- Font Awesome icons for better UX
- Form validation and CSRF protection
- Login required for sensitive operations

## Future Enhancements (Optional)
- Email notifications when objects are claimed
- Image upload for found objects
- Advanced analytics dashboard
- Export functionality for reports
- Multi-language support
- SMS notifications
