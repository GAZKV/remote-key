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

- [x] Hacer que los botones se acomoden automáticamente en **cuadrícula responsiva** sin importar la cantidad.
- [x] Mantener **aspecto cuadrado** de todos los botones usando `aspect-ratio: 1 / 1` o trucos con `padding-bottom`.
- [x] Permitir **agregar nuevos botones** desde la interfaz de configuración.
- [x] Permitir **eliminar botones** desde la misma interfaz de configuración.
- [x] Almacenar dinámicamente la cantidad total y sus configuraciones en `localStorage` o archivo JSON.

---

## 🖼 Estilo visual

- [x] Aplicar **bordes redondeados**, **sombra** y **transición suave** a los botones estilo Stream Deck.
- [x] Implementar **animación CSS de “activo”** al presionar un botón (ej: parpadeo, glow, rebote).
- [x] Utilizar `:active` o clases dinámicas con JS para disparar animaciones visuales.

---

## 📱 Adaptación a resolución

- [x] Asegurar que la cuadrícula **adapte tamaño de los botones** automáticamente según la resolución (uso de `grid`, `flex`, `minmax`, etc.).
- [x] Limitar o ajustar el número de columnas según el ancho del viewport.

---

## 🧰 Extras

- [x] Agregar botón "Añadir nuevo botón" que cree un nuevo bloque editable en el panel de configuración.
- [x] Agregar ícono de papelera o botón “Eliminar” por cada botón en la interfaz de configuración.
- [x] Agregar confirmación antes de eliminar un botón (modal de Bootstrap o JS simple).

---

## Ejemplo visual esperado

✅ Botones perfectamente alineados, cuadrados y responsivos  
✅ Estética moderna tipo Stream Deck  
✅ Animación al presionar o activar  
✅ Flexibilidad total en número de botones  
✅ Configuración completa desde la interfaz

## 🐞 Fase 7 – Corrección de errores y mejoras de interfaz (PRIORIDAD)

Objetivo: Corregir errores visuales, de codificación y funcionamiento antes de agregar nuevas funciones complejas.

- [ ] Corregir que al eliminar un botón, el modal de confirmación no se cierre automáticamente.
  - Solución sugerida: usar `bootstrap.Modal.getInstance(modal).hide()` tras confirmar.
- [ ] Reemplazar textos mal codificados como `\u00bf`, `\u00f3`, `\u2699`, etc., por sus versiones unicode legibles.
  - Ejemplo: `¿Eliminar este botón?`, `Configuración`, `⚙`.
- [ ] Asegurar que todos los archivos `.html`, `.js`, y `.json` estén guardados como UTF-8 sin BOM.
- [ ] Validar que todos los textos dinámicos inyectados por JS no utilicen codificación unicode innecesaria.

---

## 🚀 Fase 6 – Funciones avanzadas y calidad de vida

Objetivo: Añadir mejoras de automatización, personalización y compatibilidad para un sistema potente y flexible.

### 🔁 Integración y automatización

- [ ] Permitir ejecutar más de una acción secuencial por botón (macro).
- [ ] Añadir soporte para pausas (`wait 500ms`) entre combinaciones.
- [ ] Opción para ejecutar scripts de sistema o comandos shell desde un botón.
- [ ] Opción para enviar peticiones HTTP desde un botón (control de APIs externas).

### 🌐 Soporte multiplataforma

- [ ] Detectar sistema operativo y seleccionar backend de teclas compatible (`SendInput`, `pyautogui`, etc.).
- [ ] Soporte funcional mínimo en Linux/macOS (si se puede con librerías compatibles).

### 📁 Gestión de configuración

- [ ] Exportar e importar configuración completa como `.json`.
- [ ] Crear perfiles de botones (Star Citizen, Trabajo, OBS...) y cambiar entre ellos desde la UI.
- [ ] Opción para almacenar imágenes de botones como base64 embebido (evita rutas rotas).

### 🧪 Experiencia de usuario

- [ ] Agregar sonido o animación extra al presionar un botón como retroalimentación.
- [ ] Mostrar alerta visual si la secuencia se ejecutó correctamente o falló.
- [ ] Soporte para teclas especiales (funciones, mouse clicks, numpad, etc.).

### 🛡️ Seguridad y control

- [ ] Validar comandos o scripts antes de ejecutarlos (lista blanca o sanitización).
- [ ] Confirmar antes de ejecutar comandos críticos (modal).
- [ ] Agregar modo seguro que desactive la ejecución temporalmente (bloqueo global o por botón).

### 🧰 Extras deseables

- [ ] Agregar sistema de arrastrar y soltar para reordenar botones visualmente.
- [ ] Soporte para íconos SVG o emojis como fondo alternativo a imágenes.
- [ ] Crear soporte de carpetas/subpáginas de botones (Stream Deck folders).