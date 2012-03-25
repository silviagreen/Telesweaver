#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);#serve per visualizzare gli errori sul browser
use XML::LibXSLT;
use XML::LibXML;
use XML::XPath;
use utf8;
use encoding("iso-8859-1");

 $query=new CGI();

require 'forPrinting.pl';


$star1=$query->param('star1');
$star2=$query->param('star2');
$star3=$query->param('star3');
$star4=$query->param('star4');
$star5=$query->param('star5');
$idStoria=$query->param('idStoria');
my $error="false";


if(!$star1 && !$star2 && !$star3 && !$star4 && !$star5){
$error="true";	
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
   <div id="path">Ti trovi in: <a href="../xml/storie.xml">Avventure</a> &gt; <a href="readRecensioni.cgi?id=$idStoria">Recensioni</a></div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
            <li><a href="../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa del sito</a></li>
        </ul>
    </div>
<div class="corpo">	
EOF
	print "<p class=\"genericError\" >Inserire una votazione.</p>";
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


