CREATE DATABASE Zapateria; 


USE Zapateria; 


--Ejecutar en este orden las tablas para crear la base de datos sin erroes


create table Usuario
(Nombre varchar(15),
ApellidoP varchar(15), 
ApellidoM varchar(15),
primary key(Nombre,ApellidoP))


CREATE TABLE Horarios
(id_horario int primary KEY, 
horario CHAR(10)) 


create table color
(id_color int PRIMARY KEY, 
color char(10)) 


CREATE TABLE Talla
(id_talla int PRIMARY KEY, 
talla CHAR(2)) 


create table seccion
(id_seccion INT PRIMARY KEY, 
seccion char(10))  

 
create table categoria
(id_categoria INT PRIMARY KEY, 
categoria CHAR(10)) 
 

CREATE TABLE marca
(id_marca INT PRIMARY KEY, 
marca char(15)) 


CREATE TABLE Ciudades
(id_ciudad INT PRIMARY KEY IDENTITY(1,1),
nombre_ciudad VARCHAR(50) NOT NULL ) 

-- esta tabla se va a alimentra desde python o manualmente  

-- se extraera el id de el usuario medinte python y se insertara aqui 

CREATE TABLE Telefonos
( id_telefono INT PRIMARY KEY IDENTITY(1,1), 
id_duenio CHAR(15) NOT NULL,  
tipo_entidad VARCHAR(15) NOT NULL, -- si es de cliente o de proveedor o de empleado 
numero_telefono VARCHAR(20) NOT NULL )


CREATE TABLE modelo
(clave INT PRIMARY KEY, 
id_marca INT, 
modelo CHAR(20), 
FOREIGN KEY (id_marca) REFERENCES marca(id_marca))


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

 
 create table Productos
(Clave char(5) primary key, 
Modelo int, 
Seccion int, 
Categoria int,

foreign KEY (Seccion) references seccion(id_seccion),
foreign key (categoria) REFERENCES categoria(id_categoria), 
FOREIGN KEY (Modelo) REFERENCES modelo(clave)) 


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

 
create table Proveedores
(NoCuenta char(15)primary key, 
Empresa char(20), 
Direccion int, 
correroElectronico CHAR(30), 
telefono INT, 

foreign KEY (Direccion) REFERENCES Direccion(idDireccion), 
foreign KEY (telefono) REFERENCES Telefonos(id_telefono)) 

 
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

 

-- Secciones y Categorías
INSERT INTO seccion (id_seccion, seccion) VALUES (1, 'Caballero'), (2, 'Dama'), (3, 'Niños');
INSERT INTO categoria (id_categoria, categoria) VALUES (1, 'Deportivo'), (2, 'Formal'), (3, 'Bota');

-- Colores y Tallas
INSERT INTO color (id_color, color) VALUES (1, 'Negro'), (2, 'Blanco'), (3, 'Café');
INSERT INTO Talla (id_talla, talla) VALUES (1, '25'), (2, '27'), (3, '28'), (4, '24');

-- Marcas y Modelos
INSERT INTO marca (id_marca, marca) VALUES (1, 'Nike'), (2, 'Adidas'), (3, 'Flexi');

INSERT INTO modelo (clave, id_marca, modelo) VALUES 
(101, 1, 'Air Max'), 
(102, 2, 'Ultraboost'), 
(103, 3, 'Oxford Classic');

-- Productos
INSERT INTO Productos (Clave, Modelo, Seccion, Categoria) VALUES 
('C1', 101, 1, 1), 
('C2', 102, 1, 1), 
('C3', 103, 1, 2);

-- Inventario (Stock y Precios)
INSERT INTO Inventario (Clave, CantidadProducto, Talla, FechaIngreso, Precio, Color, RutaImagen) VALUES 
('C1', 10, 2, GETDATE(), 2500.00, 1, 'img/nike_negro.png'),
('C2', 15, 3, GETDATE(), 2200.00, 2, 'img/adidas_blanco.png'),
('C3', 8, 1, GETDATE(), 1200.00, 3, 'img/flexi_cafe.png');

-- Usuario
INSERT INTO Usuario (Nombre, ApellidoP, ApellidoM) VALUES ('Bladimr', 'G', 'L');

-- Horario
INSERT INTO Horarios (id_horario, horario) VALUES (1, 'Matutino');

-- Personal (Asegúrate que ClaveAcceso sea de 5 caracteres como tu tabla manda)
INSERT INTO Personal (ClaveAcceso, Direccion, NoEmergencia, Sueldo, horario, Nombre, ApellidoP) 
VALUES ('EMP01', NULL, NULL, 5000.00, 1, 'Bladimr', 'G');

-- Venta de un zapato
INSERT INTO Venta (Responsable, ClaveProducto, Fecha) 
VALUES ('EMP01', 'C1', GETDATE());


-- --- CATÁLOGOS BASE ---
SELECT * FROM seccion;
SELECT * FROM categoria;
SELECT * FROM color;
SELECT * FROM Talla;
SELECT * FROM marca;
SELECT * FROM modelo;

-- --- PRODUCTOS E INVENTARIO ---
SELECT * FROM Productos;
SELECT * FROM Inventario

-- --- PERSONAL Y VENTAS ---
SELECT * FROM Usuario;
SELECT * FROM Horarios;
SELECT * FROM Personal;
SELECT * FROM Venta;