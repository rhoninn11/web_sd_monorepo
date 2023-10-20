# web_sd

Interfejs graficzny to korzystania z generatywnych modeli sztucznej inteligencji. Całość oparta na na mikroserwisach składa się aplikacji webowej dedykowanego dla niej serwera, oraz dodatkowych serwerów przetwarzających generowanie grafiki za pomocą stable diffusion. 

![App screan](assets/screan.jpg)


Aplikacja webowa pozwala na współpracę wielu osób w czasie rzeczywistym w jednej przestrzeni, gdzie każdy jest w stanie obserwować zmiany pozostałych urzytkowników. Zadania generacji z backendu aplikacji przekazywane są do serwera centralnego, który kolejkuje je, a następnie przekazuje do serwerów edgowych. Ilość serwerów edgowych jest skalowalna

![App screan](assets/arch.png)

## Plan działania:

- [x] dodanie screana jak to wygląda
- [x] uwspólnienie typów dla tsa
- [x] stworzenie którkiego opisu aplikacji
- [x] dodanie części pythonowej 
- [ ] opisanie części pythonowej
- [x] stworzenie grafu połączeń między serwisami na ilustracji
- [ ] pomyślenie nad następnymi krokami

    