# AI Social Media Site

Aplikacja webowa napisana w django, imitująca social media w połączeniu z AI.

## Funkcje
- Postawowe funckje rejestracji i logowania do aplikacji.
- Funkcje social media: dodawanie, likeowanie, komentowanie postów tekstowych i ze zdjęciami.
Funkcje związanie ze sztuczną inteligencją:
- Generowanie zdjęć na podstawie promptów użytkownika.
- Wyszukiwanie zdania najlepiej opisującego długi tekst i automatyczne ustawianie tytułu.
- Wyszukiwanie słów kluczowych w tekście i ustawianie ich jako hashtagi postu, po których można później je przeszukiwać.

## Wymagania
```bash
Python ^3.10.12
```
biblioteki:
wszystkie wymagania umieszczone są w pliku requirements.txt. 
Upewnij się, że masz prawidłowo skonfigurowane wirtualne środowisko przed instalacją tych pakietów.
```bash
python -m venv myenv
```
windows:
```bash
myenv\Scripts\activate
```
macOS i Linux:
```bash
source myenv/bin/activate
```
Potrzebna jest również instalacja en_core_web_sm:
```bash
python -m spacy download en_core_web_sm
```
## Instalacja

```bash
git clone https://github.com/aniaprojs/apka
```
```bash
cd projekt
```
```bash
pip install -r requirements.txt
```
```bash
python manage.py runserver
```
Aplikacja będzie dostępna pod adresem `http://localhost:8000/apka`.

## Instrukcja
Sama aplikacja składa się z ekranów rejestracji, logowania, oraz głównego ekranu "Feedu", gdzie znajduje się okienko tworzenia posta ze wszystkimi jego funkcjami, oraz inifinite scroll wszystkich postów z możliwością polubiania lub dodawania komentarzy.
