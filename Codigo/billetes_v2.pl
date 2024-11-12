%%writefile billetes.pl

% Base de conocimientos de billetes
billete(10000).
billete(2000).
billete(1000).
billete(500).
billete(200).
billete(100).
billete(50).
billete(20).
billete(10).
billete(5).

% Regla para calcular la cantidad de billetes a entregar
calcular_vuelto(Vuelto, Resultado) :-
    calcular_billetes(Vuelto, [10000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5], Resultado).

% Caso base: si el vuelto es 0, no se entregan billetes.
calcular_billetes(0, _, []).

% Caso en el que se puede usar al menos un billete de la denominación actual.
calcular_billetes(Vuelto, [Billete|BilletesRestantes], [(Billete, Cantidad)|Resto]) :-
    Vuelto >= Billete,
    MaxCantidad is Vuelto // Billete,  % Calcular el máximo posible de billetes para esta denominación
    between(1, MaxCantidad, Cantidad),  % Prueba diferentes cantidades de billetes, desde 1 hasta el máximo posible
    NuevoVuelto is Vuelto - Cantidad * Billete,
    calcular_billetes(NuevoVuelto, BilletesRestantes, Resto).

% Caso en el que no se usa ningún billete de la denominación actual.
calcular_billetes(Vuelto, [_|BilletesRestantes], Resultado) :-
    calcular_billetes(Vuelto, BilletesRestantes, Resultado).


