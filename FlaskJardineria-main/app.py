from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from Entity import Base, Empleado, Departamento, Proyecto

app = Flask(__name__)

app.secret_key='123456'

# Set up the database connection
engine = create_engine('postgresql://postgres:123456@localhost/emplea2')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

#Ruta Principal
@app.route('/')
def home():
    return render_template('index.html')
# Empleado routes

### Listar empleado
@app.route('/empleado')
def listar_empleado():
    session = DBSession()
    empleados = session.query(Empleado).all()
    departamentos = session.query(Departamento).all()
    proyectos = session.query(Proyecto).all()
    session.close()
    
    return render_template('empleado.html', empleados=empleados, 
                           departamentos=departamentos, proyectos=proyectos)

### Agregar empleado
@app.route('/empleado/agregar', methods=['GET', 'POST'])
def agregar_empleado():
    if request.method == 'POST':
        session = DBSession()
        try:
            # Obtener los valores del formulario
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            fechaNacimiento = request.form['fechaNacimiento']
            cargo = request.form['cargo']
            salario = request.form['salario']
            iddepartamento = request.form['iddepartamento']
            idproyecto = request.form['idproyecto']

            # Validación de datos
            if not nombre or not apellido or not fechaNacimiento or not cargo or not salario or not iddepartamento:
                flash('Todos los campos obligatorios deben ser completados', 'error')
                return redirect(url_for('listar_empleado'))

            # Agregar empleado a la base de datos
            Empleado.agregarEmpleado(session,
                                     nombre=nombre,
                                     apellido=apellido,
                                     fechaNacimiento=fechaNacimiento,
                                     cargo=cargo,
                                     salario=salario,
                                     iddepartamento=iddepartamento,
                                     idproyecto=idproyecto)
            session.close()
            flash('Empleado agregado correctamente', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error: No se puede agregar el empleado. Verifique los datos e intente nuevamente.', 'error')
        except Exception as e:
            session.rollback()
            flash(f'Error inesperado: {e}', 'error')
        finally:
            session.close()
        return redirect(url_for('listar_empleado'))
    else:
        return render_template('agregar_empleado.html')  # Create a template for adding employees

### Eliminar empleado
@app.route('/empleado/eliminar/<int:id_empleado>')
def eliminar_empleado(id_empleado):
    session = DBSession()
    try:
        empleado = session.query(Empleado).filter_by(idempleado=id_empleado).first()
        if empleado:
            session.delete(empleado)
            session.commit()
            flash('Empleado eliminado correctamente', 'success')
        else:
            flash('No se encontró el empleado con el ID proporcionado', 'error')
    except IntegrityError:
        session.rollback()
        flash('Error: No se puede eliminar el empleado porque está vinculado a otros registros.', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error inesperado: {e}', 'error')
    finally:
        session.close()
    return redirect(url_for('listar_empleado'))

### Editar datos de empleado (para AJAX requests)
@app.route('/empleado/editarDatos', methods=['POST'])
def editar_datos_empleado():
    session = DBSession()
    try:
        id_empleado = request.form['id_empleado']
        empleado = session.query(Empleado).filter_by(idempleado=id_empleado).first()
        session.close()
        if empleado:
            return jsonify({
                'id_empleado': empleado.idempleado,
                'nombre': empleado.nombre,
                'apellido': empleado.apellido,
                'fechaNacimiento': empleado.fechaNacimiento.isoformat(),
                'cargo': empleado.cargo,
                'salario': empleado.salario,
                'iddepartamento': empleado.iddepartamento,
                'idproyecto': empleado.idproyecto
            })
        else:
            return jsonify({'error': 'No se encontró el empleado con el ID proporcionado'})
    except Exception as e:
        flash(f'Error inesperado: {e}', 'error')
        return jsonify({'error': 'Error inesperado al obtener los datos del empleado'})

### Editar empleado
@app.route('/empleado/editar/<int:id_empleado>', methods=['GET', 'POST'])
def editar_empleado(id_empleado):
    session = DBSession()
    if request.method == 'POST':
        try:
            empleado = session.query(Empleado).filter_by(idempleado=id_empleado).first()
            if empleado:
                empleado.nombre = request.form['nombre']
                empleado.apellido = request.form['apellido']
                empleado.fechaNacimiento = request.form['fechaNacimiento']
                empleado.cargo = request.form['cargo']
                empleado.salario = request.form['salario']
                empleado.iddepartamento = request.form['iddepartamento']
                empleado.idproyecto = request.form['idproyecto']

                session.commit()
                flash('Empleado actualizado correctamente', 'success')
            else:
                flash('No se encontró el empleado con el ID proporcionado', 'error')
        except IntegrityError:
            session.rollback()
            flash('Error: No se puede actualizar el empleado. Verifique los datos e intente nuevamente.', 'error')
        except Exception as e:
            session.rollback()
            flash(f'Error inesperado: {e}', 'error')
        finally:
            session.close()
        return redirect(url_for('listar_empleado'))
    else:
        empleado = session.query(Empleado).filter_by(idempleado=id_empleado).first()
        session.close()
        if empleado:
            return render_template('editar_empleado.html', empleado=empleado)  # Create a template for editing employees
        else:
            flash('No se encontró el empleado con el ID proporcionado', 'error')
            return redirect(url_for('listar_empleado'))

# Departamento routes

### Listar departamento
@app.route('/departamento')
def listar_departamento():
    session = DBSession()
    departamentos = session.query(Departamento).all()
    session.close()
    return render_template('departamento.html', departamentos=departamentos)

### Agregar departamento
@app.route('/departamento/agregar', methods=['GET', 'POST'])
def agregar_departamento():
    if request.method == 'POST':
        session = DBSession()
        try:
            nombre = request.form['nombre']
            ubicacion = request.form['ubicacion']

            if not nombre or not ubicacion:
                flash('Todos los campos obligatorios deben ser completados', 'error')
                return redirect(url_for('listar_departamento'))

            Departamento.agregarDepartamento(session, nombre=nombre, ubicacion=ubicacion)
            session.close()
            flash('Departamento agregado correctamente', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error: No se puede agregar el departamento. Verifique los datos e intente nuevamente.', 'error')
        except Exception as e:
            session.rollback()
            flash(f'Error inesperado: {e}', 'error')
        finally:
            session.close()
        return redirect(url_for('listar_departamento'))
    else:
        return render_template('agregar_departamento.html')  # Create a template for adding departments

### Eliminar departamento
@app.route('/departamento/eliminar/<int:id_departamento>')
def eliminar_departamento(id_departamento):
    session = DBSession()
    try:
        departamento = session.query(Departamento).filter_by(iddepartamento=id_departamento).first()
        if departamento:
            session.delete(departamento)
            session.commit()
            flash('Departamento eliminado correctamente', 'success')
        else:
            flash('No se encontró el departamento con el ID proporcionado', 'error')
    except IntegrityError:
        session.rollback()
        flash('Error: No se puede eliminar el departamento porque está vinculado a otros registros.', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error inesperado: {e}', 'error')
    finally:
        session.close()
    return redirect(url_for('listar_departamento'))

### Editar departamento
@app.route('/departamento/editar/<int:id_departamento>', methods=['GET', 'POST'])
def editar_departamento(id_departamento):
    session = DBSession()
    if request.method == 'POST':
        try:
            departamento = session.query(Departamento).filter_by(iddepartamento=id_departamento).first()
            if departamento:
                departamento.nombre = request.form['nombre']
                departamento.ubicacion = request.form['ubicacion']
                
                session.commit()
                flash('Departamento actualizado correctamente', 'success')
            else:
                flash('No se encontró el departamento con el ID proporcionado', 'error')
        except IntegrityError:
            session.rollback()
            flash('Error: No se puede actualizar el departamento. Verifique los datos e intente nuevamente.', 'error')
        except Exception as e:
            session.rollback()
            flash(f'Error inesperado: {e}', 'error')
        finally:
            session.close()
        return redirect(url_for('listar_departamento'))
    else:
        departamento = session.query(Departamento).filter_by(iddepartamento=id_departamento).first()
        session.close()
        if departamento:
            return render_template('editar_departamento.html', departamento=departamento)  # Create a template for editing departments
        else:
            flash('No se encontró el departamento con el ID proporcionado', 'error')
            return redirect(url_for('listar_departamento'))

# Proyecto routes

### Listar proyecto
@app.route('/proyecto')
def listar_proyecto():
    session = DBSession()
    proyectos = session.query(Proyecto).all()
    session.close()
    return render_template('proyecto.html', proyectos=proyectos)

### Agregar proyecto
@app.route('/proyecto/agregar', methods=['GET', 'POST'])
def agregar_proyecto():
    if request.method == 'POST':
        session = DBSession()
        try:
            nombre = request.form['nombre']
            fecha_inicio = request.form['fecha_inicio']
            fecha_fin = request.form['fecha_fin']

            if not nombre or not fecha_inicio or not fecha_fin:
                flash('Todos los campos obligatorios deben ser completados', 'error')
                return redirect(url_for('listar_proyecto'))

            Proyecto.agregarProyecto(session, nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            session.close()
            flash('Proyecto agregado correctamente', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error: No se puede agregar el proyecto. Verifique los datos e intente nuevamente.', 'error')
        except Exception as e:
            session.rollback()
            flash(f'Error inesperado: {e}', 'error')
        finally:
            session.close()
        return redirect(url_for('listar_proyecto'))
    else:
        return render_template('agregar_proyecto.html')  # Create a template for adding projects

### Eliminar proyecto
@app.route('/proyecto/eliminar/<int:id_proyecto>')
def eliminar_proyecto(id_proyecto):
    session = DBSession()
    try:
        proyecto = session.query(Proyecto).filter_by(idproyecto=id_proyecto).first()
        if proyecto:
            session.delete(proyecto)
            session.commit()
            flash('Proyecto eliminado correctamente', 'success')
        else:
            flash('No se encontró el proyecto con el ID proporcionado', 'error')
    except IntegrityError:
        session.rollback()
        flash('Error: No se puede eliminar el proyecto porque está vinculado a otros registros.', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error inesperado: {e}', 'error')
    finally:
        session.close()
    return redirect(url_for('listar_proyecto'))

### Editar proyecto
@app.route('/proyecto/editar/<int:id_proyecto>', methods=['GET', 'POST'])
def editar_proyecto(id_proyecto):
    session = DBSession()
    if request.method == 'POST':
        try:
            proyecto = session.query(Proyecto).filter_by(idproyecto=id_proyecto).first()
            if proyecto:
                proyecto.nombre = request.form['nombre']
                proyecto.fecha_inicio = request.form['fecha_inicio']
                proyecto.fecha_fin = request.form['fecha_fin']
                
                session.commit()
                flash('Proyecto actualizado correctamente', 'success')
            else:
                flash('No se encontró el proyecto con el ID proporcionado', 'error')
        except IntegrityError:
            session.rollback()
            flash('Error: No se puede actualizar el proyecto. Verifique los datos e intente nuevamente.', 'error')
        except Exception as e:
            session.rollback()
            flash(f'Error inesperado: {e}', 'error')
        finally:
            session.close()
        return redirect(url_for('listar_proyecto'))
    else:
        proyecto = session.query(Proyecto).filter_by(idproyecto=id_proyecto).first()
        session.close()
        if proyecto:
            return render_template('editar_proyecto.html', proyecto=proyecto)  # Create a template for editing projects
        else:
            flash('No se encontró el proyecto con el ID proporcionado', 'error')
            return redirect(url_for('listar_proyecto'))

if __name__ == '__main__':
    app.run(debug=True)
