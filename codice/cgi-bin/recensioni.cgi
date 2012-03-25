#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);#serve per visualizzare gli errori sul browser
use XML::LibXSLT;
use XML::LibXML;
use XML::XPath;
use utf8;
use encoding("iso-8859-1");
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

if($ok && (!$nomeGiocatore || !$testo || !$titolo)){

#	if($stampato eq 'no'){	
#	print "Content-type: text/html\n\n";
#	$stampato='si';
#}
	
#	print "Mancano alcuni dati";
#	$ok='no';
print "Content-type: text/html\n\n";
print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="recensioni, avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="recensioni delle avventure testuali contenute nel sito" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
	 <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>
	
        <h1 xml:lang="en"><span></span>TalesWeaver</h1>
      <!--  <span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span> -->
   <div id="container"> 
   <div id="path">Ti trovi in: <a href="../xml/storie.xml">Avventure</a> &gt; Recensioni</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
            <li><a href=".../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa del sito</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF

$ok='no';
if(!$nomeGiocatore){
	
#print "Content-type: text/html\n\n";
	
	print "<p id=\"errorTitoloo\" >Nome giocatore mancante</p>";
	
}
if(!$titolo){
#print "Content-type: text/html\n\n";
	
	print "<p id=\"errorTitoloo\" >Titolo mancante</p>";
}
if(!$testo){
#print "Content-type: text/html\n\n";
	
	print "<p id=\"errorTitoloo\" >Testo mancante</p>";
	
	
}
&printBottom;
}
if($ok eq'si' && (!$nomeGiocatore=~/\w/ || !$titolo=~/\w/ || !$testo=~/\w/)){$ok='no';
print "Content-type: text/html\n\n";
	print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="recensioni, avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="recensioni delle avventure testuali contenute nel sito" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
	 <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>
	
        <h1 xml:lang="en"><span></span>TalesWeaver</h1>
      <!--  <span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span> -->
   <div id="container"> 
   <div id="path">Ti trovi in: <a href="../xml/storie.xml">Avventure</a> &gt; Recensioni</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
<li><a href=".../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa del sito</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF
	print "<p id=\"errorTitoloo\" >Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche</p>";
&printBottom;
	
}
if($ok eq 'si' &&($nomeGiocatore=~ /^[^A-Za-z]+$/ || $titolo=~ /^[^A-Za-z]+$/ || $testo=~/^[^A-Za-z]+$/)){#se non contengono lettere
$ok='no';
print "Content-type: text/html\n\n";
		print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Recensioni - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="recensioni, avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="recensioni delle avventure testuali contenute nel sito" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
	 <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>
	
        <h1 xml:lang="en"><span></span>TalesWeaver</h1>
      <!--  <span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span> -->
   <div id="container"> 
   <div id="path">Ti trovi in: <a href="../xml/storie.xml">Avventure</a> &gt; Recensioni</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
<li><a href=".../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa del sito</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF
	print "<p id=\"errorTitoloo\">Formato1 dei campi non corretto, devono essere tutti stringhe alfanumeriche</p>";
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
	 $newTitolo="\n<titolo>$titolo</titolo>\n";
}
$newTesto="";
if($testo){
	 $newTesto="\n<testo>$testo</testo>\n";
}

if(length(($tm->mon)+1) == 1){
my $month="0".(($tm->mon)+1);}
else {
my $month=(($tm->mon)+1);
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

 $storie[i]->appendChild($newRensioneOk);


#serializzazione
open(OUT, ">$fileXml");
print OUT $doc->toString;
close(OUT);




print "Location:readRecensioni.cgi?id=$idStoria\n\n";

}
exit;


