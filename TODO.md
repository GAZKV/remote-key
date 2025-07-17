# ✅ TODO – TeclaRemota

Lista de tareas para el desarrollo incremental del proyecto.

---

## 🧱 Fase 1 – Funcionalidad básica y compatibilidad

- [ ] Reemplazar `keyboard` por `pyautogui` o `SendInput` para enviar teclas que funcionen en juegos como Star Citizen.
- [ ] Crear una función `send_key_sequence()` que reciba una cadena de texto y ejecute las teclas en el servidor.

---

## 🎨 Fase 2 – Personalización visual de botones

- [ ] Agregar soporte para mostrar imágenes como fondo de cada botón (por botón).
- [ ] Permitir definir un color de fondo cuando no se use imagen.
- [ ] Mostrar nombre personalizado en cada botón de forma configurable.

---

## ⚙️ Fase 3 – Panel de configuración visual

- [ ] Agregar botón global de engrane que despliegue un panel de configuración.
- [ ] Diseñar un modal o panel lateral con las opciones de configuración de cada botón.
- [ ] Agregar input para cambiar el nombre visible del botón.
- [ ] Agregar opción para elegir entre imagen o color como fondo.
- [ ] Mostrar paleta de color (`<input type="color">`) cuando se elija fondo por color.
- [ ] Agregar campo de texto para definir la secuencia de teclas que ejecutará el botón.

---

## 💾 Fase 4 – Persistencia y funcionalidad dinámica

- [ ] Guardar configuración de cada botón en `localStorage` o un archivo JSON.
- [ ] Aplicar los cambios visuales en tiempo real cuando se edite la configuración.
- [ ] Cargar la configuración al inicio de la aplicación para reconstruir los botones.
- [ ] Enviar al backend la secuencia de teclas definida por cada botón cuando se presiona.

---