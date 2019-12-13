# User storyt

##  Rekisteröitymätön käyttäjä voi tarkastella julkisia löytöjä
  
  	SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Saalis.julkinen, 		Sijainti.alue, Laji.nimi, Saalis.julkinen
	FROM Saalis
	JOIN Account ON Saalis.account_id = account.id
	JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
	JOIN Laji ON Saalis.laji_id = laji.id
	WHERE Saalis.julkinen = TRUE

## Käyttäjä voi luoda oman käyttäjätunnuksen, jotta hän voi pitää kirjaa ja tarkastella tekemiään villiruoka löytöjä.
	
## Käyttäjä voi tallentaa löytämiensä villiruokien lajin ja löytöpaikan ja -ajan, määrän ja koordinaatit, jotta hän voi voi myöhemmin tarkastella löytämiään villiruokia ja niihin liitettyjä tietoja.

## Käyttäjällä on näkymät, joissa voi tarkastella yhteenvetoja löydöistään paikan tai lajin mukaisesti tilastoituina

	SELECT Laji.nimi, SUM(Saalis.maara) AS maara
        FROM Laji
        LEFT JOIN Saalis ON Laji.id = Saalis.laji_id
        JOIN Account ON Saalis.account_id = account.id
        WHERE Account.id = :id
        GROUP BY Laji.nimi
        ORDER BY maara DESC

## Käyttäjä voi valita tarkasteleeko hän omassa näkymässään julkisia, omia vai hänelle jaettuja löytöjä
  	   
	SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen 
	FROM Saalis
	JOIN Account ON Saalis.account_id = account.id
	JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
	JOIN Laji ON Saalis.laji_id = laji.id
	WHERE Account.id = 	
		
		
         SELECT Saalis.account_id, Account.name, Saalis.id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen
         FROM Saalis
         JOIN Account ON Saalis.account_id = account.id
         JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
         JOIN Laji ON Saalis.laji_id = laji.id
         WHERE Account.id = :id
         OR Saalis.julkinen = TRUE ").params(id=user_id);"
            
	
  	 SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen
         FROM Saalis
         JOIN Account ON Saalis.account_id = account.id
         JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
         JOIN Laji ON Saalis.laji_id = laji.id
         WHERE Account.id = 
         OR Saalis.julkinen = TRUE
   
   
   	 SELECT Account.username, Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Saalis.julkinen, Sijainti.alue, Laji.nimi, Saalis.julkinen
         FROM Shared
         JOIN Saalis ON Shared.jaettu_saalis_id = Saalis.id
         JOIN Account ON Saalis.account_id = Account.id
         JOIN Sijainti ON Saalis.sijainti_id = sijainti.id
         JOIN Laji ON Saalis.laji_id = laji.id
         WHERE kohde_account_id = 
  

## Käyttäjä voi määritellä onko hänen tekemänsä löytö näkyvillä vain hänelle itselleen vai julkinen, jolloin se on kaikille näkyvissä

## Käyttäjä voi jakaa löydyn valituille käyttäjille.


To do:
* Käyttäjä voi tarkastella paikkakohtaisia lajitilastoja ja lajikohtaisia paikkatilastoja
* Käyttäjänäkymässä on myös kartta, josta voi tarkastella löytöjen sijaintia.
* Jokaisen käyttäjän aloitusnäkymässä esitetään myös näkymä, joka aikaisempien merkintöjen perusteella ehdottaa, mitä siihen vuodenaikaan kannattaisi mahdollisesti kerätä.

