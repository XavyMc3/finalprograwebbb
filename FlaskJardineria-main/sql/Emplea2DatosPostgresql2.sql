
INSERT INTO departamento (nombre, ubicacion) VALUES ('Recursos Humanos', 'Madrid'), ('IT', 'Barcelona'), ('Marketing', 'Valencia');
INSERT INTO proyecto (nombre, fecha_inicio, fecha_fin) VALUES ('Proyecto A', '2024-01-01', '2024-06-30'), ('Proyecto B', '2024-02-15', '2024-08-31'), ('Proyecto C', '2024-03-01', '2024-09-30');
INSERT INTO empleado (nombre, apellido, fechaNacimiento, cargo, salario, iddepartamento, idproyecto) VALUES 
('Juan', 'Pérez', '1985-07-23', 'Gerente', 50000, 1, 1), 
('Ana', 'López', '1990-12-10', 'Desarrollador', 40000, 2, 2),
('Pedro', 'Gómez', '1988-03-15', 'Analista', 45000, 3, 3);
