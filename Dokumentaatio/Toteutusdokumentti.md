# Toteutusdokumentti

## Ohjelman Rakenne

Ohjelman ydin ovat algoritmit, jotka perivät luokan PathFindingAlgorithm. Luokka määrittelee mitä metodeja ja attribuutteja jokaisella algoritmilla tulee olla, jotta verailu onnistuu. Lisäksi luokassa on metodi measure_performance, joka mittaa algoritmin nopeutta.

JPS algoritmi perii A\* algoritmin, koska siinä voidaan hyödyntää monia sen metodeja.

app.py tiedosto on ytimestä irronnainen osa, joka hoitaa itse visualisaation ja tulostaa algoritmien tilastot.

## Aika- Tilavaativuudet

A\* pseudokoodi:

    aloita prioriteettijonolla (avoin joukko), jossa on aloitus-solmu
        kun jono ei ole tyhjä:
            ota jonosta solmu, jolla on pienin f = g + h
            jos solmu on jo tarkistettu, skippaa se
            lisää solmu suljettuun joukkoon
            jos solmu on maali, lopeta
            tarkista solmun naapurit
            jokaisella avoimella naapurilla:
                laske uusi g arvo
                jos uusi polku on parempi kuin paras aiemmin tunnettu:
                    tallenna uusi arvo
                    lisää naapuri prioriteettijonoon (avoimeen joukkoon)

JPS pseudokoodi:

    aloita prioriteettijonolla (avoin joukko), jossa on aloitus-solmu
    kun jono ei ole tyhjä:
        ota jonosta solmu, jolla on pienin f = g + h
        jos solmu on jo tarkistettu, skippaa se
        lisää solmu suljettuun joukkoon
        jos solmu on maali, lopeta
        valitse vain hyödylliset suunnat tästä solmusta
        jokaisella hyödyllisellä suunnalla:
            jatka suuntaan kunnes:
                osut seinään
                osut maaliin
                löydät pakotetun naapurin
            jos hyppypiste löydettiin, ja polku on parempi kuin paras aiemmin tunnettu:
                tallenna uusi arvo
                lisää naapuri prioriteettijonoon (avoimeen joukkoon)

A\* aikavaativuus: Jokainen solmu saatetaan tarkistaa kerran, ja prioriteettijonon operaatiot ovat aikavaativuudeltaan $\log V$, jossa $V$ on solmujen määrä. Joten algoritmin aikavaativuus on $O(V \log V)$. (Joka taitaa olla sama kuin määrittelydokumentissa mainittu $O(E \log V)$, mutta en tiiä miten tässä tapauksessa sen kaarien määrän saisi solmujen tilalle.)

JPS aikavaativuus: A\* toimii JPS:än pohjana. Vaikka JPS:än tapauksessa solmuja tutkitaan usein vähemmän, on yhden solmun tutkiminen on kalliimpaa. JPS:än erot eivät kuitenkaan vaikuta aikavaativuus analyysiin, joten myös JPS:än aikavaativuus on $O(V \log V)$.

Algoritmien tilavaativuudet: Molempien algoritmien tilavaativuudet ovat $O(V)$, koska jokaista solmua kohti algoritmeissä käytetyissä tietorakenteissa voi olla enintään yksi alkio.

## Suorituskykyvertailu

Ohjelmaa ajettaessa omalla koneella ja oletus kartalla, JPS on noin 2,5 kertaa nopeampi kuin A\*. JPS:än avoimeen joukkoon lisätään noin 19 kertaa vähemmän alkioita ja JPS:än suljettuun joukkoon lisätään noin 14 kertaa vähemmän alkioita.

## Puutteet

Olen aika iloinen itse algoritmien kanssa, mutta muuten sovellukseen voisi vielä tehdä joitain parannuksia:

- Visualisoinnin synkronointi algoritmien suorituskyvyn perusteella. Tällä hetkellä A\* vaikuttaa visualisoinnissa paljon hitaammalta, kuin mitä se oikeasti on.

- Konfiguraatioon muuttuja, joka määritteelee visualisoinnin suoritusajan.

- Yksikkötestien kattavuutta voisi vielä parantaa varsinkin JPS:än kohdalla.

- Visualisoinnin ikkunan koon (eli konfiguraation pixel_scale avaimen) laskeminen dynaamisesti kartan ja näytön koon perusteella.

- Uusia algoritmejä olisi hieman hankala lisätä mm. koska ne täytyy implementoida aika spesifisellä tavalla.

- Integraatio testejä olisi myös hyvä olla vielä hieman lisää. Olisi lisäksi kiva jos integraatio testit saisi lisättyä uudelle algoritmille helpommin.

## Tekoälyn Käyttö

ChatGPT 5.5 Instant mallia on käytetty koodikäytäntö kysymyksissä, testien ideoinnissa, pytestin dokumentaation vaihtoehtona ja joissain pienemmissä implementaatio kysymyksissä (esim. mitä pythonissa kannattaa käyttää suorituskyvyn mittaamiseen).

## Lähteet

[https://harabor.net/data/papers/harabor-grastien-aaai11.pdf](https://harabor.net/data/papers/harabor-grastien-aaai11.pdf)

[https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search/](https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search/)

[https://en.wikipedia.org/wiki/Jump_point_search/](https://en.wikipedia.org/wiki/Jump_point_search/)

[http://en.wikipedia.org/wiki/A\*\_search_algorithm](http://en.wikipedia.org/wiki/A*_search_algorithm)
