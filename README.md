# MyJ-API
### Peticiones POST (JSON) Todas las peticiones requieren un bearer token (access_token) otorgado al hacer login

http://IP:PORT/api/auth/sign-up
```javascript
{
    "email":"test@test.test",
    "password":"test",
    "fullName":"testing"
}
```

http://IP:PORT/api/auth/login
```javascript
{
    "email": "test@test.test",
    "password": "test"
}
```

http://IP:PORT/api/scheduler/technician
```javascript
{
    "comuna":"Comuna",
    "rut":"123456789",
    "nombre":"nombre",
    "capacidad":"7",
    "estado":"No disponible"
}
```

http://IP:PORT/api/scheduler/client
```javascript
{
    "rut":"987654321",
    "email":"asdas@asda.com",
    "nombre":"testing",
    "contacto1":"1231233",
    "contacto2":"1231232",
    "created_by": "test@test.test", //Correo del usuario actual
    "updated_by": "test@test.test"  //Correo del usuario actual
}
```

http://IP:PORT/api/scheduler/residence
```javascript
{
    "comuna":"Comuna",
    "direccion":"direccion",
    "mac":"mac",
    "pppoe":"pppoe"
}
```

http://IP:PORT/api/scheduler/order
```javascript
{
    "idtipo":"1",                    //ID tipo de instalacion
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
    "domicilio": "1"              //ID Domicilio del cliente
}
```

http://IP:PORT/api/scheduler/typeorder
```javascript
{ 
    "descripcion":"instalacion" 
}
```

### Peticiones GET Todas las peticiones requieren un bearer token (access_token) otorgado al hacer login

http://IP:PORT/api/scheduler/typeorder
```javascript
    SIN PARAMETROS
```


http://IP:PORT/api/scheduler/technician
```javascript
{
    SIN PARAMETROS
}
```

http://IP:PORT/api/scheduler/client
```javascript
{
    "rut":"123422125"
}
```

http://IP:PORT/api/scheduler/residence
```javascript
{
    "rut":"987654321"
}
```

http://IP:PORT/api/scheduler/order
```javascript
{
    "date_init":"2020-05-10"
    "date_end":"2020-05-12"
}
```

http://IP:PORT/api/scheduler/cl-orders
```javascript
{
    "rut_cliente":"18839285-7", #id_orden #nombre_encargado #domicilio
    "date_init":"2018-01-01",
    "date_end":"2021-01-01"
}
```

