
## Tietokantakaavio
![tietokantakaavio](https://github.com/tumajote/Villiruokasovellus/blob/master/documentation/Tietokantakaavio.png)

## Create Table 
    CREATE TABLE account (
      id INTEGER NOT NULL, 
      date_created DATETIME,
      date_modified DATETIME,
      name VARCHAR(144) NOT NULL,
      username VARCHAR(144) NOT NULL,
      password VARCHAR(144) NOT NULL,
      PRIMARY KEY (id));

    CREATE TABLE sijainti (
	    id INTEGER NOT NULL, 
	    alue VARCHAR(20) NOT NULL, 
	    PRIMARY KEY (id));
    
    CREATE TABLE laji (
	    id INTEGER NOT NULL, 
	    nimi VARCHAR(20) NOT NULL, 
	    PRIMARY KEY (id));
    
    CREATE TABLE saalis (
	    id INTEGER NOT NULL, 
	    paivamaara DATETIME, 
	    maara INTEGER NOT NULL, 
	    koordinaatit VARCHAR(100) NOT NULL, 
	    julkinen BOOLEAN NOT NULL, 
	    account_id INTEGER NOT NULL, 
	    sijainti_id INTEGER NOT NULL, 
	    laji_id INTEGER NOT NULL, 
	    PRIMARY KEY (id), 
	    CHECK (julkinen IN (0, 1)), 
	    FOREIGN KEY(account_id) REFERENCES account (id), 
	    FOREIGN KEY(sijainti_id) REFERENCES sijainti (id), 
	    FOREIGN KEY(laji_id) REFERENCES laji (id));
