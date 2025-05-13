const especialidadSelect = document.getElementById('especialidad');
  const doctorSelect = document.getElementById('doctor');
  const bloqueInput = document.getElementById('bloque');
  const calendarContainer = document.getElementById('calendario-container');
  const horarioSelect = document.getElementById('horario');

  let fechasDisponiblesGlobal = []; 
  let mesActual = new Date(); 
  
  const crearCalendario = async (fechasDisponibles = [], fecha = new Date()) => {
    // Guardar fechas disponibles para navegación entre meses
    fechasDisponiblesGlobal = fechasDisponibles;
    
    // Crear mapa de fechas para acceso rápido
    const fechasMap = new Map(
      fechasDisponibles.map(f => [f.fecha, f])
    );

    calendarContainer.innerHTML = '';
    
    // Crear contenedor principal del calendario
    const contenedorMes = document.createElement('div');
    contenedorMes.className = 'calendar-container';
    
    // Crear barra de navegación del mes
    const navegacion = document.createElement('div');
    navegacion.className = 'month-navigation';
    
    const botonAnterior = document.createElement('button');
    botonAnterior.className = 'nav-button';
    botonAnterior.textContent = '← Anterior';
    botonAnterior.type = 'button';
    
    const tituloMes = document.createElement('div');
    tituloMes.className = 'month-title';
    
    const botonSiguiente = document.createElement('button');
    botonSiguiente.className = 'nav-button';
    botonSiguiente.textContent = 'Siguiente →';
    botonSiguiente.type = 'button';
    
    // Configurar título y límites de navegación
    tituloMes.textContent = fecha.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
    
    const hoy = new Date();
    const ultimoDia = new Date(hoy);
    ultimoDia.setDate(hoy.getDate() + 56); // Límite de 8 semanas
    
    const primerDiaMes = new Date(fecha.getFullYear(), fecha.getMonth(), 1);
    const ultimoDiaMes = new Date(fecha.getFullYear(), fecha.getMonth() + 1, 0);
    
    // Deshabilitar botones según límites
    botonAnterior.disabled = primerDiaMes < hoy;
    botonSiguiente.disabled = ultimoDiaMes > ultimoDia;
    
    // Configurar navegación entre meses
    botonAnterior.addEventListener('click', () => {
      mesActual.setMonth(mesActual.getMonth() - 1);
      crearCalendario(fechasDisponiblesGlobal, new Date(mesActual));
    });
    
    botonSiguiente.addEventListener('click', () => {
      mesActual.setMonth(mesActual.getMonth() + 1);
      crearCalendario(fechasDisponiblesGlobal, new Date(mesActual));
    });
    
    // Ensamblar la navegación
    navegacion.appendChild(botonAnterior);
    navegacion.appendChild(tituloMes);
    navegacion.appendChild(botonSiguiente);
    contenedorMes.appendChild(navegacion);
    
    // Crear grid del calendario
    const calendario = document.createElement('div');
    calendario.className = 'calendar';
    
    // Agregar encabezados de días
    const diasSemana = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    diasSemana.forEach(dia => {
      const header = document.createElement('div');
      header.className = 'calendar-header';
      header.textContent = dia;
      calendario.appendChild(header);
    });
    
    // Calcular días del mes
    const inicioMes = new Date(fecha.getFullYear(), fecha.getMonth(), 1);
    const finMes = new Date(fecha.getFullYear(), fecha.getMonth() + 1, 0);
    
    // Agregar celdas vacías hasta el primer día del mes
    for (let i = 0; i < inicioMes.getDay(); i++) {
      const dia = document.createElement('div');
      dia.className = 'calendar-day disabled';
      calendario.appendChild(dia);
    }
    
    // Agregar los días del mes
    for (let i = 1; i <= finMes.getDate(); i++) {
      const fecha = new Date(inicioMes.getFullYear(), inicioMes.getMonth(), i);
      const fechaStr = fecha.toISOString().split('T')[0];
      
      const dia = document.createElement('div');
      dia.className = 'calendar-day';
      dia.textContent = i;
      
      // Determinar si es fin de semana
      const esFinde = fecha.getDay() === 0 || fecha.getDay() === 6;
      
      // Aplicar estilos según disponibilidad
      if (fecha < hoy || fecha > ultimoDia || esFinde) {
        dia.classList.add('disabled');
        if (esFinde) dia.classList.add('weekend');
      } else if (fechasMap.has(fechaStr)) {
        dia.classList.add('available');
        dia.dataset.fecha = fechaStr;
        dia.addEventListener('click', () => mostrarBloques(fechasMap.get(fechaStr)));
      } else {
        dia.classList.add('disabled');
      }
      
      calendario.appendChild(dia);
    }
    
    contenedorMes.appendChild(calendario);
    calendarContainer.appendChild(contenedorMes);
  };

  const listarDoctores = async (especialidadId) => {
    try {
      // Deshabilitar controles y limpiar selecciones previas
      doctorSelect.disabled = true;
      calendarContainer.innerHTML = '';
      horarioSelect.disabled = true;
      horarioSelect.innerHTML = '<option value="">Seleccione un horario</option>';
      
      const response = await fetch(`get_doctores/${especialidadId}/`);
      const data = await response.json();
      
      let options = '<option value="">Seleccione un doctor</option>';
      data.forEach(doctor => {
        options += `<option value="${doctor.id}">${doctor.nombre}</option>`;
      });
      doctorSelect.innerHTML = options;
      doctorSelect.disabled = false;
    } catch (error) {
      console.error('Error al cargar doctores:', error);
    }
  };

  const formatearFecha = (fecha) => {
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const listarEspecialidades = async () => {
    try {
      const response = await fetch('get_especialidades/');
      const data = await response.json();
      
      let options = '<option value="">Seleccione una especialidad</option>';
      data.forEach(especialidad => {
        options += `<option value="${especialidad.id}">${especialidad.nombre}</option>`;
      });
      especialidadSelect.innerHTML = options;
    } catch (error) {
      console.error('Error al cargar especialidades:', error);
    }
  };

  const mostrarBloques = (fecha) => {
    document.querySelectorAll('.calendar-day').forEach(dia => {
      dia.classList.remove('selected');
    });
    
    const diaSeleccionado = document.querySelector(`[data-fecha="${fecha.fecha}"]`);
    if (diaSeleccionado) {
      diaSeleccionado.classList.add('selected');
    }
    
    const fechaObj = new Date(fecha.fecha);
    horarioSelect.innerHTML = '<option value="">Seleccione un horario</option>' +
      fecha.bloques.map(bloque => `
        <option value="${bloque.id}">${bloque.hora_inicio} - ${bloque.hora_fin}</option>
      `).join('');
    
    horarioSelect.disabled = false;
  };

  const listarFechas = async (doctorId) => {
    try {
      calendarContainer.innerHTML = '';
      horarioSelect.disabled = true;
      horarioSelect.innerHTML = '<option value="">Seleccione un horario</option>';
      bloqueInput.value = '';
      
      const response = await fetch(`get_fechas/${doctorId}/`);
      const fechasDisponibles = await response.json();
      
      if (fechasDisponibles.length === 0) {
        calendarContainer.innerHTML = '<p>No hay fechas disponibles para este doctor.</p>';
        return;
      }

      mesActual = new Date();
      crearCalendario(fechasDisponibles);
    } catch (error) {
      console.error('Error al cargar fechas:', error);
      calendarContainer.innerHTML = '<p>Error al cargar el calendario. Por favor, intente nuevamente.</p>';
    }
  };

  horarioSelect.addEventListener('change', (e) => {
    bloqueInput.value = e.target.value || '';
  });

  especialidadSelect.addEventListener('change', (e) => {
    if (e.target.value) {
      listarDoctores(e.target.value);
    } else {
      doctorSelect.innerHTML = '<option value="">Seleccione un doctor</option>';
      doctorSelect.disabled = true;
      calendarContainer.innerHTML = '';
      horarioSelect.disabled = true;
      horarioSelect.innerHTML = '<option value="">Seleccione un horario</option>';
      bloqueInput.value = '';
    }
  });

  doctorSelect.addEventListener('change', (e) => {
    if (e.target.value) {
      listarFechas(e.target.value);
    } else {
      calendarContainer.innerHTML = '';
      horarioSelect.disabled = true;
      horarioSelect.innerHTML = '<option value="">Seleccione un horario</option>';
      bloqueInput.value = '';
    }
  });

  window.addEventListener('load', listarEspecialidades);