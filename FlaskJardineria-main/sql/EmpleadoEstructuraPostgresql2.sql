-- PostgreSQL SQL script for initializing the database
CREATE TABLE departamento (
    iddepartamento SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    ubicacion VARCHAR(255)
);

CREATE TABLE proyecto (
    idproyecto SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE
);

CREATE TABLE empleado (
    idempleado SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    fechaNacimiento DATE,
    cargo VARCHAR(255),
    salario INTEGER,
    iddepartamento INTEGER REFERENCES departamento(iddepartamento),
    idproyecto INTEGER REFERENCES proyecto(idproyecto)
);