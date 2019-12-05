# User storyt

* Rekisteröitymätön käyttäjä voi tarkastella julkisia löytöjä

* Käyttäjä voi luoda oman käyttäjätunnuksen, jotta hän voi pitää kirjaa omista tekemistään villiruoka löydöistään.
	*       SELECT Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Saalis.julkinen, Sijainti.alue, Laji.nimi, Saalis.julkinen "
  
            FROM Saalis
            
            JOIN Account ON Saalis.account_id = account.id
            
            JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
            
            JOIN Laji ON Saalis.laji_id = laji.id
            
            WHERE Saalis.julkinen = TRUE;
* Käyttäjä voi tallentaa löytämiensä villiruokien lajin ja löytöpaikan ja -ajan, määrän ja koordinaatit, jotta hän voi voi myöhemmin tarkastella löytämiään villiruokia ja niihin liitettyjä tietoja. 
* Käyttäjällä on oma näkymä, jossa voi tarkastella omia löytöjään ja järjestää tietoa paikan tai ajankohdan mukaisesti.
* Käyttäjä voi valita tarkasteleeko hän omassa näkymässään julkisia, omia vai julkisia ja omia löytöjään
	* Omat ja julkiset:
  
            SELECT Saalis.account_id, Account.name, Saalis.id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen
            
            FROM Saalis
            
            JOIN Account ON Saalis.account_id = account.id
            
            JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
            
            JOIN Laji ON Saalis.laji_id = laji.id
            
            WHERE Account.id = :id
            
            OR Saalis.julkinen = TRUE ").params(id=user_id);"
            
	* Omat:
  
            SELECT Account.name, Saalis.account_id, Saalis.id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen
  
            FROM Saalis
  
            JOIN Account ON Saalis.account_id = account.id
  
            JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
  
            JOIN Laji ON Saalis.laji_id = laji.id
  
            WHERE Account.id = :id").params(id=user_id);
  
   
  
* Useampi käyttäjä voi merkitä saman löydön, jos käyttäjät ovat tehneet löydön yhdessä. Tällöin löytö näkyy kaikille merkityille käyttäjille.
* Käyttäjä voi määritellä onko hänen tekemänsä löytö näkyvillä vain hänelle itselleen vai julkinen, jolloin se on kaikille näkyvissä. 
* Käyttäjän omassa näkymässä voi tarkastella myös julkisia löytöjä ja järjestää niitä paikan tai ajankohdan mukaisesti.
* Käyttäjä näkee omassa näkymässään yhteenvedon paljon hän on kerännyt sinä vuonna erilaisia löytöjä
* Käyttäjä näkee omassa näkymässään tilaston mitä löytöjä hän on eniten tehnyt

Ekstra:
* Jokaisen käyttäjän aloitusnäkymässä esitetään myös näkymä, joka aikaisempien merkintöjen perusteella ehdottaa, mitä siihen vuodenaikaan kannattaisi mahdollisesti kerätä.
* Käyttäjänäkymässä on myös kartta, josta voi tarkastella löytöjen sijaintia.
