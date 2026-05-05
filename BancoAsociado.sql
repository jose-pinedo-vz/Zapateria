Create database BancoGuachinango;

use BancoGuachinango;

create table Sucursal
(Nombre_Sucursal varchar(20)primary key,
Ciudad_Sucursal varchar(15));

create table Cuenta
(ClaveCuenta varchar(5)primary key,
Saldo money,
Sucursal varchar(20),
PIN varchar(4) NOT NULL,
foreign key(Sucursal) references Sucursal(Nombre_Sucursal),
foreign key(ClaveCuenta) references Cliente(ClaveCuenta));

create table Cliente
(ClaveCuenta varchar(5)primary key,
NombreCliente varchar(10),
ApellidoM varchar(15),
ApeelidoP varchar(15));


DELETE FROM Cuenta;
ALTER TABLE Cuenta ADD PIN varchar(4) NOT NULL;

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

CREATE TABLE Tarjeta (
    id_tarjeta INT PRIMARY KEY IDENTITY(1,1),
    numero_tarjeta CHAR(16) UNIQUE NOT NULL,
    cvv CHAR(3) NOT NULL,
    id_cuenta_asociada varchar(5) NOT NULL,
    FOREIGN KEY (id_cuenta_asociada) REFERENCES Cuenta(ClaveCuenta)
);
