# Parte 6: Propuesta unicah_prestamo_equipo

## 1. Problema y usuarios
Hoy el préstamo de proyectores, laptops y cámaras se registra en hojas de cálculo o cuadernos.
Eso genera equipos "perdidos", préstamos duplicados y nadie sabe quién tiene qué ni quién se atrasó.
Lo usarían el personal de laboratorio/audiovisual (registra entregas y devoluciones) y la
coordinación académica (consulta atrasos e historial). Estudiantes y docentes son los solicitantes.

## 2. Por qué en Odoo
- Los solicitantes ya son contactos (res.partner), y se reutiliza el tipo de cliente de la tienda.
- Chatter y trazabilidad integrados: queda registro de cada cambio de estado.
- Permisos por grupo, búsquedas, filtros y agrupaciones sin programarlos.
- Se integra con otros módulos del ERP (Inventario, Activos, Contabilidad) en el futuro.
- Reemplaza múltiples hojas desconectadas por una única fuente de datos.

## 3. Diseño
**Modelos**
- `unicah.equipo`: name, codigo (único), categoria, active, prestamo_ids (One2many), disponible (calculado).
- `unicah.prestamo`: name (secuencia PRE/0001), equipo_id (Many2one), partner_id (Many2one),
  fecha_prestamo, fecha_prevista, fecha_devolucion, dias_prestamo (calculado, almacenado),
  dias_retraso (calculado), state (borrador/prestado/devuelto), notas.

**Herencia:** `res.partner` recibe el campo prestamo_count y un botón inteligente en su formulario
que abre los préstamos del contacto.

**Reglas de negocio**
- La devolución prevista no puede ser anterior al préstamo ni exceder 7 días.
- Un equipo no se puede entregar si ya está prestado.
- Un solicitante no puede tener más de 3 préstamos activos.
- Al devolver con retraso se deja un mensaje en el chatter.

## 4. Capturas
(Pegar capturas: lista de préstamos, formulario, botón en el contacto, error de validación.)

## 5. Segunda versión
- Reservas anticipadas con calendario.
- Notificaciones por correo de devoluciones próximas y atrasadas.
- Multas o bloqueo de solicitantes morosos.
- Integración con inventario/activos fijos y código QR por equipo.
- Reporte PDF del comprobante de préstamo y tablero de uso por categoría.
