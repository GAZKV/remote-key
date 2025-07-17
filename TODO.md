# ✅ TODO – TeclaRemota

Lista de tareas para el desarrollo incremental del proyecto.

---

## 🧱 Fase 1 – Funcionalidad básica y compatibilidad

- [x] Reemplazar `keyboard` por `pyautogui` o `SendInput` para enviar teclas que funcionen en juegos como Star Citizen.
- [x] Crear una función `send_key_sequence()` que reciba una cadena de texto y ejecute las teclas en el servidor.

---

## 🎨 Fase 2 – Personalización visual de botones

- [x] Agregar soporte para mostrar imágenes como fondo de cada botón (por botón).
- [x] Permitir definir un color de fondo cuando no se use imagen.
- [x] Mostrar nombre personalizado en cada botón de forma configurable.

---

## ⚙️ Fase 3 – Panel de configuración visual

- [x] Agregar botón global de engrane que despliegue un panel de configuración.
- [x] Diseñar un modal o panel lateral con las opciones de configuración de cada botón.
- [x] Agregar input para cambiar el nombre visible del botón.
- [x] Agregar opción para elegir entre imagen o color como fondo.
- [x] Mostrar paleta de color (`<input type="color">`) cuando se elija fondo por color.
- [x] Agregar campo de texto para definir la secuencia de teclas que ejecutará el botón.

---

## 💾 Fase 4 – Persistencia y funcionalidad dinámica

- [x] Guardar configuración de cada botón en `localStorage` o un archivo JSON.
- [x] Aplicar los cambios visuales en tiempo real cuando se edite la configuración.
- [x] Cargar la configuración al inicio de la aplicación para reconstruir los botones.
- [x] Enviar al backend la secuencia de teclas definida por cada botón cuando se presiona.

---

# 🆕 TODO – Fase 5 – Interfaz estilo Stream Deck

Objetivo: Transformar la interfaz en una cuadrícula dinámica, responsiva y visualmente atractiva, inspirada en el diseño del Stream Deck físico.

---

## 🧱 Diseño y distribución

- [ ] Hacer que los botones se acomoden automáticamente en **cuadrícula responsiva** sin importar la cantidad.
- [ ] Mantener **aspecto cuadrado** de todos los botones usando `aspect-ratio: 1 / 1` o trucos con `padding-bottom`.
- [ ] Permitir **agregar nuevos botones** desde la interfaz de configuración.
- [ ] Permitir **eliminar botones** desde la misma interfaz de configuración.
- [ ] Almacenar dinámicamente la cantidad total y sus configuraciones en `localStorage` o archivo JSON.

---

## 🖼 Estilo visual

- [ ] Aplicar **bordes redondeados**, **sombra** y **transición suave** a los botones estilo Stream Deck.
- [ ] Implementar **animación CSS de “activo”** al presionar un botón (ej: parpadeo, glow, rebote).
- [ ] Utilizar `:active` o clases dinámicas con JS para disparar animaciones visuales.

---

## 📱 Adaptación a resolución

- [ ] Asegurar que la cuadrícula **adapte tamaño de los botones** automáticamente según la resolución (uso de `grid`, `flex`, `minmax`, etc.).
- [ ] Limitar o ajustar el número de columnas según el ancho del viewport.

---

## 🧰 Extras

- [ ] Agregar botón "Añadir nuevo botón" que cree un nuevo bloque editable en el panel de configuración.
- [ ] Agregar ícono de papelera o botón “Eliminar” por cada botón en la interfaz de configuración.
- [ ] Agregar confirmación antes de eliminar un botón (modal de Bootstrap o JS simple).

---

## Ejemplo visual esperado

✅ Botones perfectamente alineados, cuadrados y responsivos  
✅ Estética moderna tipo Stream Deck  
✅ Animación al presionar o activar  
✅ Flexibilidad total en número de botones  
✅ Configuración completa desde la interfaz

