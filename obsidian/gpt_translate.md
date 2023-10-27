Ok, nie wiem jak zacząć, wiec po prostu o tym napiszę, aby wpisać parę tokenów by ułatwić sobie dalszą rozkminę

Do aplikacji chciałbym dodać funkcjonalność tłumaczenia promptów z polskiego na angielski, wiem, że wszyscy powinni znać angielski, ale jednak to chodzi o coś innego niż brak jego znajomości... Co prawda po polsku znamy zdecydowanie więcej słów, które pozwalają nam opisywać to co widzimy lub co chcemy zobaczyć.

Mysię, że to dobry task na początek aby się trochę zaznajomić z pythonem:D

No dobra to teraz opiszę jak to widzę:
 - na początek ma powstać aplikacja cli w pythonie, która po prostu tłumaczy tekst za pomocą [[open_ai_api]], korzystając z funkcjonalności [[gpt_fm_calling]].
   Klucz api aplikacja powinna wczytać ze ze zmiennej środowiskowej OPENAI_API_KEY.
```
   Szkielet utworzony w: web_sd/apps
   Model: gpt-3.5-turbo
```
 - na początek tłumaczenie tekstu ze zmiennej
 - potem tłumaczenie tekstu podanego na wejściu aplikacji cli
 - potem potem dodanie zapisu rezultatu (wraz z inputem) do pliku json w web_sd/fs
 - potem stworzenie pliku wejściowego json w jednym samplem i podanie ścieżki do pliku jako input cli
 - potem możliwość podania wielu sampli do tłumaczenia w wejściowym pliku json

na razie chyba tyle xD