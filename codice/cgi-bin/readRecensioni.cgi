
#!/usr/bin/perl
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;

use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";

print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="avventure testuali, storie su cui si può giocare e interagire con il testo" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
     <link type="text/css" rel="stylesheet" href="/public_html/TecnologieWeb/codice/html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
	 <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>
	
        <h1 xml:lang="en"><span>Word Adventure</span></h1>
      <!--  <span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span> -->
   <div id="container">  
    <div id="menu">
    	<ul id="menuLista">
        	<li id="home"><a href="Home.html" tabindex="1" accesskey="h">Home</a></li>
            <li id="attivo"><a href="Avventure.html" tabindex="2" accesskey="a">Avventure</a></li>
            <li id="storia"><a href="" tabindex="3" accesskey="g">Storia</a></li>
	    <li id="recensioni">Recensioni</li>
            <li id="mappa"><a href="" tabindex="4" accesskey="m">Mappa</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF

#Quale storia sto usando? Lo vedo dalla Query String
my $buffer=$ENV{'QUERY_STRING'};
my @qstring=split(/=/,$buffer);



#Se il nome della variabile non è ID, qualcuno sta cercando di modificare la query string!
if ($qstring[0] ne 'id') {print<<EOF;
ERRORE! ACCESSO NON AUTORIZZATO!
    </div>

    <div id="piede">

    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>

    </div>
</div>
</body>
</html>
EOF
exit;}

#Apro il file xml e cerco la storia
my $xp = XML::XPath->new(filename =>  '/var/www/public_html/TecnologieWeb/codice/xml/storie.xml');
my $radicestoria = $xp->find("//storia[\@id='$qstring[1]']");
my $esistonostorie = $xp->find("count(//storia[\@id='$qstring[1]'])");

#Se non ci sono storie con quell'ID, restituisco errore
if ($esistonostorie==0) {print<<EOF;
ERRORE! STORIA INESISTENTE!
    </div>
</div>

    <div id="piede">

    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>

    </div>
</body>
</html>
EOF
exit;
}

print<<EOF;

<h2>Recensioni</h2>
<dl class="storie">
EOF


foreach my $species ($xp->find('//storia[@id='.$qstring[1].']/recensione')->get_nodelist){
    print "<dt>".$species->find('utente')->string_value ."</dt>";
    print "<dd>" . $species->find('testo');
    print "Posted: ".$species->find('data') ."</dd>";
    print "\n";
}

print<<EOF;

</dl>

 <form id="recensioni" action="" method="POST">
    <fieldset id="tuaRecensione">
     	<legend>Lascia la tua recensione</legend>
        <label for="nome">Nome giocatore:</label>
        <input name="nomeGiocatore" id="nome" value="Nome" maxlength="30" />
        <label for="titolo">Titolo recensione:</label>
        <input name="titoloRecensione" id="titolo" value="Titolo" maxlength="50" /></br>
        <label for="testoRecensione">Testo:</label>
        <textarea rows="10" cols="50" id="testoRecensione" name="testoRecensione">
        </textarea>
        <input type="submit" name="invio" value="Prosegui" />
     </fieldset>	
    </form>

</div>
</div>

    <div id="piede">

    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>

    </div>
</body>
</html>

EOF




