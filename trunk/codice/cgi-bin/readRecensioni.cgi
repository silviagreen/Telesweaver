#!/usr/bin/perl
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
use utf8;
use encoding("iso-8859-1");
use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";

print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game, recensioni"/>
    <meta name="description" content="recensioni delle avventure testuali con cui si può giocare nel sito" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
<meta http-equiv="Content-Script-Type" content="text/javascript" /> 
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" /> 
	<!-- <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />-->
    <!-- <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" /> -->
 <!--script javascript-->
	<script type="text/javascript" src="../js/validaRecensioni.js"></script>
	<script type="text/javascript" src="../js/svuotaCampi.js"></script>
</head>
<body>
	
        <h1 xml:lang="en"><span></span>TalesWeaver</h1>
   <div id="container"> 
   <div id="path">Ti trovi in: <a href="../xml/storie.xml">Avventure</a> &gt; Recensioni</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
            <li><a href="manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="" tabindex="4">Mappa</a></li>
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

   				<img src="css/img/css.gif" alt="CSS Valid!"/>
        			<img src="css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</div>
</body>
</html>
EOF
exit;
}

#Apro il file xml e cerco la storia
my $xp = XML::XPath->new(filename =>  '../xml/storie.xml');
my $radicestoria = $xp->find("//storia[\@id='$qstring[1]']");
my $esistonostorie = $xp->find("count(//storia[\@id='$qstring[1]'])");

#Se non ci sono storie con quell'ID, restituisco errore
if ($esistonostorie==0) {print<<EOF;
ERRORE! STORIA INESISTENTE!
    </div>
</div>

    <div id="piede">

  				<img src="css/img/css.gif" alt="CSS Valid!"/>
        			<img src="css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</body>
</html>
EOF
exit;
}
$titolo=$xp->find('//storia[@id='.$qstring[1].']/titolo')->string_value;

print<<EOF;
<ul id="menuRec">
<li><a class="indietro" href="../xml/storie.xml" accesskey="t">Torna alle avventure</a></li>
<li><a class="indietro" href="#recensioni" accesskey="r">Recensisci la storia</a></li>
</ul>
<h2>Recensioni - $titolo</h2>

<dl class="storie">
EOF


foreach my $species ($xp->find('//storia[@id='.$qstring[1].']/recensione')->get_nodelist){
    print "<dt>".$species->find('titolo')->string_value ."</dt>";
    print "<dd>" . $species->find('testo')."</dd>";

    print "<dd>Posted: ".$species->find('data') ." By: ".$species->find('utente')."<a class=\"su\" href=\"#menuRec\">Torna su</a></dd>";
    print "\n";
}



print "</dl>";

print<<EOF;
	<form id="votazioni" action="votazione.cgi" method="post">
	<fieldset class="rating">
		<legend>Vota la storia</legend>
		<label for="nomeUtente">Nome giocatore: <span id="errorUtente">Inserisci una stringa alfanumerica</span></label>
		<input name="nomeUtente" id="nomeUtente" value="Nome" maxlenght="30" onclick="svuotaCampi('nomeUtente');" onchange="return controllaTipiRecensione('nomeUtente', 'errorUtente');"/>
	    <input type="radio" id="star5" name="star5" value="5" tabindex="4" /><label for="star5" title="5 stelle">5 stelle</label>
	    <input type="radio" id="star4" name="star4" value="4" tabindex="5" /><label for="star4" title="4 stelle">4 stelle</label>
	    <input type="radio" id="star3" name="star3" value="3" tabindex="6" /><label for="star3" title="3 stelle">3 stelle</label>
	    <input type="radio" id="star2" name="star3" value="2" tabindex="7" /><label for="star2" title="2 stelle">2 stelle</label>
	    <input type="radio" id="star1" name="star1" value="1" tabindex="8" /><label for="star1" title="1 stella">1 stella</label>
        <input name="idStoria" id="idStoria" value="$qstring[1]" type="hidden" />
		<input type="submit" id="submitRating" name="vota" value="Vota" />
	</fieldset>
	</form>

EOF

print<<EOF;
	<form id="recensioni" action="recensioni.cgi" method="post">
    <fieldset id="tuaRecensione">
     	<legend>Lascia la tua recensione</legend>
        <label for="nome">Nome giocatore: <span id="errorNomeGiocatore">Inserisci una stringa alfanumerica</span></label>
        <input name="nomeGiocatore" id="nome" value="Nome" maxlength="30" onclick="svuotaCampi('nome');" onchange="return controllaTipiRecensione('nome', 'errorNomeGiocatore');" tabindex="9"/>
        <label for="titolo">Titolo recensione: <span id="errorTitolo">Inserisci una stringa alfanumerica</span></label>
        <input name="titoloRecensione" id="titolo" value="Titolo" maxlength="50" onclick="svuotaCampi('titolo');" onchange="return controllaTipiRecensione('titolo', 'errorTitolo');" tabindex="10"/>
        <label for="testoRecensione">Testo: <span id="errorTesto">Inserisci caratteri alfanumerici</span></label>
        <textarea rows="10" cols="50" id="testoRecensione" name="testoRecensione" onclick="svuotaCampi('testoRecensione');" onchange="return controllaTipiRecensione('testoRecensione', 'errorTesto');" tabindex="11">Scrivi qui la tua recensione</textarea>
        <input name="idStoria" id="idStoria" value="$qstring[1]" type="hidden" />
        <input type="submit" name="invio" value="Prosegui" tabindex="12"/>
     </fieldset>	
    </form>

</div>
</div>

    <div id="piede">

   				<img src="css/img/css.gif" alt="CSS Valid!"/>
        			<img src="css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</body>
</html>

EOF



