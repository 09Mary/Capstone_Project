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

  "username": "mary\_test",

password

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

