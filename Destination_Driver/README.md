Destination driver platform 
Destination Driver is a driver-booking platform where users can request verified drivers (with or without vehicles) for both local and safari trips.The platform connects clients and drivers, ensures transparency through ratings, and is designed to scale with advanced features like payments and geolocation.


 Backend

Django 5.x

Django REST Framework (DRF)

Simple JWT for authentication

SQLite (development) / PostgreSQL (production-ready)


Frontend

HTML, CSS, JavaScript (you may later extend to React or Vue)

Fetch API / Axios for backend communication

 Tools

Features
 Authentication

Register and login for Clients and Drivers

JWT-based secure authentication

 Trip Management

Clients can request trips (pickup, destination)

Drivers can view and accept assigned trips

Trip statuses: requested → assigned → in-progress → completed

Ratings & Profiles

Clients can rate drivers

Each user has a role-based profile (Client/Driver)
Postman for API testing

Git & GitHub for version control



 API Endpoints 
Authentication
POST /auth/register/client/ → register a client.  -Public
POST /auth/register/driver/ → register a driver.  -Public
POST /auth/login/ → login.  -Public
Profiles
GET /profile/client/{id}/ → fetch from CustomUser (role = client)
GET /profile/driver/{id}/ → fetch from DriverProfile + base user info.
PUT /profile/driver/{id}/ → update driver profile details (license, experience, etc)
Vehicles
POST /vehicles/ → add vehicle (driver only).   -Authenticated Driver (with vehicle)
GET /vehicles/{id}/ → get vehicle details.  -Authenticated Driver or Admin
Trips / Bookings
POST /trips/ → create a trip booking.  Authenticated Client
GET /trips/{id}/ → view booking details.    -Authenticated Client or Driver
PUT /trips/{id}/accept/ → driver accepts booking.     -Authenticated Driver
PUT /trips/{id}/cancel/ → client or driver cancels booking.   -Authenticated Client or Driver
GET /trips/user/{id}/ → view all bookings by a client.  -Authenticated Client
GET /trips/driver/{id}/ → view all bookings for a driver.   -Authenticated Driver
Ratings
POST /ratings/ → add rating for a trip.  -Authenticated Client
GET /ratings/driver/{id}/ → view driver’s ratings.


 
Register Client POST http://127.0.0.1:8000/api/users/users/

header- Content-Type: application/json

{

  "username": "tamim",
  "email": "tamim@example.com",
  "password": "StrongPass123",
  "role": "client"

}

POST http://127.0.0.1:8000/api/users/login/



{

  "username": "tamim",
   "password": "StrongPass123"

}



GET http://127.0.0.1:8000/api/users/logout/

Content-Type: application/json

Authorization: Bearer <your\_access\_token>





GET http://127.0.0.1:8000/api/drivers/   (LIST OF DRIVERS)





http://127.0.0.1:8000/api/trips/   POST

{

  "pickup\_location": "Nairobi CBD",

  "destination": "ATHI RIVER "

}

