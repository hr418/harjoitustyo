# Määrittelydokumentti

Projektin ohjelmointikieli: Python

Muut osatut kieliet: JS/TS (ja ainakin React/Next, Astro), html css, C#

Dokumentaation kieli: Suomi

Opinto-ohjelma: tietojenkäsittelytieteen kandidaatti (TKT)

## Yleinen kuvaus

Projektissa vertaillaan reitinhakualgoritmeja. Projektissa toteutetaan ainakin A\* ja jump point search (JPS) algoritmit.

Ohjelma saa syötteeksi 2D pikselikartan, jota käyttämälle se vertailee projektissa toteutettuja algoritmeja. Vertailu visualisoidaan reaaliajassa jotenkin esim. pygamen avulla.

## Aika- ja tilavaativuus tavoitteet

Molempien algoritmien pahimman tapauksen aikavaativuudet ovat $O(E \log V)$, jossa $E$ on kaarien määrä sekä $V$ solmujen määrä.

Molempien algoritmien pahimman tapauksen tilavaativuudet ovat $O(V)$.

## Projektin ydin

Projektin ydin on A\* sekä JPS algoritmit ja niiden tehokas toteutus.

## Lähteet

[https://en.wikipedia.org/wiki/Jump_point_search](https://en.wikipedia.org/wiki/Jump_point_search)

[https://en.wikipedia.org/wiki/A\*\_search_algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
