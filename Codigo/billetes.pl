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

% Regla auxiliar para calcular los billetes
calcular_billetes(0, _, []). % Caso base: si el vuelto es 0, no se entregan billetes
calcular_billetes(Vuelto, [Billete|BilletesRestantes], [(Billete, Cantidad)|Resto]) :-
    Vuelto >= Billete,
    Cantidad is Vuelto // Billete,
    NuevoVuelto is Vuelto mod Billete,
    calcular_billetes(NuevoVuelto, BilletesRestantes, Resto).
calcular_billetes(Vuelto, [_|BilletesRestantes], Resultado) :-
    calcular_billetes(Vuelto, BilletesRestantes, Resultado).

% Ejemplo de consulta para obtener el vuelto
% consulta: calcular_vuelto(3870, Resultado).
