import sys

def exercise1(tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    """
    Returns the best solution found by the branch and bound algorithm of exercise 1
    :param tasks: number of tasks in the task planning problem with resources
    :param resources: number of resources in the task planning problem with resources
    :param task_duration: list of durations of the tasks
    :param task_resource: list of resources required by each task
    :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
    :return: list with the start time of each task in the best solution found, or empty list if no solution was found
    """

    def branch_and_bound(profundidad, dependencias_tarea_minus1, planificacion_actual, recursos_actuales,
                         tarea_planificada, mejor_makespan,
                         mejor_planificacion):
        if profundidad == tasks:
            todo_true = [True] * tasks
            if todo_true == tarea_planificada:
                makespan_actual = calcular_makespan(planificacion_actual,
                                                    dependencias_tarea_minus1, [0] * tasks)
                if makespan_actual < mejor_makespan [0]:
                    mejor_makespan [0] = makespan_actual
                    mejor_planificacion [:] = planificacion_actual [:]
            return

        for i in range(tasks):
            if not tarea_planificada [i] and check_dependencies(i, dependencias_tarea_minus1, tarea_planificada):
                tarea_planificada [i] = True
                planificacion_actual [profundidad] = i

                if check_resources(i, recursos_actuales):
                    recursos_actuales = recursos_actuales + task_resource [i]
                else:
                    recursos_actuales = task_resource [i]
                profundidad = profundidad + 1
                branch_and_bound(profundidad, dependencias_tarea_minus1, planificacion_actual, recursos_actuales,
                                 tarea_planificada, mejor_makespan,
                                 mejor_planificacion)
                profundidad = profundidad - 1
                recursos_actuales = recursos_actuales - task_resource [i]
                desmarcar_tarea(i, dependencias_tarea_minus1, tarea_planificada)

    def desmarcar_tarea(tarea, dependencias_tarea_minus1, tarea_planificada):
        tarea_planificada [tarea] = False

        for dependencia in dependencias_tarea_minus1:
            if dependencia [0] == tarea:
                desmarcar_tarea(dependencia [1], dependencias_tarea_minus1, tarea_planificada)

    def check_dependencies(tarea, dependencias_tarea_minus1, tarea_planificada):
        no_tiene_dependencias = True
        for dependencia in dependencias_tarea_minus1:
            if dependencia [1] == tarea:
                no_tiene_dependencias = False
                break

        if no_tiene_dependencias:
            return True

        for dependencia in dependencias_tarea_minus1:
            if dependencia [1] == tarea and not tarea_planificada [dependencia [0]]:
                return False
        return True

    def check_resources(tarea, recursos_actuales):
        return recursos_actuales + task_resource [tarea] <= resources

    def calcular_makespan(planificacion, dependencias_tarea_minus1, inicio_tarea):
        lista_seg_rec = [0]

        tiempos_fin_tarea = [0] * len(planificacion)

        for k in range(len(planificacion)):
            tarea = planificacion [k]
            contador = inicio_tarea [planificacion [k - 1]] if k != 0 else 0
            dependientes = son_dependientes(tarea, dependencias_tarea_minus1)
            i = 0
            while i < task_duration [tarea]:
                if k != 0:
                    if check_resources(tarea, lista_seg_rec [contador]) and tiempos_dependencias_completados(contador,
                                                                                                             dependientes,
                                                                                                             tiempos_fin_tarea):
                        inicio_tarea [tarea] = contador - i
                        lista_seg_rec [contador] += task_resource [tarea]
                        tiempos_fin_tarea [tarea] = task_duration [tarea] + inicio_tarea [tarea]
                    else:
                        i -= 1
                    lista_seg_rec.append(0)
                    contador += 1
                else:
                    for j in range(task_duration [tarea]):
                        lista_seg_rec [j] = task_resource [tarea]
                        lista_seg_rec.append(0)
                    tiempos_fin_tarea [tarea] = task_duration [tarea]
                i += 1

        lista_seg_rec = [x for x in lista_seg_rec if x != 0]

        return len(lista_seg_rec)

    def son_dependientes(tarea, dependencias_tarea_minus1):
        dependientes = []
        for dependencia in dependencias_tarea_minus1:
            if dependencia [1] == tarea:
                dependientes.append(dependencia [0])
        return dependientes

    def tiempos_dependencias_completados(contador, dependientes, tiempos_fin_tarea):
        for dependiente in dependientes:
            if tiempos_fin_tarea [dependiente] > contador:
                return False
        return True

    mejor_planificacion = [0] * tasks
    planificacion_actual = [0] * tasks
    inicio_tarea = [0] * tasks
    mejor_makespan = [sys.maxsize]
    tarea_planificada = [False] * tasks

    dependencias_tarea_minus1 = [list(dependencia) for dependencia in task_dependencies]

    for i in range(len(dependencias_tarea_minus1)):
        dependencias_tarea_minus1 [i] [0] = dependencias_tarea_minus1 [i] [0] - 1
        dependencias_tarea_minus1 [i] [1] = dependencias_tarea_minus1 [i] [1] - 1

    branch_and_bound(0, dependencias_tarea_minus1, planificacion_actual, 0,
                     tarea_planificada, mejor_makespan, mejor_planificacion)
    calcular_makespan(mejor_planificacion, dependencias_tarea_minus1, inicio_tarea)

    for i in range(len(planificacion_actual)):
        mejor_planificacion [i] += 1

    print("Makespan:", mejor_makespan [0])
    print("Planificación:", mejor_planificacion)
    return inicio_tarea


def exercise2(tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    """
    Returns the best solution found by the A* algorithm of exercise 2
    :param tasks: number of tasks in the task planning problem with resources
    :param resources: number of resources in the task planning problem with resources
    :param task_duration: list of durations of the tasks
    :param task_resource: list of resources required by each task
    :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
    :return: list with the start time of each task in the best solution found, or empty list if no solution was found
    """

    def algoritmo_a(dependencias_tarea, planificacion, visitado):
        lista_seg_rec = []
        while len(planificacion) < len(visitado):
            c = calcular_heuristica(dependencias_tarea, visitado, planificacion, lista_seg_rec)
            visitado [c] = True
            planificacion.append(c)

    def calcular_heuristica(dependencias_tarea, visitados, planificacion, lista_seg_rec):
        if not planificacion:
            mejor_dependencia = 0
            mas_dependencias = 0
            for i in range(len(visitados)):
                if check_dependencies(i, dependencias_tarea, visitados) and len(
                        dependen(i, dependencias_tarea)) > mejor_dependencia and check_resources(i, 0):
                    mas_dependencias = i
                    mejor_dependencia = len(dependen(i, dependencias_tarea))
            for i in range(task_duration [mas_dependencias]):
                lista_seg_rec.insert(i, task_resource [mas_dependencias])
            return mas_dependencias
        else:
            disponibles = []
            contador = 0
            while lista_seg_rec [contador] == resources:
                contador += 1
            for _ in range(1000000):
                for i in range(len(visitados)):
                    if not visitados [i] and check_dependencies(i, dependencias_tarea, visitados) and check_resources(i,
                                                                                                                      lista_seg_rec [
                                                                                                                          contador]):
                        disponibles.append(i)
                if not disponibles:
                    lista_seg_rec.append(0)
                    contador += 1
                else:
                    mismas_dependencias = []
                    dependencias_mejor = 0
                    for disponible in disponibles:
                        dependencias = len(dependen(disponible, dependencias_tarea))
                        if dependencias == dependencias_mejor:
                            mismas_dependencias.append(disponible)
                        elif dependencias > dependencias_mejor:
                            mismas_dependencias = [disponible]
                            dependencias_mejor = dependencias

                    resultado = menor_tiempo(task_duration, mismas_dependencias)

                    for i in range(task_duration [resultado]):
                        lista_seg_rec.append(0)
                        lista_seg_rec [contador] += task_resource [resultado]
                        contador += 1

                    return resultado
        return 0

    def menor_tiempo(duracion_tarea, mismas_dependencias):
        if len(mismas_dependencias) == 1:
            return mismas_dependencias [0]
        else:
            menor = 0
            duracion_menor = float('inf')
            for tarea in mismas_dependencias:
                duracion = duracion_tarea [tarea]
                if duracion < duracion_menor:
                    menor = tarea
                    duracion_menor = duracion
            return menor

    def calcular_makespan(planificacion, dependencias_tarea_minus1, inicio_tarea):
        lista_seg_rec = [0]

        tiempos_fin_tarea = [0] * len(planificacion)

        for k in range(len(planificacion)):
            tarea = planificacion [k]
            contador = inicio_tarea [planificacion [k - 1]] if k != 0 else 0
            dependientes = son_dependientes(tarea, dependencias_tarea_minus1)
            i = 0
            while i < task_duration [tarea]:
                if k != 0:
                    if task_resource [tarea] + lista_seg_rec [
                        contador] <= resources and tiempos_dependencias_completados(contador, dependientes,
                                                                                    tiempos_fin_tarea):
                        inicio_tarea [tarea] = contador - i
                        lista_seg_rec [contador] += task_resource [tarea]
                        tiempos_fin_tarea [tarea] = task_duration [tarea] + inicio_tarea [tarea]
                    else:
                        i -= 1
                    lista_seg_rec.append(0)
                    contador += 1
                else:
                    for j in range(task_duration [tarea]):
                        lista_seg_rec [j] = task_resource [tarea]
                        lista_seg_rec.append(0)
                    tiempos_fin_tarea [tarea] = task_duration [tarea]
                i += 1

        lista_seg_rec = [x for x in lista_seg_rec if x != 0]

        return len(lista_seg_rec)

    def son_dependientes(tarea, dependencias_tarea):
        dependientes = []
        for dependencia in dependencias_tarea:
            if dependencia [1] == tarea:
                dependientes.append(dependencia [0])
        return dependientes

    def dependen(tarea, dependencias_tarea):
        dependientes = []
        for dependencia in dependencias_tarea:
            if dependencia [0] == tarea:
                dependientes.append(dependencia [1])
        return dependientes

    def tiempos_dependencias_completados(contador, dependientes, tiempos_fin_tarea):
        for dependiente in dependientes:
            if tiempos_fin_tarea [dependiente] > contador:
                return False
        return True

    def check_dependencies(tarea, dependencias_tarea, tarea_planificada):
        no_tiene_dependencias = True
        for dependencia in dependencias_tarea:
            if dependencia [1] == tarea:
                no_tiene_dependencias = False
                break
        if no_tiene_dependencias:
            return True
        for dependencia in dependencias_tarea:
            if dependencia [1] == tarea and not tarea_planificada [dependencia [0]]:
                return False
        return True

    def check_resources(tarea, ultimo_recurso):
        return ultimo_recurso + task_resource [tarea] <= resources

    planificacion = []
    visitado = [False] * tasks
    inicio_tarea = [0] * tasks
    dependencias_tarea_minus1 = [list(map(lambda x: x - 1, dependencia)) for dependencia in task_dependencies]

    algoritmo_a(dependencias_tarea_minus1, planificacion, visitado)

    maskespan = calcular_makespan(planificacion, dependencias_tarea_minus1, inicio_tarea)

    planificacion = [x + 1 for x in planificacion]

    print("Makespan:", maskespan)
    print("Planificación:", planificacion)
    return inicio_tarea
