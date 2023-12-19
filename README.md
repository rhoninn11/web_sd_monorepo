# web_sd

## Opis ogólny

Interfejs graficzny typu "mapa myśli" do kreatywnego korzystania z graficznych generatywnych modeli sztucznej inteligencji.
Dalszy rozwój projektu ma na celu stworzenie intuicyjnego interfejsu do korzystania z różnych modeli generatywnych.
Całość oparta na na mikroserwisach, w celu ułatwienia późniejszych "permutacji" w architekturze. 

## Architektura

Aktulanie całość można podzielić na dwie części, pierwsza związana jest z aplikacją webową, druga z obsługą modeli lub/i api w backendzie.

![App screan](assets/arch.png)

### Aplikacja webowa

Aplikacja webowa pozwala na współpracę wielu osób w czasie rzeczywistym w jednej przestrzeni, gdzie każdy jest w stanie obserwować zmiany pozostałych urzytkowników. Zadania generacji z backendu aplikacji przekazywane są do serwera centralnego, który kolejkuje je, a następnie przekazuje do serwerów edgowych. Ilość serwerów edgowych jest skalowalna

![App screan](assets/screan.jpg)

### Ai backend

Serwer centralny aplikacji w tym momencie jest nastawiany na komunikację z jednym klientem. Akutalnie jego tryb działania jest nastawiony na rozsyłanie rządzań interfejsu webowego tj. zapytania txt2img, img2img i inpaint (choć sam interfejs jeszcze tego nie obsługuje) oraz na odsyłanie wyników przetwarzania wraz z informacjami o procesie przetwarzania, bezpośrednio od serverów przetwarzających. 
Serwery przetwarzając implementyją wspomniane wcześniej funkcje stable diffusion, opierają się one bibliotrkę diffusers w sposób, który tylko raz ładuje model a potem dystrybyuje go po różnych pipelinach biblioteki.

## Instrukcje

### Wymagania windows/linux (python)

anaconda

### Konfiguracja środowiskaa (windows powershell)

```
cd web_sd
./script/00_create_env.ps1
```

### Uruchamianie aplikacji (windows powershell)


```
cd web_sd
./script/01_activate.ps1
./script/02_run_central.ps1 lub ./script/03_run_edge.ps1
```
---
### EEG related

#### instalacja oprogramowania:
- zainstalować sobie [conda](https://www.anaconda.com/download/)
- zainstalować sobie [git](https://git-scm.com/download/win)
- zachęcam też do instalacji [vscode](https://code.visualstudio.com/)
- następnie uruchomić powershell
```
conda init
```
- zamknąć i na nowo uruchomić powershell, sprawdzić czy na początku linijki pojawiło się (base)
- aktywacja środowiska:

#### Uruchamianie aplikacji:

Jeżeli środowisko conda nie zostało jeszcze stworzone uruchamiamy:
```
cd web_sd
./script/00_create_env.ps1
```
Uruchomienia serwera eeg (terminal #1):
```
cd web_sd
./script/01_activate.ps1
python ./src/serv/eeg/main.py 4444 3333
```
Uruchomienia clienta eeg (terminal #2):

```
cd web_sd
./script/01_activate.ps1
python ./src/client/eeg/main.py 3333
```

Aplikacje zatrzymuje się klikając __ctrl+c__ :D

#### Znane problemy
Czasami serwer eeg lub blender się zwiesza, zazwyczaja restart serwera pomaga