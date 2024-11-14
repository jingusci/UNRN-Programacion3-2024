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

todos_los_billetes(Lista) :-
    setof(Valor, billete(Valor), ListaAscentente),
    reverse(ListaAscentente, Lista).

% Regla para calcular la cantidad de billetes a entregar
billetes_suman(Total, BilletesUsados) :-
    todos_los_billetes(BilletesPosibles),
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
