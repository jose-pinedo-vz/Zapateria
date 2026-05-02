Create database BancoGuachinango;

ALTER AUTHORIZATION ON DATABASE::BancoGuachinango TO sa;
GO

use BancoGuachinango;

create table Sucursal
(Nombre_Sucursal varchar(20)primary key,
Ciudad_Sucursal varchar(15));

create table Cuenta
(ClaveCuenta varchar(5)primary key,
Saldo money,
Sucursal varchar(20),
foreign key(Sucursal) references Sucursal(Nombre_Sucursal),
foreign key(ClaveCuenta) references Cliente(ClaveCuenta));

CREATE TABLE Clientes (
    clave CHAR(5) PRIMARY KEY,
    Nombre VARCHAR(50),        
    ApellidoP VARCHAR(50),     
    Email VARCHAR(100),       
    Direccion VARCHAR(200),    
    telefono BIGINT            
);
GO



create table Transaccion
(ClaveDeposito varchar(10)primary key,
ClaveDeposita varchar(5),
ClaveRecive varchar(5),
foreign key(ClaveDeposita) references Cliente(ClaveCuenta),
foreign key(ClaveRecive) references Cliente(ClaveCuenta));

create table Deposito
(ClaveDeposito varchar(10)primary key,
Fecha datetime,
Monto money,
foreign key(ClaveDeposito) references Transaccion(ClaveDeposito));

create table Ubicacion
(Nombre varchar(10)primary key,
Ciudad varchar(15),
Clave varchar(5),
foreign key(Clave) references Cliente(ClaveCuenta));

INSERT INTO Sucursal VALUES('Zacatecas Sur', 'Tlaltenango');


INSERT INTO Cliente VALUES('tl-01','Jose','Pinedo','Valdez');
INSERT INTO Ubicacion VALUES('Jose','Tlaltenango','tl-01');
INSERT INTO Cuenta VALUES('tl-01', 10000,'Zacatecas Sur');

INSERT INTO Cliente VALUES('tl-02','Diego','Observacerros','Canaya');
INSERT INTO Ubicacion VALUES('Diego','Colotlan','tl-02');
INSERT INTO Cuenta VALUES('tl-02', 500,'Zacatecas Sur');



INSERT INTO Transaccion VALUES('tl-jpv-000','tl-01','tl-02');
INSERT INTO Deposito VALUES('tl-jpv-000','tl-01',500);



CREATE TABLE Productos (
    Clave CHAR(5) PRIMARY KEY, 
    Modelo VARCHAR(100),
    Marca VARCHAR(100),  
    Seccion VARCHAR(100), 
    Categoria VARCHAR(100)
);


create table Inventario
(Clave char(5), 
CantidadProducto int, 
Talla int, 
FechaIngreso datetime, 
Precio DECIMAL(10,2), 
Color char(100), 
RutaImagen CHAR(300), 

PRIMARY key(Clave, talla, color), 
foreign key (Clave) references Productos(Clave))