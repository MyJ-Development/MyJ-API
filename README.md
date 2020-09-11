# MyJ-API
Peticiones POST (JSON) Todas las peticiones requieren un bearer token (access_token) otorgado al hacer login

http://IP:PORT/api/auth/sign-up
{
    "email":"test@test.test",
    "password":"test",
    "fullName":"testing"
}

http://IP:PORT/api/auth/login
{
    "email": "test@test.test",
    "password": "test"
}

http://IP:PORT/api/scheduler/technician
{
    "comuna":"Comuna",
    "rut":"123456789",
    "nombre":"nombre",
    "capacidad":"7",
    "estado":"No disponible"
}

http://IP:PORT/api/scheduler/client
{
    "rut":"987654321",
    "email":"asdas@asda.com",
    "nombre":"testing",
    "contacto1":"1231233",
    "contacto2":"1231232",
    "created_by": "test@test.test", //Correo del usuario actual
    "updated_by": "test@test.test"  //Correo del usuario actual
}

http://IP:PORT/api/scheduler/residence
{
    "comuna":"Comuna",
    "direccion":"direccion",
    "mac":"mac",
    "pppoe":"pppoe"
}

http://IP:PORT/api/scheduler/order
{
    "tipo":"Instalacion",
    "prioridad":"Primera del dia",
    "disponibilidad":"despues 10 am",
    "comentario":"comentarioo",
    "fechaejecucion":"2020-05-3 15:23:00",
    "estadocliente": "No aplicable",
    "estadoticket": "No aplicable",
    "mediodepago": "Imported",
    "monto": "0",
    "created_by":"test@test.test", //Correo del usuario actual
    "encargado":"123456789",      //Rut tecnico encargado
    "client_order": "987654321"   //Rut cliente de la orden
}


Peticiones GET Todas las peticiones requieren un bearer token (access_token) otorgado al hacer login

http://IP:PORT/api/scheduler/order
{
    "id":"1"
}

http://10.19.11.9:3003/api/scheduler/technician
{
    "rut":"rut"
}

http://IP:PORT/api/scheduler/client
{
    "rut":"123422125"
}

http://IP:PORT/api/scheduler/residence
{
    "rut":"987654321"
}