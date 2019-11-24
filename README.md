# Project for Hackathon+ 2019 
## https://hackathon.miir.gov.pl/)

Problem: są mapy z miejscami dla osób poruszających się na wózku, ale żeby dotrzeć do tego miejsca trzeba nieraz pokonać sporą drogę, która nie zawsze jest dostosowana do poruszania się na wózku. 

Repozytorium zawiera aplikację dla osób poruszających się na wózkach zbierającą dane na temat tego jakimi trasami się poruszają. Wykorzystamy dane z gps, wifi, bluetooth, akcelerometru, żyroskopu, magnetometru żeby ustalić pozycję, prędkość, rodzaj trasy, wskazać momenty w których pojawiały się trudności.
Następnie te dane mogą zostać wykorzystane do tego żeby zbudować mapy i nawigację dla osób poruszających się na wózkach. 

Aplikacja stworzona w react native przy użyciu expo (https://expo.io/), testoswana na iOS - iphone 7 plus.

Dużym plusem tego projektu jest to że jest on szybki do wdrożenia. Jedyne co potrzebujemy to kilkuset użytkowników z zainstalowaną aplikacją. Nie musimy podpisywać dodatkowych umów z innymi firmami lub władzami miast, ani zawierać żadnych partnerstw co potrafi zająć dużo czasu. W ciągu kilku miesięcy można by wygenerować tego typu mapy dla osób na wózkach.

Backend nie został ukończony na czas, proszę korzystać z `simple_backend`

W folderze `visualisation` znajdują się skrypty do przetwarzania i wizualizacji zebranych danych
