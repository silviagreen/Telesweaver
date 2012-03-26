#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);#serve per visualizzare gli errori sul browser
use XML::LibXSLT;
use XML::LibXML;
use XML::XPath;
#use utf8;
#use encoding("iso-8859-1");

 $query=new CGI();

require 'forPrinting.pl';


$star1=$query->param('star1');
$star2=$query->param('star2');
$star3=$query->param('star3');
$star4=$query->param('star4');
$star5=$query->param('star5');
$idStoria=$query->param('idStory');
my $error="false";


if(!$star1 && !$star2 && !$star3 && !$star4 && !$star5){
$error="true";	
print "Content-type: text/html\n\n";
print<<EOF;
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
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
	 <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
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
my $xp = XML::XPath->new(filename =>  '../xml/storie.xml');
$titoloStoria=$xp->find('//storia['.$idStoria.']/titolo')->string_value;
print<<EOF;
<ul id="menuRec">
<li><a class="indietro" href="../xml/storie.xml" accesskey="t">Torna alle avventure</a></li>
<li><a class="indietro" href="#recensioni" accesskey="r">Recensisci la storia</a></li>
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

my $numVoti=$xp->find("count(//storia[\@id='$idStoria']/valutazione)");
#in teoria conta gli elementi
my $sommaVoti;
foreach my $val ($xp->find('//storia[@id='.$idStoria.']/valutazione')->get_nodelist){
	$sommaVoti+=int($val->find('numero'));
}
#my $mediaVoti=$sommaVoti/$numVoti;

print<<EOF;

<p>La media delle valutazioni degli utenti per questa storia &egrave: </p>
EOF
print "$mediaVoti";

print <<EOF;

	<form id="votazioni" action="votazione.cgi" method="post">
	<span class="genericError">Devi inserire una votazione. Per votare clicca sulla stella. 1 &egrave il voto minimo, 5 il massimo.</span>
	<fieldset class="rating">
		<legend>Vota la storia</legend>
	    <input type="radio" id="star5" name="star5" value="5" tabindex="4" /><label for="star5" title="5 stelle">5 stelle</label>
	    <input type="radio" id="star4" name="star4" value="4" tabindex="5" /><label for="star4" title="4 stelle">4 stelle</label>
	    <input type="radio" id="star3" name="star3" value="3" tabindex="6" /><label for="star3" title="3 stelle">3 stelle</label>
	    <input type="radio" id="star2" name="star3" value="2" tabindex="7" /><label for="star2" title="2 stelle">2 stelle</label>
	    <input type="radio" id="star1" name="star1" value="1" tabindex="8" /><label for="star1" title="1 stella">1 stella</label>
        <input name="idStoria" id="idStoria" value="$idStoria" type="hidden" />
		<input type="submit" id="submitRating" name="vota" value="Vota" />
	</fieldset>
	</form>

EOF

print<<EOF;
	<form id="recensioni" action="recensioni.cgi" method="post">
    <fieldset id="tuaRecensione">
     	<legend>Lascia la tua recensione</legend>
        <label for="nome">Nome giocatore: 
	</label>
        <input name="nomeGiocatore" id="nome" value="Nome" maxlength="30" onclick="svuotaCampi('nome');" onchange="return controllaTipiRecensione('nome', 'errorNomeGiocatore');" tabindex="9"/>
        <label for="titolo">Titolo recensione: 
	</label>
        <input name="titoloRecensione" id="titolo" value="Titolo" maxlength="50" onclick="svuotaCampi('titolo');" onchange="return controllaTipiRecensione('titolo', 'errorTitolo');" tabindex="10"/>
        <label for="testoRecensione">Testo: 
</label>
        <textarea rows="10" cols="50" id="testoRecensione" name="testoRecensione" onclick="svuotaCampi('testoRecensione');" onchange="return 		controllaTipiRecensione('testoRecensione', 'errorTesto');" tabindex="11">Scrivi qui la tua recensione</textarea>
        <input name="idStoria" id="idStoria" value="$idStoria" type="hidden" />
        <input type="submit" name="invio" value="Prosegui" tabindex="12"/>
     </fieldset>	
    </form>

EOF
&printBottom;
}


if($error eq "false"){
$newStarRating="";
 if($star1){
 	$newStarRating="\n<numero>".$star1."</numero>\n";
}
if($star2){
 	$newStarRating="\n<numero>".$star2."</numero>\n";
}
if($star3){
	$newStarRating="\n<numero>".$star3."</numero>\n";
}
if($star4){
	$newStarRating="\n<numero>".$star4."</numero>\n";
}
if($star5){
	$newStarRating="\n<numero>".$star1."</numero>\n";
}
 			
$newUserStarRating="\n<valutazione>".$newStarRating."</valutazione>\n";

#ok, tutti i dati sono a posto

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


my $newStarRatingOk=$parser->parse_balanced_chunk($newUserStarRating);

 $storie[i]->appendChild($newStarRatingOk);


#serializzazione
open(OUT, ">$fileXml");
print OUT $doc->toString;
close(OUT);

#non stampa nulla xke viene semplicemente visualizzata dal browser all'aggiornamento della pagina
print "Location:readRecensioni.cgi?id=$idStoria\n\n";#redirect

}

exit;


