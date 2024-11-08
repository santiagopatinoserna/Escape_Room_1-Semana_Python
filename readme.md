# Escape Room

## Primer proyecto colaborativo del Bootcamp de Análisis de Datos de Ironhack

Este repositorio forma parte del Bootcamp de Análisis de Datos impartido por Ironhack, específicamente, este es el proyecto de la primera semana.

El juego presenta un mapa con cuatro habitaciones (Casa, Dormitorio 1, Dormitorio 2 y Salón), que aunque están conectadas, todas tienen sus puertas cerradas. El objetivo del juego es salir de la casa recogiendo todas las llaves y un tesoro, que hemos agregado en el código que nos fue otorgado antes de limpiarlo y dividirlo en un archivo `mainfinal.ipynb` y otro `funcionesfinal.py`.

---

## Herramientas

Este primer proyecto se centra en aprender, aplicar y mejorar la lógica de programación básica en Python. Para su desarrollo, utilizamos Google Colab para compartir el código entre compañeros y Visual Studio Code para probar partes del código de manera aislada. Logramos corregir diferencias de funcionamiento para asegurar que el código se ejecute correctamente en ambos entornos.

---

## Objetivos

- El primer objetivo fue dividir el código en dos archivos a partir del archivo original: `mainfinal.ipynb` y `funcionesfinal.py`.
  
- El segundo fue aplicar los conocimientos adquiridos en la primera semana del bootcamp para mejorar el código y la interacción con el usuario, incluyendo:
  * Convertir las palabras ingresadas a minúsculas para evitar problemas de **Key Sensitive**.
  * Mejorar la documentación de las funciones.
  * Agregar bucles `while` y `for` para iterar sobre los elementos.

- El tercer objetivo fue implementar nuevas funciones y cambios en el juego basados en ideas propias para enriquecer el proyecto:
  * Añadimos niveles de dificultad al juego (modo "Easy" y "Hard").
  * Incorporamos una función `push` para interactuar con elementos y descubrir un nuevo objeto como recompensa.
  * En el modo "Hard", se añadió un temporizador que finaliza el juego después de 5 minutos.

---

## Problemas

Durante la semana de desarrollo enfrentamos varios problemas que logramos resolver mediante lectura detallada y revisión continua del código:

- **División en archivos**: Uno de los problemas principales fue que, al separar el código en `mainfinal.ipynb` y `funcionesfinal.py`, varias funciones no funcionaban correctamente, ya que en el archivo original usaban variables globales. La solución fue colocar las parametros correspondiente a las funciones para evitar dependencias globales, haciendo que el código fuera más limpio y robusto.

- **Temporizador en modo "Hard"**: Al agregar el temporizador en el modo "Hard", inicialmente solo mostraba el tiempo al realizar un input. Posteriormente, lo configuramos para que fuera visible en todo momento. También encontramos un bucle que reiniciaba el juego después de finalizar el juego, el cual resolvimos ajustando las condiciones de finalización.

- **Errores menores**: Tuvimos varios errores menores de comillas, mayúsculas y comas, que impedían que el código se ejecutara correctamente. Estos fueron corregidos para que el código fuera funcional.

- **Función `push`**: La función `push` inicialmente no estaba programada correctamente, ya que también encontraba el tesoro al examinar la mesa. La idea era que solo lo descubriera al empujar la mesa. Modificamos las funciones `examine` y `push` para asegurar que el tesoro se obtuviera de forma correcta. Finalmente, el código funcionó como se esperaba.

---

## Entregables

- `funcionesfinal.py`: contiene todas las funciones.
- `mainfinal.ipynb`: contiene los objetos y las relaciones.

---

## Enlaces

Puedes acceder al Escape Room desde Google Colab aquí. [Link al proyecto en Colab]

- **Acceso a `functions.py`**: [Link al archivo]
- **Acceso a `main.ipynb`**: [Link al archivo]
- **Presentación en diapositivas**: [Link a la presentación]

---

## Participantes

- Gerardo Jiménez
- Esteban Cristos

---

## Mapa

(https://github.com/estcr/Escape_Room_1-Semana_Python/blob/main/Imagenes/mapa.png)
