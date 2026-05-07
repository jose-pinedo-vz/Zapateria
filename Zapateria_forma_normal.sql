CREATE DATABASE Zapateria; 

ALTER AUTHORIZATION ON DATABASE::Zapateria TO [DESKTOP-EVUPC6S\BloodSG];
GO

ALTER AUTHORIZATION ON DATABASE::Zapateria TO sa;
GO

USE Zapateria; 

create table Usuario
(Nombre varchar(15),
ApellidoP varchar(15), 
ApellidoM varchar(15),
primary key(Nombre,ApellidoP))


create table Personal
(ClaveAcceso varchar(5)primary key,
Direccion int, 
NoEmergencia int, 
Sueldo money, 
horario int,
Nombre varchar(15), 
ApellidoP varchar(15),

foreign key (Nombre,ApellidoP) references Usuario(Nombre,ApellidoP),
foreign key (horario) references Horarios(id_horario), 
foreign KEY (Direccion) REFERENCES Direccion(idDireccion), 
foreign KEY (NoEmergencia) REFERENCES Telefonos(id_telefono)) 

 

CREATE TABLE Horarios
(id_horario int primary KEY, 
horario CHAR(10)) 

 drop table Inventario

create table Inventario(
    Clave char(5), 
    CantidadProducto int, 
    Talla int, 
    FechaIngreso datetime, 
    Precio DECIMAL(10,2), 
    Color char(100), 
    RutaImagen CHAR(300), 

    PRIMARY key(Clave, talla, color), 
    foreign key (Clave) references Productos(Clave)
)
 
create table color
(id_color int PRIMARY KEY, 
color char(10)) 


CREATE TABLE Talla
(id_talla int PRIMARY KEY, 
talla CHAR(2)) 


CREATE TABLE Productos (
    Clave CHAR(5) PRIMARY KEY, 
    Modelo VARCHAR(100),
    Marca VARCHAR(100),   
    Seccion VARCHAR(100), 
    Categoria VARCHAR(100)
);
 
create table seccion
(id_seccion INT PRIMARY KEY, 
seccion char(10))  

 
create table categoria
(id_categoria INT PRIMARY KEY, 
categoria CHAR(10)) 


CREATE TABLE modelo
(clave INT PRIMARY KEY, 
id_marca INT, 
modelo CHAR(20), 

FOREIGN KEY (id_marca) REFERENCES marca(id_marca)) 


CREATE TABLE marca
(id_marca INT PRIMARY KEY, 
marca char(15)) 
 

CREATE TABLE Clientes (
    clave CHAR(5) PRIMARY KEY,
    Nombre VARCHAR(50),        
    ApellidoP VARCHAR(50),     
    Email VARCHAR(100),       
    Direccion VARCHAR(200),    
    telefono BIGINT            
);
GO
 

create table Apartado
( -- apartas un producto 
ClaveDeApartado CHAR(5), 
Responsable varchar(5), 
FechaInicial char(15), 
FechaLimite char(15), 
CostoTotal money, 
Importe money, 
Beneficiario char(5), 

primary key(Responsable, Beneficiario, ClaveDeApartado), 
foreign key (Responsable) references Personal(ClaveAcceso), 
foreign key (Beneficiario) references Clientes(clave)) 

 

 

-- esta tabla se va a alimentra desde python o manualmente  

-- se extraera el id de el usuario medinte python y se insertara aqui 

CREATE TABLE Telefonos
( id_telefono INT PRIMARY KEY IDENTITY(1,1), 
id_duenio CHAR(15) NOT NULL,  
tipo_entidad VARCHAR(15) NOT NULL, -- si es de cliente o de proveedor o de empleado 
numero_telefono VARCHAR(20) NOT NULL ) 

 
create table Proveedores
(NoCuenta char(15)primary key, 
Empresa char(20), 
Direccion int, 
correroElectronico CHAR(30), 
telefono INT, 

foreign KEY (Direccion) REFERENCES Direccion(idDireccion), 
foreign KEY (telefono) REFERENCES Telefonos(id_telefono)) 

 

CREATE TABLE Ciudades
(id_ciudad INT PRIMARY KEY IDENTITY(1,1),
nombre_ciudad VARCHAR(50) NOT NULL ) 

 
CREATE TABLE CodigosPostales
(cp CHAR(5) PRIMARY KEY,  
id_ciudad INT, 

FOREIGN KEY (id_ciudad) REFERENCES Ciudades(id_ciudad))

 
CREATE TABLE Direccion
(idDireccion INT PRIMARY KEY IDENTITY(1,1), 
calle VARCHAR(50), 
numero_externo VARCHAR(10),
cp CHAR(5), 

FOREIGN KEY (cp) REFERENCES CodigosPostales(cp)) 

 
create table Surtir
(Cantidad int, 
CostoTotal DECIMAL(10,2), 
Fecha datetime, 
ClaveProducto char(5), 
ClaveEmpleado varchar(5), 
ClaveProveedor char(15), 

primary key(ClaveEmpleado, ClaveProducto, ClaveProveedor, Fecha), 
foreign key(ClaveProducto) references Inventario(Clave), 
foreign key(ClaveProveedor) references Proveedores(NoCuenta), 
foreign key(ClaveEmpleado) references Personal(ClaveAcceso)) 

 

create table Venta
(NoVenta int identity(1,1), 
Responsable varchar(5), 
ClaveProducto char(5), 
Fecha datetime, 

primary key(NoVenta,ClaveProducto,Responsable),
foreign key(Responsable) references Personal(ClaveAcceso), 
foreign key(ClaveProducto)references Inventario(Clave)) 

 