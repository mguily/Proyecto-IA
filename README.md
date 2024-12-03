Descripción del proyecto:

Este proyecto se realizó en segundo de carrera de la asignatura de Inteligencia Artificial (IA) en la Universidad Politécnica de Madrid (UPM). El objetivo principal fue implementar y comparar distintos algoritmos de búsqueda y optimización.

Algoritmos implementados
El proyecto incluyó la implementación de los siguientes algoritmos de búsqueda y optimización:

1. Branch and Bound (B&B)
Descripción: Algoritmo de búsqueda que utiliza una estrategia de poda para reducir el espacio de búsqueda. Explora el árbol de solución de manera eficiente al eliminar subespacios que no cumplen con los criterios de optimalidad.
Aplicación: Utilizado para encontrar la solución óptima de problemas de optimización como el problema de la mochila o el problema de asignación.
2. A (A-Star)*
Descripción: Algoritmo de búsqueda informada que utiliza una función de costo f(n) = g(n) + h(n) para encontrar el camino más corto en un grafo. g(n) representa el costo acumulado desde el nodo inicial hasta el nodo actual, y h(n) es una estimación del costo restante hasta el nodo objetivo.
Aplicación: Implementado para encontrar rutas óptimas en mapas o problemas de búsqueda de caminos en un entorno con obstáculos.
3. Algoritmo Genético Básico
Descripción: Algoritmo de optimización inspirada en la evolución natural. Utiliza operadores de selección, cruce y mutación para generar nuevas soluciones de una población y mejorar la calidad de las soluciones en generaciones sucesivas.
Aplicación: Implementado para resolver problemas de optimización donde la búsqueda de soluciones mediante métodos tradicionales es ineficiente.
4. Algoritmo Genético Avanzado
Descripción: Extensión del algoritmo genético básico con mejoras como la adaptación de tasas de mutación, cruce más complejo (e.g., cruce de un punto, cruce de dos puntos), y estrategias de elitismo para mantener las mejores soluciones.
Aplicación: Utilizado para optimizar problemas de mayor complejidad y comparar la mejora en la calidad de las soluciones con el algoritmo genético básico.

Resultados y comparación
B&B: Proporcionó soluciones óptimas en un tiempo razonable para problemas pequeños, pero presentó dificultades de escalabilidad para problemas más complejos.
A*: Fue efectivo en la búsqueda de rutas óptimas, especialmente en entornos donde la heurística h(n) podía estimar de forma precisa el costo restante.
Algoritmo Genético Básico: Mostró capacidad de encontrar soluciones buenas en problemas de optimización complejos, pero a veces se quedó estancado en óptimos locales.
Algoritmo Genético Avanzado: Superó al genético básico en términos de calidad de soluciones y velocidad de convergencia gracias a las mejoras implementadas.

Tecnologías utilizadas
Lenguaje de programación: Python
