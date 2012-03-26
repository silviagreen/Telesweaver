#!/usr/bin/perl -w
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
#use utf8;
#use encoding("iso-8859-1");
use CGI::Carp qw(fatalsToBrowser);
use strict;
use warnings;

print "Content-type: text/html\n\n";
#print "Content-Encoding: utf8\n\n";

print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game, recensioni"/>
    <meta name="description" content="recensioni delle avventure testuali con cui si può giocare nel sito" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
	<link rel="icon" href="../html/css/img/book.png" type="image/x-icon" />
<meta http-equiv="Content-Script-Type" content="text/javascript" /> 
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="screen" /> 
	 <link type="text/css" rel="stylesheet" href="../html/css/mobile.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
   
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
            <li><a href="../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa</a></li>
	    <li><a href="../cgi-bin/lista.cgi" tabindex="5">Soluzioni</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF

#Quale storia sto usando? Lo vedo dalla Query String
my $buffer=$ENV{'QUERY_STRING'};
my @qstring=split(/=/,$buffer);



#Se il nome della variabile non è ID, qualcuno sta cercando di modificare la query string!
if ($qstring[0] ne 'id') {print<<EOF;
<p class=\"genericError\">ERRORE! ACCESSO NON AUTORIZZATO!</p>
 </div>

    <div id="piede">

   				<img src="../html/css/img/css.gif" alt="CSS Valid!"/>
        			<img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

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
<p class=\"genericError\">ERRORE! STORIA INESISTENTE!</p>
    </div>
</div>

    <div id="piede">

  				<img src="../html/css/img/css.gif" alt="CSS Valid!"/>
        			<img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</body>
</html>
EOF
exit;
}
my $titolo=$xp->find('//storia[@id='.$qstring[1].']/titolo')->string_value;

print<<EOF;
<ul id="menuRec">
<li><a class="indietro" href="../xml/storie.xml">Torna alle avventure</a></li>
<li><a class="indietro" href="#recensioni">Recensisci la storia</a></li>
</ul>
<h2>Recensioni - $titolo</h2>

<dl class="storie">
EOF


foreach my $species ($xp->find('//storia[@id='.$qstring[1].']/recensione')->get_nodelist){
	my $testo=$species->find('testo');
	utf8::encode($testo);
    print "<dt>".$species->find('titolo')->string_value ."</dt>";
    print "<dd>" .$testo."</dd>";

    print "<dd>Posted: ".$species->find('data') ." By: ".$species->find('utente')."<a class=\"su\" href=\"#menuRec\">Torna su</a></dd>";
    print "\n";
}

print "</dl>";




my $numVoti=int($xp->find("count(//storia[\@id='$qstring[1]']/valutazione)"));

#in teoria conta gli elementi
my $sommaVoti;
foreach my $val ($xp->find('//storia[@id='.$qstring[1].']/valutazione')->get_nodelist){
	$sommaVoti+=int($val->find('numero'));
}
#print "somma: ".$sommaVoti." num: ".$numVoti;class="on"
my $mediaVoti=($sommaVoti/$numVoti);


if($mediaVoti < 1 && $mediaVoti > 0){
print<<EOF;
<div class="rating">
La media delle valutazioni degli utenti per questa storia &egrave;: 
<span >★</span><span>☆</span><span>☆</span><span>☆</span><span>☆</span>
</div>​

EOF
}  if($mediaVoti < 2 && $mediaVoti > 1){
print<<EOF;
<div class="rating">
La media delle valutazioni degli utenti per questa storia &egrave;: 
<span >★</span><span>★</span><span>☆</span><span>☆</span><span>☆</span>
</div>​

EOF

}
 if($mediaVoti < 3 && $mediaVoti > 2){
print<<EOF;
<div class="rating">
La media delle valutazioni degli utenti per questa storia &egrave;: 
<span >★</span><span>★</span><span>★</span><span>☆</span><span>☆</span>
</div>​
EOF

}
 if($mediaVoti < 4 && $mediaVoti > 3){
print<<EOF;
<div class="rating">
La media delle valutazioni degli utenti per questa storia &egrave;: 
<span >★</span><span>★</span><span>★</span><span>★</span><span>☆</span>
</div>​

EOF

}
 if($mediaVoti < 5 && $mediaVoti > 4){
print<<EOF;
<div class="rating">
La media delle valutazioni degli utenti per questa storia &egrave;: 
<span >★</span><span>★</span><span>★</span><span>★</span><span>★</span>
</div>​

EOF

}

print <<EOF;

	<form id="votazioni" action="votazione.cgi" method="post">
	<fieldset class="rating">
		<legend>Vota la storia</legend>
	    <input type="radio" id="star5" name="star5" value="5" tabindex="4" /><label for="star5" title="5 stelle">5 stelle</label>
	    <input type="radio" id="star4" name="star4" value="4" tabindex="5" /><label for="star4" title="4 stelle">4 stelle</label>
	    <input type="radio" id="star3" name="star3" value="3" tabindex="6" /><label for="star3" title="3 stelle">3 stelle</label>
	    <input type="radio" id="star2" name="star3" value="2" tabindex="7" /><label for="star2" title="2 stelle">2 stelle</label>
	    <input type="radio" id="star1" name="star1" value="1" tabindex="8" /><label for="star1" title="1 stella">1 stella</label>
        <input name="idStory" id="idStory" value="$qstring[1]" type="hidden" />
		<input type="submit" id="submitRating" name="vota" value="Vota" />
	</fieldset>
		
	</form>

EOF

print<<EOF;
	<form id="recensioni" action="recensioni.cgi" method="post">
    <fieldset id="tuaRecensione">
     	<legend>Lascia la tua recensione</legend>
        <label for="nome">Nome giocatore:</label>
        <input name="nomeGiocatore" id="nome" value="Nome" maxlength="30" onclick="svuotaCampi('nome');" onchange="return controllaTipiRecensione('nome', 'errorNomeGiocatore');" tabindex="9"/>
        <label for="titolo">Titolo recensione:</label>
        <input name="titoloRecensione" id="titolo" value="Titolo" maxlength="50" onclick="svuotaCampi('titolo');" onchange="return controllaTipiRecensione('titolo', 'errorTitolo');" tabindex="10"/>
        <label for="testoRecensione">Testo:</label>
        <textarea rows="10" cols="50" id="testoRecensione" name="testoRecensione" onclick="svuotaCampi('testoRecensione');" onchange="return controllaTipiRecensione('testoRecensione', 'errorTesto');" tabindex="11">Scrivi qui la tua recensione</textarea>
        <input name="idStoria" id="idStoria" value="$qstring[1]" type="hidden" />
        <input type="submit" name="invio" value="Prosegui" tabindex="12"/>
     </fieldset>	
    </form>

</div>
</div>

    <div id="piede">
		<img src="../html/css/img/css.gif" alt="CSS Valid!"/>
        			<img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>

</body>
</html>

EOF



