Create database BancoGuachinango;

use BancoGuachinango;

create table Sucursal
(Nombre_Sucursal varchar(20)primary key,
Ciudad_Sucursal varchar(15));

create table Cliente
(ClaveCuenta varchar(5) primary key,
NombreCliente varchar(10),
ApellidoM varchar(15),
ApellidoP varchar(15),
Telefono varchar(15),
Email varchar(50),    
Activo bit default 1);

create table Cuenta
(ClaveCuenta varchar(5)primary key,
Saldo money,
Sucursal varchar(20),
PIN varchar(4) not null,
foreign key(Sucursal) references Sucursal(Nombre_Sucursal),
foreign key(ClaveCuenta) references Cliente(ClaveCuenta));

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
(Ciudad varchar(15),
Clave varchar(5) primary key,
foreign key(Clave) references Cliente(ClaveCuenta));

create table Tarjeta 
(id_tarjeta int primary key identity(1,1),
numero_tarjeta char(16) unique not null,
cvv char(3) not null,
id_cuenta_asociada varchar(5) not null,
foreign key (id_cuenta_asociada) references Cuenta(ClaveCuenta));
INSERT INTO Sucursal VALUES('Zacatecas Sur', 'Tlaltenango');


INSERT INTO Cliente VALUES('tl-01','Jose','Pinedo','Valdez');
INSERT INTO Ubicacion VALUES('Jose','Tlaltenango','tl-01');
INSERT INTO Cuenta VALUES('tl-01', 10000,'Zacatecas Sur','1234');

INSERT INTO Cliente VALUES('tl-02','Diego','Observac','Canaya');
INSERT INTO Ubicacion VALUES('Diego','Colotlan','tl-02');
INSERT INTO Cuenta VALUES('tl-02', 500,'Zacatecas Sur','2345');



INSERT INTO Transaccion VALUES('tl-jpv-000','tl-01','tl-02');
INSERT INTO Deposito VALUES('tl-jpv-000',GETDATE(),500);

select * from Sucursal
select * from Cliente
select * from Cuenta
select * from Ubicacion
select * from Transaccion
select * from Deposito
select * from Tarjeta

SELECT distinct Cliente.ClaveCuenta,NombreCliente,ApellidoM,ApeelidoP,Saldo,Sucursal,numero_tarjeta 
FROM Cuenta,Cliente,Tarjeta 
WHERE Cliente.ClaveCuenta=Cuenta.ClaveCuenta and  Cliente.ClaveCuenta=id_cuenta_asociada and Cliente.ClaveCuenta='tl-01'

ALTER TABLE Cliente ADD Activo BIT DEFAULT 1;
GO

UPDATE Cliente SET Activo = 1;
GO

ALTER TABLE Cliente ADD Telefono VARCHAR(15);
ALTER TABLE Cliente ADD Email VARCHAR(50);
GO