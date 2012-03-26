#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);#serve per visualizzare gli errori sul browser
use XML::LibXSLT;
use XML::LibXML;
use XML::XPath;
#use utf8;
#use encoding("utf-8");
use Time::localtime;
$tm = localtime;
 $query=new CGI();

require 'forPrinting.pl';
	


$nomeGiocatore=$query->param('nomeGiocatore');
$titolo=$query->param('titoloRecensione');
$testo=$query->param('testoRecensione');
$idStoria=$query->param('idStoria');
my $ok='si';
my $stampato='no';



#controlli sui dati inseriti

#if(!$nomeGiocatore && !$titolo && !$testo){
#$stampato='si';
#	$ok='no';
#	print "Content-type: text/html\n\n";
#	&printTop;
#	print "<p>Non hai inserito alcun dato</p>";
#	&printBottom;
#	$stampato='si';
#	$ok='no';
#}

if(!$nomeGiocatore || !$titolo || !$testo){
	$ok='no';

}

if($ok eq'si' && (!$nomeGiocatore=~/\w/ || !$titolo=~/\w/ || !$testo=~/\w/)){
$ok='no';

}
if($ok eq 'si' &&($nomeGiocatore=~ /^[^A-Za-z]+$/ || $titolo=~ /^[^A-Za-z]+$/ || $testo=~/^[^A-Za-z]+$/)){#se non contengono lettere
$ok='no';

}

if($ok eq 'no'){
print "Content-type: text/html\n\n";

print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni-TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="keywords" content="recensioni, avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="recensioni delle avventure testuali contenute nel sito" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
	
<link rel="icon" href="../html/css/img/book.png" type="image/x-icon" />
<meta http-equiv="Content-Script-Type" content="text/javascript" /> 
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
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
            <li><a href=".../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa</a></li>
	     <li><a href="../cgi-bin/lista.cgi" tabindex="5">Soluzioni</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF

#allora devo ristampare la pagina delle recensioni con le form
print $idStoria;
my $xp = XML::XPath->new(filename =>  '../xml/storie.xml');
$titoloStoria=$xp->find('//storia['.$idStoria.']/titolo')->string_value;
print<<EOF;
<ul id="menuRec">
<li><a class="indietro" href="../xml/storie.xml" >Torna alle avventure</a></li>
<li><a class="indietro" href="#recensioni">Recensisci la storia</a></li>
</ul>
<h2>Recensioni - $titoloStoria</h2>

<dl class="storie">
EOF


foreach my $species ($xp->find('//storia[@id='.$idStoria.']/recensione')->get_nodelist){
my $testo=$species->find('testo');
	utf8::encode($testo);
    print "<dt>".$species->find('titolo')->string_value ."</dt>";
    print "<dd>" . $testo."</dd>";

    print "<dd>Posted: ".$species->find('data') ." By: ".$species->find('utente')."<a class=\"su\" href=\"#menuRec\">Torna su</a></dd>";
    print "\n";
}

print "</dl>";

#aggiunte per prelevare le recensioni da database
print <<EOF;
<h2>Valutazioni - $titoloStoria</h2>
<dl class="valutazioni">

</dl>
EOF
#fine aggiunte database



my $numVoti=int($xp->find("count(//storia[\@id='$idStoria']/valutazione)"));

#in teoria conta gli elementi
my $sommaVoti;
foreach my $val ($xp->find('//storia[@id='.$idStoria.']/valutazione')->get_nodelist){
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
        <input name="idStory" id="idStory" value="$idStoria" type="hidden" />
		<input type="submit" id="submitRating" name="vota" value="Vota" />
	</fieldset>
	</form>

EOF

print<<EOF;
	<form id="recensioni" action="recensioni.cgi" method="post">
    <fieldset id="tuaRecensione">
     	<legend>Lascia la tua recensione</legend>
        <label for="nome">Nome giocatore: 

EOF

if(!$nomeGiocatore){
print<<EOF;
	<span class="genericError">Il campo Giocatore deve essere compilato con il tuo nome!</span>
EOF
}
#se il nome del giocatore non contiene nemmeno una lettera
if($nomeGiocatore=~ /^[^A-Za-z]+$/ || !$nomeGiocatore=~/\w/){
print<<EOF;
	<span class="genericError">Devi inserire una stringa alfanumerica. Sono obbligatorie delle lettere.</span>
EOF
}
print<<EOF;
	</label>
        <input name="nomeGiocatore" id="nome" value="Nome" maxlength="30" onclick="svuotaCampi('nome');" onchange="return controllaTipiRecensione('nome', 'errorNomeGiocatore');" tabindex="9"/><span id="errorNomeGiocatore">Il nome del giocatore deve essere alfanumerico.</span>
        <label for="titolo">Giudizio generale: 
EOF

if(!$titolo){
print<<EOF

<span class="genericError">Il campo Titolo deve essere compilato!</span>

EOF
}

if($titolo=~ /^[^A-Za-z]+$/ || !$titolo=~/\w/){
print<<EOF;

<span class="genericError">Il campo Titolo deve contenere una stringa alfanumerica. Sono obbligatorie delle lettere.</span>

EOF
}
print<<EOF;
	</label>
        <input name="titoloRecensione" id="titolo" value="Titolo" maxlength="50" onclick="svuotaCampi('titolo');" onchange="return controllaTipiRecensione('titolo', 'errorTitolo');" tabindex="10"/><span id="errorTitolo">Il titolo deve essere alfanumerico.</span>
        <label for="testoRecensione">Testo: 
EOF

if(!$testo){
print<<EOF;
	<span class="genericError">Devi inserire un testo per la recensione! il testo dev'essere di tipo alfanumerico.</span>
EOF
}

if($testo=~ /^[^A-Za-z]+$/ || !$testo=~/\w/){
print<<EOF;
	<span class="genericError">Il campo Testo deve contenere caratteri alfanumerici. Sono obbligatorie delle lettere.</span>
EOF
}

print<<EOF;
</label>
        <textarea rows="10" cols="50" id="testoRecensione" name="testoRecensione" onclick="svuotaCampi('testoRecensione');" onchange="return 		controllaTipiRecensione('testoRecensione', 'errorTesto');" tabindex="11">Scrivi qui la tua recensione</textarea>
        <input name="idStoria" id="idStoria" value="$idStoria" type="hidden" /><span id="errorTesto">Il testo deve essere alfanumerico.</span>
        <input type="submit" name="invio" value="Prosegui" tabindex="12"/>
     </fieldset>	
    </form>

EOF
&printBottom;
}


#ok, tutti i dati sono a posto
if($ok eq 'si'){
$newNomeGiocatore="";
if($nomeGiocatore){
	 $newNomeGiocatore="\n<utente>$nomeGiocatore</utente>\n";
}

$newTitolo="";
if($titolo){
	utf8::decode($titolo);
	 $newTitolo="\n<titolo>$titolo</titolo>\n";
}
$newTesto="";
if($testo){
	 $newTesto="\n<testo>$testo</testo>\n";
}

my $month="";
if(length(($tm->mon)+1) eq 1){
 $month="0".(($tm->mon)+1);}
else {
 $month=(($tm->mon)+1);
}

my $date=($tm->year+1900)."-".$month."-".($tm->mday);
my $newRensione= "\n<recensione>".$newTitolo.$newTesto.$newNomeGiocatore."<data>".$date."</data>\n</recensione>\n";#frammento da inserire nell'xml

#print "Content-type: text/html\n\n";
	#print $newRensione;

#inserimento nel file xml dei nuovi dati

 #$xp = XML::XPath->new(filename =>  '../xml/storie.xml');
 #$radiceStoria = $xp->find("//storia[\@id='$idStoria']");
my $fileXml='../xml/storie.xml';
my $parser=XML::LibXML->new();



my $doc=$parser->parse_file($fileXml);
my $radice=$doc->getDocumentElement;
my @storie=$radice->getElementsByTagName('storia');


my $newRensioneOk=$parser->parse_balanced_chunk($newRensione);
my $k=idStoria-1;
 $storie[i+$k]->appendChild($newRensioneOk);


#serializzazione
open(OUT, ">$fileXml");
print OUT $doc->toString;
close(OUT);




print "Location:readRecensioni.cgi?id=$idStoria\n\n";

}
exit;


