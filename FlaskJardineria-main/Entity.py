from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence

from sqlalchemy.orm import relationship, declarative_base

Base= declarative_base()

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'empleado'
    idempleado = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(100), nullable=False)
    fechaNacimiento = Column(Date, nullable=False)
    cargo = Column(String(50), nullable=False)
    salario = Column(Integer, nullable=False)
    iddepartamento = Column(Integer, ForeignKey('departamento.iddepartamento'), nullable=False)
    idproyecto = Column(Integer, ForeignKey('proyecto.idproyecto'), nullable=True)

    departamento = relationship('Departamento', back_populates='empleados')
    proyecto = relationship('Proyecto', back_populates='empleados')

    @staticmethod
    def empleadoInfo(session):
        empleados = session.query(Empleado).all()
        for empleado in empleados:
            print(f"ID de Empleado: {empleado.idempleado}")
            print(f"Nombre: {empleado.nombre}")
            print(f"Apellido: {empleado.apellido}")
            print(f"Fecha de Nacimiento: {empleado.fechaNacimiento}")
            print(f"Cargo: {empleado.cargo}")
            print(f"Salario: {empleado.salario}")
            print(f"ID de Departamento: {empleado.iddepartamento}")
            print(f"ID de Proyecto: {empleado.idproyecto}")
            print("--------------------------")

    @staticmethod
    def agregarEmpleado(session, nombre, apellido, fechaNacimiento, cargo, salario, iddepartamento, idproyecto=None):
        nuevoEmpleado = Empleado(
            nombre=nombre, 
            apellido=apellido, 
            fechaNacimiento=fechaNacimiento, 
            cargo=cargo, 
            salario=salario, 
            iddepartamento=iddepartamento, 
            idproyecto=idproyecto
        )
        session.add(nuevoEmpleado)
        session.commit()
        print("Empleado agregado correctamente")

    @staticmethod
    def modificarEmpleado(session, id_empleado, **kwargs):
        empleado = session.query(Empleado).filter_by(idempleado=id_empleado).first()
        if empleado:
            for key, value in kwargs.items():
                setattr(empleado, key, value)
            session.commit()
            print('Empleado actualizado')
        else:
            print('Empleado no encontrado')

    @staticmethod
    def eliminarEmpleado(session, id_empleado):
        empleado = session.query(Empleado).filter_by(idempleado=id_empleado).first()
        if empleado:
            session.delete(empleado)
            session.commit()
            print('Empleado eliminado')
        else:
            print('No existe el empleado')

class Departamento(Base):
    __tablename__ = 'departamento'
    iddepartamento = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    ubicacion = Column(String(100), nullable=False)

    empleados = relationship('Empleado', back_populates='departamento')

    @staticmethod
    def departamentoInfo(session):
        departamentos = session.query(Departamento).all()
        for departamento in departamentos:
            print(f"ID de Departamento: {departamento.iddepartamento}")
            print(f"Nombre: {departamento.nombre}")
            print(f"Ubicación: {departamento.ubicacion}")
            print("--------------------------")

    @staticmethod
    def agregarDepartamento(session, nombre, ubicacion):
        nuevoDepartamento = Departamento(
            nombre=nombre, 
            ubicacion=ubicacion
        )
        session.add(nuevoDepartamento)
        session.commit()
        print("Departamento agregado correctamente")

    @staticmethod
    def modificarDepartamento(session, id_departamento, **kwargs):
        departamento = session.query(Departamento).filter_by(iddepartamento=id_departamento).first()
        if departamento:
            for key, value in kwargs.items():
                setattr(departamento, key, value)
            session.commit()
            print('Departamento actualizado')
        else:
            print('Departamento no encontrado')

    @staticmethod
    def eliminarDepartamento(session, id_departamento):
        departamento = session.query(Departamento).filter_by(iddepartamento=id_departamento).first()
        if departamento:
            session.delete(departamento)
            session.commit()
            print('Departamento eliminado')
        else:
            print('No existe el departamento')

class Proyecto(Base):
    __tablename__ = 'proyecto'
    idproyecto = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    empleados = relationship('Empleado', back_populates='proyecto')

    @staticmethod
    def proyectoInfo(session):
        proyectos = session.query(Proyecto).all()
        for proyecto in proyectos:
            print(f"ID de Proyecto: {proyecto.idproyecto}")
            print(f"Nombre: {proyecto.nombre}")
            print(f"Fecha de Inicio: {proyecto.fecha_inicio}")
            print(f"Fecha de Fin: {proyecto.fecha_fin}")
            print("--------------------------")

    @staticmethod
    def agregarProyecto(session, nombre, fecha_inicio, fecha_fin):
        nuevoProyecto = Proyecto(
            nombre=nombre, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin
        )
        session.add(nuevoProyecto)
        session.commit()
        print("Proyecto agregado correctamente")

    @staticmethod
    def modificarProyecto(session, id_proyecto, **kwargs):
        proyecto = session.query(Proyecto).filter_by(idproyecto=id_proyecto).first()
        if proyecto:
            for key, value in kwargs.items():
                setattr(proyecto, key, value)
            session.commit()
            print('Proyecto actualizado')
        else:
            print('Proyecto no encontrado')

    @staticmethod
    def eliminarProyecto(session, id_proyecto):
        proyecto = session.query(Proyecto).filter_by(idproyecto=id_proyecto).first()
        if proyecto:
            session.delete(proyecto)
            session.commit()
            print('Proyecto eliminado')
        else:
            print('No existe el proyecto')
