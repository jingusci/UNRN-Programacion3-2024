% Base de conocimientos de billetes
billete(ars, 10000).
billete(ars, 2000).
billete(ars, 1000).
billete(ars, 500).
billete(ars, 200).
billete(ars, 100).
billete(ars, 50).
billete(ars, 20).
billete(ars, 10).
billete(ars, 5).

billete(usd, 100).
billete(usd, 50).
billete(usd, 20).
billete(usd, 10).
billete(usd, 5).
billete(usd, 2).
billete(usd, 1).

todos_los_billetes(Moneda, Lista) :-
    setof(Valor, billete(Moneda, Valor), ListaAscentente),
    reverse(ListaAscentente, Lista).

% Regla para calcular la cantidad de billetes a entregar:
% Al evaluar billetes_suman(moneda, monto, X), se obtienen todas las combinaciones
% de billetes que suman monto. Las combinaciones están ordenadas de manera
% que las primeras de la lista usan la mayor cantidad posible de los
% billetes más grandes.

billetes_suman(Moneda, Total, BilletesUsados) :-
    todos_los_billetes(Moneda, BilletesPosibles),
    billetes_suman_usando(Total, BilletesUsados, BilletesPosibles).

% caso base: si el total es 0 la lista de billetes está vacía.
billetes_suman_usando(0, [], _).

% Caso recursivo: Combinaciones que usa el billete más grande.
billetes_suman_usando(Total, [(BilleteActual, Cantidad)|Resto], [BilleteActual|BilletesRestantes]) :-
    Total >= BilleteActual,
    MaxCantidad is Total // BilleteActual, % Calcular cuantos billetes se pueden usar de esta denominación.
    between_desc(MaxCantidad, 1, Cantidad),  % Prueba diferentes cantidades de billetes, desde el máximo posible hasta 1.
    MontoRestante is Total - Cantidad * BilleteActual,
    billetes_suman_usando(MontoRestante, Resto, BilletesRestantes).

% Caso recursivo: Combinaciones que no usan el billete más grande.
billetes_suman_usando(Total, BilletesUsados, [_|BilletesRestantes]) :-
    Total > 0,
    billetes_suman_usando(Total, BilletesUsados, BilletesRestantes).

% Esta regla es igual que between: pasa por todos lo números entre Start y End.
% La diferencia es que pasa en orden descendiente, lo cual nos sirve para evaluar
% primero las opciones de vuelto que usan menos billetes.
between_desc(Start, End, Start) :-
    Start >= End.
between_desc(Start, End, X) :-
    Start > End,
    Next is Start - 1,
    between_desc(Next, End, X).
