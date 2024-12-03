import sys

def exercise3(seed=0, tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
    """
        Returns the best solution found by the basic genetic algorithm of exercise 3
        :param seed: used to initialize the random number generator
        :param tasks: number of tasks in the task planning problem with resources
        :param resources: number of resources in the task planning problem with resources
        :param task_duration: list of durations of the tasks
        :param task_resource: list of resources required by each task
        :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
        :return: list with the start time of each task in the best solution found, or empty list if no solution was found
        """
    import random
    import copy
    random.seed(seed)
    def fitness(individuo, task_duration, task_resource, task_dependencies, resources, alphabet):
        fitness = 0
        tareasComienzoInd = [-1] * len(individuo)
        tareasFinInd = [-1] * len(individuo)
        tareasFin = [float('inf')] * len(alphabet)
        tareasComienzo = [float('inf')] * len(alphabet)
        tareasComenzada = [False] * len(individuo)
        tareasTerminada = [False] * len(individuo)

        tiempo = 0
        i = 0

        recursos = resources
        cumple = False
        for m in range(len(individuo)):
            for j in range(len(individuo)):
                if individuo[m] == individuo[j] and m != j:
                    cumple = True
        if not cumple:
            while i < len(individuo):
                for j in range(len(individuo)):
                    if tareasFinInd[j] == tiempo and not tareasTerminada[j] and tareasComenzada[j]:
                        tareasTerminada[j] = True
                        recursos += task_resource[individuo[j] - 1]

                dependencia = False
                for c in task_dependencies:
                    if c[1] == individuo[i] and tareasFin[c[0] - 1] > tiempo and tareasComienzo[c[0] - 1] <= tiempo:
                        dependencia = True

                if recursos >= task_resource[individuo[i] - 1] and not dependencia:
                    tareasComienzoInd[i] = tiempo
                    tareasComenzada[i] = True
                    tareasFinInd[i] = tiempo + task_duration[individuo[i] - 1]
                    recursos -= task_resource[individuo[i] - 1]

                    if tareasFin[individuo[i] - 1] == float('inf'):
                        tareasComienzo[individuo[i] - 1] = tareasComienzoInd[i]
                        tareasFin[individuo[i] - 1] = tareasFinInd[i]

                    i += 1
                else:
                    tiempo += 1

            for j in range(len(individuo)):
                if tareasFinInd[j] > fitness:
                    fitness = tareasFinInd[j]

            cumple = True

            for c in task_dependencies:
                if tareasComienzo[c[1] - 1] < tareasFin[c[0] - 1]:
                    cumple = False

        if cumple:
            return fitness
        else:
            return 0

    def cruce(poblacion, numPoblacion, tasks, pCross, valores_fitness, sumaFitness):
        poblacionCruzada = [[0] * tasks for _ in range(numPoblacion)]
        cruzados = [False] * numPoblacion

        for i in range(numPoblacion):
            probabilidad = random.random()

            individuo1 = poblacion[i]

            if probabilidad < pCross and not cruzados[i]:
                pareja = random.randint(0, numPoblacion - 1)

                while pareja == i and cruzados[pareja]:
                    pareja = random.randint(0, numPoblacion - 1)

                individuo2 = poblacion[pareja]

                cruzados[i] = True
                cruzados[pareja] = True

                poblacionCruzada[i] = individuo1
                poblacionCruzada[pareja] = individuo2

                hijo1 = individuo1[:tasks // 2] + individuo2[tasks // 2:]
                hijo2 = individuo2[:tasks // 2] + individuo1[tasks // 2:]

                for y in range(2):
                    indicePeor = 0
                    peorFitness = float('-inf')

                    for k in range(numPoblacion):
                        if peorFitness < valores_fitness[k] and not cruzados[k]:
                            peorFitness = valores_fitness[k]
                            indicePeor = k

                    if y == 0:
                        poblacionCruzada[indicePeor] = hijo1
                    else:
                        poblacionCruzada[indicePeor] = hijo2

                    cruzados[indicePeor] = True

            else:
                poblacionCruzada[i] = individuo1

        return poblacionCruzada

    def setValores_fitness(poblacion, numPoblacion, sumaFitness, mejorFitness, valores_fitness, task_duration,
                           task_resource, task_dependencies, resources, alphabet):
        sumaFitness[0] = 0
        mejorFitness[0] = float('inf')
        mejorIndividuo = [0] * len(alphabet)

        for i in range(numPoblacion):
            valores_fitness[i] = fitness(poblacion[i], task_duration, task_resource, task_dependencies, resources, alphabet)
            sumaFitness[0] += valores_fitness[i]

            if 0 < valores_fitness[i] < mejorFitness[0]:
                mejorFitness[0] = valores_fitness[i]
                mejorIndividuo = copy.deepcopy(poblacion[i])

        return mejorIndividuo

    def mutacion(poblacion, pMut, tasks, numPoblacion, alphabet, valores_fitness):
        for i in range(numPoblacion):
            if random.random() < pMut and valores_fitness[i] == 0:
                poblacion[i][random.randint(0, tasks - 1)] = alphabet[random.randint(0, tasks - 1)]

    def generarPoblacionInicial(numPoblacion, tasks, alphabet):
        poblacion = [[0] * tasks for _ in range(numPoblacion)]

        for i in range(numPoblacion):
            for j in range(tasks):
                poblacion[i][j] = alphabet[random.randint(0, tasks - 1)]

        return poblacion

    def getComienzoTareas(individuo, task_duration, task_resource, task_dependencies, resources, alphabet):
        tareasComienzoInd = [-1] * len(individuo)
        tareasFinInd = [-1] * len(individuo)
        tareasFin = [float('inf')] * len(alphabet)
        tareasComienzo = [float('inf')] * len(alphabet)
        tareasComenzada = [False] * len(individuo)
        tareasTerminada = [False] * len(individuo)

        tiempo, i, recursos = 0, 0, resources

        while i < len(individuo):
            for j in range(len(individuo)):
                if tareasFinInd[j] == tiempo and not tareasTerminada[j] and tareasComenzada[j]:
                    tareasTerminada[j] = True
                    recursos += task_resource[individuo[j] - 1]

            dependencia = False
            for c in task_dependencies:
                if c[1] == individuo[i] and tareasFin[c[0] - 1] > tiempo and tareasComienzo[c[0]-1] <= tiempo:
                    dependencia = True

            if recursos >= task_resource[individuo[i] - 1] and not dependencia:
                tareasComienzoInd[individuo[i]-1] = tiempo
                tareasComenzada[i] = True
                tareasFinInd[i] = tiempo + task_duration[individuo[i] - 1]
                recursos -= task_resource[individuo[i] - 1]
                if tareasFin[individuo[i] - 1] == float('inf'):
                    tareasComienzo[individuo[i] - 1] = tareasComienzoInd[i]
                    tareasFin[individuo[i] - 1] = tareasFinInd[i]

                i += 1
            else:
                tiempo += 1

        return tareasComienzoInd

    # INICIALIZAR VARIABLES
    numPoblacion = 100
    pCross = 0.9
    pMut = 0.1
    mejorFitness = [float('inf')]
    mejorIndividuo = [0] * tasks
    sumaFitness = [0]
    mediaFitness = [0]
    valores_fitness = [float('inf')] * numPoblacion
    alphabet = list(range(1, tasks + 1))

    # GENERAR POBLACION
    poblacion = generarPoblacionInicial(numPoblacion, tasks, alphabet)

    generacion = 0
    numGeneraciones = 100

    # CALCULAR FITNESS
    mejorIndividuo = setValores_fitness(poblacion, numPoblacion, sumaFitness, mejorFitness, valores_fitness,
                                        task_duration, task_resource, task_dependencies, resources, alphabet)

    # REPETIR TANTAS VECES O HASTA QUE ENCUENTRE SOLUCION
    while generacion < numGeneraciones:
        # CALCULAR FITNESS
        setValores_fitness(poblacion, numPoblacion, sumaFitness, mejorFitness, valores_fitness,
                           task_duration, task_resource, task_dependencies, resources, alphabet)

        # CRUCE DE ORDEN CON PREFERENCIA
        # A LOS QUE MENOS FITNESS TENGAN

        poblacionCruzada = cruce(poblacion, numPoblacion, tasks, pCross, valores_fitness, sumaFitness[0])

        # COMPARAR CON LA ANTERIOR POBLACION
        mejorFitnessCuzada = float('inf')
        valores_fitnessCruzada = [0] * numPoblacion

        for i in range(numPoblacion):
            aux = fitness(poblacionCruzada[i], task_duration, task_resource, task_dependencies, resources, alphabet)
            valores_fitnessCruzada[i] = aux
            if mejorFitnessCuzada > aux > 0:
                mejorFitnessCuzada = aux

        if mejorFitnessCuzada < mejorFitness[0]:
            poblacion = poblacionCruzada

            for i in range(numPoblacion):
                valores_fitness[i] = valores_fitnessCruzada[i]

            mejorFitness[0] = mejorFitnessCuzada

        mutacion(poblacion, pMut, tasks, numPoblacion, alphabet, valores_fitness)

        mejorIndividuo = setValores_fitness(poblacion, numPoblacion, sumaFitness, mejorFitness, valores_fitness,
                                            task_duration, task_resource, task_dependencies, resources, alphabet)

        generacion += 1

    if mejorFitness[0] == float('inf'):
        mejorFitness[0] = 0
        mejorIndividuo = [0] * tasks

    print("Mejor Makespan: ", mejorFitness[0])
    print("Planificacion: ", mejorIndividuo)

    if mejorFitness[0] != 0:
        return getComienzoTareas(mejorIndividuo, task_duration, task_resource, task_dependencies, resources, alphabet)
    else:
        return [0] * tasks


def exercise4(seed=0, tasks=0, resources=0, task_duration=[], task_resource=[], task_dependencies=[]):
        """
        Returns the best solution found by the advanced genetic algorithm of exercise 4
        :param seed: used to initialize the random number generator
        :param tasks: number of tasks in the task planning problem with resources
        :param resources: number of resources in the task planning problem with resources
        :param task_duration: list of durations of the tasks
        :param task_resource: list of resources required by each task
        :param task_dependencies: list of dependencies (expressed as binary tuples) between tasks
        :return: list with the start time of each task in the best solution found, or empty list if no solution was found
        """
        import random
        random.seed(seed)
        def fitness(individuo, task_duration, task_resource, task_dependencies, resources, alphabet):
            fitness = 0
            tareasComienzoInd = [-1] * len(individuo)
            tareasFinInd = [-1] * len(individuo)
            tareasFin = [float('inf')] * len(alphabet)
            tareasComienzo = [float('inf')] * len(alphabet)
            tareasComenzada = [False] * len(individuo)
            tareasTerminada = [False] * len(individuo)

            tiempo, i, recursos = 0, 0, resources

            while i < len(individuo):
                for j in range(len(individuo)):
                    if tareasFinInd[j] == tiempo and not tareasTerminada[j] and tareasComenzada[j]:
                        tareasTerminada[j] = True
                        recursos += task_resource[individuo[j] - 1]

                dependencia = False
                for c in task_dependencies:
                    if c[1] == individuo[i] and tareasFin[c[0] - 1] > tiempo and tareasComienzo[c[0]-1] <= tiempo:
                        dependencia = True

                if recursos >= task_resource[individuo[i] - 1] and not dependencia:
                    tareasComienzoInd[i] = tiempo
                    tareasComenzada[i] = True
                    tareasFinInd[i] = tiempo + task_duration[individuo[i] - 1]
                    recursos -= task_resource[individuo[i] - 1]

                    if tareasFin[individuo[i] - 1] == float('inf'):
                        tareasComienzo[individuo[i] - 1] = tareasComienzoInd[i]
                        tareasFin[individuo[i] - 1] = tareasFinInd[i]

                    i += 1
                else:
                    tiempo += 1

            for j in range(len(individuo)):
                if tareasFinInd[j] > fitness:
                    fitness = tareasFinInd[j]

            for c in task_dependencies:
                if tareasComienzo[c[1] - 1] < tareasFin[c[0] - 1]:
                    fitness += 100
            return fitness

        def cruce(poblacion, numPoblacion, tasks, pCross, valores_fitness, mejorIndividuo):
            poblacionCruzada = [[0] * tasks for _ in range(numPoblacion)]
            cruzados = [False] * numPoblacion
            seguir = True
            m = 0

            while m < numPoblacion and seguir:
                if poblacion[m] == mejorIndividuo:
                    poblacionCruzada[m] = mejorIndividuo
                    seguir = False
                m += 1

            numCruzados = 0

            for i in range(numPoblacion):
                individuo1 = poblacion[i]
                probabilidad = random.random()

                if probabilidad < pCross and not cruzados[
                    i] and individuo1 != mejorIndividuo and numCruzados < numPoblacion / 2:
                    poblacionCruzada[i] = individuo1
                    candidato1 = int(random.random() * (numPoblacion - 1))

                    while cruzados[candidato1]:
                        candidato1 = int(random.random() * (numPoblacion - 1))

                    candidato2 = int(random.random() * (numPoblacion - 1))

                    while candidato1 == candidato2 or cruzados[candidato2]:
                        candidato2 = int(random.random() * (numPoblacion - 1))

                    valorFitness1 = valores_fitness[candidato1]
                    valorFitness2 = valores_fitness[candidato2]
                    pareja = candidato1 if valorFitness1 < valorFitness2 else candidato2
                    cruzados[pareja] = True
                    individuo2 = poblacion[pareja]
                    poblacionCruzada[i] = individuo1
                    poblacionCruzada[pareja] = individuo2
                    hijo1 = [0] * tasks
                    hijo2 = [0] * tasks
                    tareasUsadas1 = [False] * tasks
                    tareasUsadas2 = [False] * tasks
                    tercioSeleccionado = tasks // 3

                    for j in range(tercioSeleccionado, tasks - tercioSeleccionado):
                        hijo1[j] = individuo1[j]
                        hijo2[j] = individuo2[j]
                        tareasUsadas1[individuo1[j] - 1] = True
                        tareasUsadas2[individuo2[j] - 1] = True

                    for x in range(tasks):
                        y = 0
                        seguir = True

                        if(x<tercioSeleccionado or x>=tasks-tercioSeleccionado):
                            while seguir and y < tasks:
                                if not tareasUsadas1[individuo2[y] - 1]:
                                    seguir = False
                                else: y += 1

                            if(y<tasks):
                                hijo1[x] = individuo2[y]
                                tareasUsadas1[individuo2[y] - 1] = True
                            y = 0
                            seguir = True

                            while seguir and y < tasks:
                                if not tareasUsadas1[individuo2[y] - 1]:
                                    seguir = False
                                else: y += 1
                            if(y<tasks):
                                hijo2[x] = individuo2[y]
                                tareasUsadas2[individuo2[y] - 1] = True

                    for y in range(2):
                        indicePeor = 0
                        peorFitness = float('-inf')

                        for k in range(numPoblacion):
                            if peorFitness < valores_fitness[k] and not cruzados[k]:
                                peorFitness = valores_fitness[k]
                                indicePeor = k

                        if y == 0:
                            poblacionCruzada[indicePeor] = hijo1
                        else:
                            poblacionCruzada[indicePeor] = hijo2

                        cruzados[indicePeor] = True

                    numCruzados += 2

                else:
                    poblacionCruzada[i] = individuo1

            return poblacionCruzada

        def setValores_fitness(poblacion, numPoblacion, mejorFitness, valores_fitness, tasks_duration, task_resource,
                               task_dependencies, resources, alphabet):
            mejorFitness[0] = float('inf')
            mejorIndividuo = [0] * len(alphabet)

            for i in range(numPoblacion):
                valores_fitness[i] = fitness(poblacion[i], tasks_duration, task_resource, task_dependencies, resources,
                                             alphabet)

                if valores_fitness[i] < mejorFitness[0]:
                    mejorFitness[0] = valores_fitness[i]
                    mejorIndividuo = poblacion[i]

            return mejorIndividuo

        def mutacion(poblacion, pMut, tasks, numPoblacion, alphabet, valores_fitness):
            sumaTiempoTotal = sum(task_duration)

            for i in range(numPoblacion):
                individuo = poblacion[i]
                probabilidad = random.random()

                if probabilidad < pMut and valores_fitness[i] > sumaTiempoTotal:
                    posicion1 = int(random.random() * (tasks - sys.float_info.epsilon))
                    posicion2 = int(random.random() * (tasks - sys.float_info.epsilon))

                    while posicion1 == posicion2:
                        posicion2 = int(random.random() * (tasks - sys.float_info.epsilon))

                    aux = individuo[posicion1]
                    individuo[posicion1] = individuo[posicion2]
                    individuo[posicion2] = aux

        def generarPoblacionInicial(numPoblacion, tasks, alphabet):
            poblacion = [[-1] * tasks for _ in range(numPoblacion)]

            for i in range(numPoblacion):
                individuo = [-1] * tasks

                tareasUsadas = [False] * tasks

                for j in range(tasks):
                    tarea = alphabet[int(random.random() * (tasks - sys.float_info.epsilon))]

                    while tareasUsadas[tarea - 1]:
                        tarea = alphabet[int(random.random() * (tasks - sys.float_info.epsilon))]

                    tareasUsadas[tarea - 1] = True
                    individuo[j] = tarea

                poblacion[i] = individuo

            return poblacion

        def getComienzoTareas(individuo, task_duration, task_resource, resources, alphabet):
            tareasComienzoInd = [-1] * len(individuo)
            tareasFinInd = [-1] * len(individuo)
            tareasFin = [float('inf')] * len(alphabet)
            tareasComienzo = [float('-inf')] * len(alphabet)
            tareasComenzada = [False] * len(individuo)
            tareasTerminada = [False] * len(individuo)

            for i in range(len(individuo)):
                tareasComienzoInd[i] = -1
                tareasFinInd[i] = -1
                tareasFin[i] = float('inf')
                tareasComienzo[i] = float('-inf')
                tareasComenzada[i] = False
                tareasTerminada[i] = False

            tiempo, i, recursos = 0, 0, resources

            while i < len(individuo):
                for j in range(len(individuo)):
                    if tareasFinInd[j] == tiempo and not tareasTerminada[j] and tareasComenzada[j]:
                        tareasTerminada[j] = True
                        recursos += task_resource[individuo[j] - 1]

                dependencia = False
                for c in task_dependencies:
                    if c[1] == individuo[i] and tareasFin[c[0] - 1] > tiempo and tareasComienzo[c[0]-1] <= tiempo:
                        dependencia = True

                if recursos >= task_resource[individuo[i] - 1] and not dependencia:
                    tareasComienzoInd[i] = tiempo
                    tareasComenzada[i] = True
                    tareasFinInd[i] = tiempo + task_duration[individuo[i] - 1]
                    recursos -= task_resource[individuo[i] - 1]

                    if tareasFin[individuo[i] - 1] == float('inf'):
                        tareasComienzo[individuo[i] - 1] = tareasComienzoInd[i]
                        tareasFin[individuo[i] - 1] = tareasFinInd[i]

                    i += 1
                else:
                    tiempo += 1

            return tareasComienzoInd

        # INICIALIZAR VARIABLES
        sumaTiempoTotal = sum(task_duration)
        pCross = tasks / 6.66
        numPoblacion = tasks * 17
        pMut = numPoblacion / 1000
        mejorFitness = [float('inf')]
        mejorIndividuo = [0] * tasks
        valores_fitness = [float('inf')] * numPoblacion
        alphabet = [i + 1 for i in range(tasks)]

        # GENERAR POBLACION
        poblacion = generarPoblacionInicial(numPoblacion, tasks, alphabet)

        generacion = 0
        numGeneraciones = 100

        # CALCULAR FITNESS
        mejorIndividuo = setValores_fitness(poblacion, numPoblacion, mejorFitness, valores_fitness, task_duration,
                                            task_resource, task_dependencies, resources, alphabet)

        # REPETIR TANTAS VECES O HASTA QUE ENCUENTRE SOLUCION
        while generacion < numGeneraciones:
            # CALCULAR FITNESS
            mejorIndividuo = setValores_fitness(poblacion, numPoblacion, mejorFitness, valores_fitness, task_duration,
                                                task_resource, task_dependencies, resources, alphabet)
            # CRUCE DE ORDEN CON PREFERENCIA
            # A LOS QUE MENOS FITNES TENGAN
            poblacionCruzada = cruce(poblacion, numPoblacion, tasks, pCross, valores_fitness, mejorIndividuo)
            # COMPARAR CON LA ANTERIOR POBLACION
            mejorFitnessCuzada = float('inf')
            valores_fitnessCruzada = [0] * numPoblacion

            for i in range(numPoblacion):
                aux = fitness(poblacionCruzada[i], task_duration, task_resource, task_dependencies, resources, alphabet)
                valores_fitnessCruzada[i] = aux

                if mejorFitnessCuzada > aux > 0:
                    mejorFitnessCuzada = aux

            if mejorFitnessCuzada < mejorFitness[0]:
                poblacion = poblacionCruzada

                for i in range(numPoblacion):
                    valores_fitness[i] = valores_fitnessCruzada[i]

                mejorFitness[0] = mejorFitnessCuzada

            mutacion(poblacion, pMut, tasks, numPoblacion, alphabet, valores_fitness)
            mejorIndividuo = setValores_fitness(poblacion, numPoblacion, mejorFitness, valores_fitness, task_duration,
                                                task_resource, task_dependencies, resources, alphabet)

            generacion += 1

        if mejorFitness[0] >= sumaTiempoTotal:
            mejorFitness[0] = 0
            mejorIndividuo = [0] * tasks
        print("Mejor Makespan: ", mejorFitness[0])
        print("Planificacion: ", mejorIndividuo)
        if mejorFitness[0] != 0:
            return getComienzoTareas(mejorIndividuo, task_duration, task_resource, resources, alphabet)
        else:
            return [0] * tasks

