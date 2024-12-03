from Skeleton.ProjectName.src.upmevo import evo_exercises
from Skeleton.ProjectName.src.upmproblems import rcpsp06
from Skeleton.ProjectName.src.upmproblems import rcpsp07
from Skeleton.ProjectName.src.upmproblems import rcpsp10
from Skeleton.ProjectName.src.upmproblems import rcpsp30
import time


def main():

    problemas = [rcpsp06, rcpsp07, rcpsp10, rcpsp30]

    print("SOLUCIONES CON ALGORITMO GENÉTICO BÁSICO")
    for i in range(len(problemas)):
        inicio_tiempo = time.perf_counter()

        print("-------------")
        print("Ejercicio " + str(i + 1))
        print("-------------")
        result = evo_exercises.exercise3(2663677, problemas[i].get_tasks(), problemas[i].get_resources(), problemas[i].get_task_duration(), problemas[i].get_task_resource(), problemas[i].get_task_dependencies())
        print("Resultado: " + str(result))

        fin_tiempo = time.perf_counter()
        duracion = fin_tiempo - inicio_tiempo
        print("Tiempo de ejecución:", duracion, "segundos\n")

    problemas = [rcpsp06, rcpsp07, rcpsp10, rcpsp30]
    print("SOLUCIONES CON ALGORITMO GENÉTICO AVANZADO")

    for i in range(len(problemas)):
        inicio_tiempo = time.perf_counter()

        print("-------------")
        print("Ejercicio " + str(i + 1))
        print("-------------")
        result = evo_exercises.exercise4(7849673, problemas[i].get_tasks(), problemas[i].get_resources(),
                                         problemas[i].get_task_duration(), problemas[i].get_task_resource(),
                                         problemas[i].get_task_dependencies())
        print("Resultado: " + str(result))

        fin_tiempo = time.perf_counter()
        duracion = fin_tiempo - inicio_tiempo
        print("Tiempo de ejecución:", duracion, "segundos\n")

if __name__ == "__main__":
    main()