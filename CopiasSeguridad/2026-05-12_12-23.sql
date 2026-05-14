CREATE DATABASE Zapateria; 

USE Zapateria; 





-- 1. TABLAS INDEPENDIENTES (Catálogos)
CREATE TABLE Usuario (
    Nombre VARCHAR(15),
    ApellidoP VARCHAR(15), 
    ApellidoM VARCHAR(15),
    PRIMARY KEY (Nombre, ApellidoP)
);

CREATE TABLE Horarios (
    id_horario INT PRIMARY KEY, 
    horario VARCHAR(20)
);

CREATE TABLE color (
    id_color INT PRIMARY KEY, 
    color CHAR(10)
);

CREATE TABLE Talla (
    id_talla INT PRIMARY KEY, 
    talla CHAR(2)
);

CREATE TABLE seccion (
    id_seccion INT PRIMARY KEY, 
    seccion CHAR(10)
);

CREATE TABLE categoria (
    id_categoria INT PRIMARY KEY, 
    categoria CHAR(10)
);

CREATE TABLE marca (
    id_marca INT PRIMARY KEY, 
    marca CHAR(15)
);

CREATE TABLE Ciudades (
    id_ciudad INT PRIMARY KEY IDENTITY(1,1),
    nombre_ciudad VARCHAR(50) NOT NULL
);

-- 2. TABLAS DE CONTACTO Y DIRECCIÓN
CREATE TABLE Telefonos (
    id_telefono INT PRIMARY KEY IDENTITY(1,1), 
    id_duenio CHAR(15) NOT NULL,  
    tipo_entidad VARCHAR(15) NOT NULL, -- Cliente, Proveedor o Empleado 
    numero_telefono VARCHAR(20) NOT NULL
);

CREATE TABLE CodigosPostales (
    cp CHAR(5) PRIMARY KEY,  
    id_ciudad INT, 
    FOREIGN KEY (id_ciudad) REFERENCES Ciudades(id_ciudad)
);

CREATE TABLE Direccion (
    idDireccion INT PRIMARY KEY IDENTITY(1,1), 
    calle VARCHAR(50), 
    numero_externo VARCHAR(10),
    cp CHAR(5), 
    FOREIGN KEY (cp) REFERENCES CodigosPostales(cp)
);

-- 3. TABLAS DE PRODUCTOS Y PERSONAL
CREATE TABLE modelo (
    clave INT PRIMARY KEY, 
    id_marca INT, 
    modelo CHAR(20), 
    FOREIGN KEY (id_marca) REFERENCES marca(id_marca)
);

CREATE TABLE Personal (
    ClaveAcceso VARCHAR(5) PRIMARY KEY,
    Direccion INT, 
    NoEmergencia INT, 
    Sueldo MONEY, 
    horario INT,
    Nombre VARCHAR(15), 
    ApellidoP VARCHAR(15),
    FOREIGN KEY (Nombre, ApellidoP) REFERENCES Usuario(Nombre, ApellidoP),
    FOREIGN KEY (horario) REFERENCES Horarios(id_horario), 
    FOREIGN KEY (Direccion) REFERENCES Direccion(idDireccion), 
    FOREIGN KEY (NoEmergencia) REFERENCES Telefonos(id_telefono)
);


CREATE TABLE Productos (--esta es la buena
    Clave CHAR(5) PRIMARY KEY, 
    Modelo VARCHAR(100),
    Marca VARCHAR(100),   
    Seccion VARCHAR(100), 
    Categoria VARCHAR(100)
);


CREATE TABLE Inventario (--esta es la buena
    Clave CHAR(5), 
    CantidadProducto INT, 
    Talla INT, 
    FechaIngreso DATETIME, 
    Precio DECIMAL(10,2), 
    Color VARCHAR(100), 
    RutaImagen CHAR(300), 
    PRIMARY KEY (Clave, Talla, Color), 
    FOREIGN KEY (Clave) REFERENCES Productos(Clave)
);

-- 4. TABLAS DE OPERACIONES (Ventas, Clientes, Proveedores)
CREATE TABLE Clientes (
    clave CHAR(5) PRIMARY KEY,
    Nombre VARCHAR(50),        
    ApellidoP VARCHAR(50),     
    Email VARCHAR(100),       
    Direccion VARCHAR(200),    
    telefono BIGINT            
);

CREATE TABLE Apartado (
    ClaveDeApartado CHAR(5), 
    Responsable VARCHAR(5), 
    FechaInicial CHAR(15), 
    FechaLimite CHAR(15), 
    CostoTotal MONEY, 
    Importe MONEY, 
    Beneficiario CHAR(5), 
    PRIMARY KEY (Responsable, Beneficiario, ClaveDeApartado), 
    FOREIGN KEY (Responsable) REFERENCES Personal(ClaveAcceso), 
    FOREIGN KEY (Beneficiario) REFERENCES Clientes(clave)
);

CREATE TABLE Proveedores (
    NoCuenta CHAR(15) PRIMARY KEY, 
    Empresa CHAR(20), 
    Direccion INT, 
    correoElectronico CHAR(30), 
    telefono INT, 
    FOREIGN KEY (Direccion) REFERENCES Direccion(idDireccion), 
    FOREIGN KEY (telefono) REFERENCES Telefonos(id_telefono)
);

CREATE TABLE Venta (
    NoVenta INT IDENTITY(1,1), 
    Responsable VARCHAR(5), 
    ClaveProducto CHAR(5), 
    Fecha DATETIME, 
    PRIMARY KEY (NoVenta, ClaveProducto, Responsable),
    FOREIGN KEY (Responsable) REFERENCES Personal(ClaveAcceso), 
    FOREIGN KEY (ClaveProducto) REFERENCES Productos(Clave) 
);

-- 1. LIMPIEZA RÁPIDA
DELETE FROM Venta; DELETE FROM Inventario; DELETE FROM Productos;
DELETE FROM modelo; DELETE FROM Personal; DELETE FROM Telefonos;
DELETE FROM Direccion; DELETE FROM CodigosPostales; DELETE FROM Ciudades;
DELETE FROM Usuario; DELETE FROM Horarios; DELETE FROM color;
DELETE FROM Talla; DELETE FROM seccion; DELETE FROM categoria;
DELETE FROM marca;
GO

SELECT * FROM Personal;
SELECT * FROM Clientes;
SELECT * FROM Venta;
SELECT * FROM Inventario;
SELECT * FROM Productos;

SELECT Productos.Clave, Modelo, Marca, Seccion, Categoria, Talla, Precio, Color, RutaImagen
FROM Productos,Inventario
WHERE Productos.Clave = Inventario.Clave

-- 1. Insertar en Usuario (Nombre y Apellidos)
INSERT INTO Usuario (Nombre, ApellidoP, ApellidoM) 
VALUES ('Juan', 'Perez', 'Garcia');

-- 2. Insertar un Horario (si no tienes uno)
INSERT INTO Horarios (id_horario, horario) 
VALUES (1, '9:00 - 18:00');

-- 3. Insertar Ciudad y Código Postal para su dirección
INSERT INTO Ciudades (nombre_ciudad) VALUES ('CDMX');
-- Nota: id_ciudad será 1 por ser IDENTITY

INSERT INTO CodigosPostales (cp, id_ciudad) 
VALUES ('06000', 1);

-- 4. Insertar su Dirección
INSERT INTO Direccion (calle, numero_externo, cp) 
VALUES ('Av. Reforma', '123', '06000');
-- Nota: idDireccion será 1 por ser IDENTITY

-- 5. Insertar un Teléfono de emergencia
INSERT INTO Telefonos (id_duenio, tipo_entidad, numero_telefono) 
VALUES ('P001', 'Empleado', '5512345678');
-- Nota: id_telefono será 1 por ser IDENTITY

-- 6. ¡AHORA SÍ! Insertar en la tabla Personal
INSERT INTO Personal (
    ClaveAcceso, 
    Direccion, 
    NoEmergencia, 
    Sueldo, 
    horario, 
    Nombre, 
    ApellidoP
) 
VALUES (
    'E001',  -- Su clave de acceso
    1,       -- El idDireccion que creamos arriba
    1,       -- El id_telefono que creamos arriba
    8500.50, -- Su sueldo
    1,       -- El id_horario que creamos arriba
    'Juan',  -- Debe coincidir exactamente con Usuario
    'Perez'  -- Debe coincidir exactamente con Usuario
);

-- Verificar que se agregó correctamente
SELECT * FROM Personal;