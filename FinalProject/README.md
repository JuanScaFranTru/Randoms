# Trabajo Final de Modelos y Simulación
## FaMAF - 2017

<img src="images/lavarropa.jpg" alt="lavarropa" style="display: block; margin: auto; width: 200px;"/>

### Estudiantes:


#### **Francisco Trucco, Juan Scavuzzo**




<div class="page-break"></div>

# Introducción

El problema consiste en realizar una simulación de un servicio de lavadero de
ropa automático. Se desea determinar el tiempo medio, y la desviación
estándar, que transcurre hasta que el lavadero deja de ser operativo. Ésto
ocurre cuando se tiene menos de N máquinas funcionando en un momento dado o,
equivalentemente, cuando posee más de S máquinas defectuosas en el taller de
reparación.

<br>
<br>

## Modelo

El lavadero cuenta con **N** máquinas lavadoras en servicio y **S** máquinas
de respuesto, todas ellas de idéntica marca, modelo y antigúedad.
Por otra parte, el lavadero cuenta con los servicios de técnicos que reparan
las máquinas en simultáneo entre sí pero cada uno de manera secuencial, cuando
éstas se rompen.

Todos los tiempos de funcionamiento de las máquinas hasta descomponerse son
variables aleatorias independientes exponenciales con un tiempo medio de fallar
de **T_r**,

El tiempo de reparación de una máquina que ingresa al taller es una variable
exponencial con tiempo medio igual a **T_f**, independiente de todos los
anteriores.

<br>
<br>

## Approach

Para resolver el problema en cuestión, se desarrolló un algoritmo que simula la
relación que se establece entre los lavarropas que se rompen, aquellos que se
están arreglando y los lavarropas de repuesto.

En esta simulación se considera un 'evento' cuando se rompe una máquina o
cuando se termina de arreglar una.

Entonces, si se rompe una máquina, y no puede ser atendida por el técnico
porque éste está arreglando otra, ésta se considera en la cola de espera para
ser atendida.
Una vez que un operario termina de arreglar un máquina, o bien comienza a
reparar otra o bien se considera "libre".

<div class="page-break"></div>

# Algoritmo y descripción de las Variables

En este trabajo se desarrolló un algoritmo implementado en python que generaliza
la idea de el problema propuesto.
El algoritmo retorna el tiempo que pasa hasta que el sistema deja de ser
operativo, dada una cantidad arbitraria de técnicos reparadores, máquinas de
repuesto, máquinas que deben estar funcionando en todo momento.

Los parámetros del algoritmo son, entonces:

- **n**: Cantidad de máquinas que deben estar funcionando en todo momento.
- **spare**: Cantidad de máquinas de repuesto.
- **Tf**: Tiempo medio de falla de una máquina.
- **Tg**: Tiempo medio de reparación de una máquina por un operador.
- **oper**: Cantidad de operadores que reparan las máquinas.


Para generar los tiempos de retardo de los eventos, definieron las siguientes
funciones auxiliares:

- Para generar el tiempo de falla de una máquina, el cuál está descripto por
una variable aleatoria con distribución exponencial con media **Tf** utilizamos
la siguiente función auxiliar:

```python
def random_fail():
    return exponential(1 / Tf)  # Genera un número aleatorio X ~ ɛ(λ)
```

- Para generar el tiempo que tarda un operario en arreglar una máquina, el cuál
está descripto por una variable aleatoria con distribución exponencial con -
media **Tr** utilizamos la siguiente función auxiliar:

```python
def random_fix():
    return exponential(1 / Tg)  # Genera un número aleatorio X ~ ɛ(λ)
```

Por otro lado, se utilizaron las siguientes variables:

- **t**: Tiempo actual.

- **fails**: Lista de los tiempos de fallos de máquinas. Está ordenada de menor
             a mayor.
- **t_fixed**: Lista de los tiempos en los que se finalizan los arreglos de las
               máquinas. Si hay un valor igual a `inf` significa que existe un
               operario libre.

- **fixing**: Cantidad de operarios que están arreglando máquinas. O
              equivalentemente, la cantidad de máquinas que están siendo
              arregladas.
- **broken**: Cantidad de máquinas que están rotas (incluye aquellas que están
              siendo arregladas).
La cantidad de máquinas a arreglar se calcula como `broken - fixing`




El algoritmo completo es el siguiente:

```python
def simulation(n, spare, Tf, Tg, oper):
    assert n > 0
    assert spare >= 0

    def random_fail():
        return exponential(1 / Tf)

    def random_fix():
        return exponential(1 / Tg)

    inf = float('inf')
    fails = [random_fail() for i in range(n)]
    fails.sort()
    t = 0
    broken = 0
    fixing = 0
    # 'oper' operarios
    t_fixed = [inf] * oper

    while True:  # Mientras funcione la lavandería

        # Como t_fixed siempre está ordenada de mayor a menor, t_fixed guarda en
        # la última posición el mínimo (evento de ese tipo más reciente) y como
        # fails está ordenado de menor a mayor guarda el mínimo en la primera
        # posición. El próximo evento a ocurrir es el mínimo entre fails[0] y
        # t_fixed[oper - 1]

        if fails[0] < t_fixed[oper - 1]: # Un lavarropas ha fallado
            t = fails[0]
            broken += 1

            # Si no hay lavarropas de repuesto la lavandería deja de funcionar
            if broken >= spare + 1:
                return t

            # Tomar un lavarropa de repuesto y reemplazar el viejo
            if broken < spare + 1:
                fails[0] = t + random_fail()
                fails.sort()  # Siempre se ordenan de menor a mayor tiempo

            # Si hay operarios libres ponerlos a trabajar con los lavarropas
            # rotos
            i = 0
            while broken > fixing and t_fixed[i] == inf:
                t_fixed[i] = t + random_fix()
                fixing += 1
                i += 1
            t_fixed.sort(reverse=True)

        else: # Un operario ha terminado de arreglar un lavarropa
            t = t_fixed[oper - 1]
            broken -= 1
            fixing -= 1

            # Si no hay lavarropas por arreglar, el operario queda libre
            if broken == fixing:
                t_fixed[oper - 1] = inf

            # Si hay lavarropas por arreglar, poner el operario a arreglar el
            # lavarropas
            if broken > fixing:
                t_fixed[oper - 1] = t + random_fix()
                fixing += 1
            t_fixed.sort(reverse=True)
```


<div class="page-break"></div>

# Resultados

En todos los casos, se realizaron 10000 simulaciones para calcular la media
y la desviación estándar. Con los resultados de estas simulaciones es que se
contruyeron los distintos histogramas que se presentarán a continuación.

Dado el contexto del problema, resulta de gran interés saber cómo maximizar el
tiempo que tarda el sistema en fallar. Para ésto, los parámetros más
significativas son **spare** y **oper** ya que éstos son los que el dueño del
local modficaría para maximizar sus ganancias.

Es por ésto que los parámetros que se pusieron en comparación son las
anteriormente nombradas.

<img src="images/S2O1.png" alt="S2O1" style="display: block; margin: auto; width: 400px;"/>


<img src="images/S2O2.png" alt="S2O2" style="display: block; margin: auto; width: 400px;"/>

<img src="images/S3O1.png" alt="S3O1" style="display: block; margin: auto; width: 400px;"/>

<img src="images/S2O1vsS2O2.png" alt="S2O1vsS2O2" style="display: block; margin: auto; width: 400px;"/>

<img src="images/S3O1vsS2O2.png" alt="S2O1vsS3O1" style="display: block; margin: auto; width: 400px;"/>

<img src="images/S3O1vsS2O1vsS2O2.png" alt="S3O1vsS2O1vsS2O2" style="display: block; margin: auto; width: 400px;"/>


<div class="page-break"></div>

# Conclusiones
