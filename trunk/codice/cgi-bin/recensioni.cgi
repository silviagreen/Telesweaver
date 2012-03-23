#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);#serve per visualizzare gli errori sul browser
#use XML::LibXSLT;
#use XML::LibXML;

 $query=new CGI();

$nomeGiocatore=$query->param('nome');
$titolo=$query->param('titolo');
$testo=$query->param('testoRecensione');

print "Content-type: text/html\n\n";

#controlli sui dati inseriti
if(!$nomeGiocatore && !$titolo && !$testo){
	print "Non hai inserito alcun dato";
}
if(!$nomeGiocatore && !$titolo || !$nomeGiocatore && !$testo || !$titolo && !$testo ){
	print "Mancano alcuni dati";
}
if(!$nomeGiocatore){
	print "Nome giocatore mancante";
}
if(!$titolo){
	print "Titolo mancante";
}
if(!$testo){
	print "Testo mancante";
}
if(!$nomeGiocatore=~/\w/ && !$titolo=~/\w/ && !$testo=~/\w/){
	print "Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche";
}
if(!$nomeGiocatore=~/\w/ || !$titolo=~/\w/ || !$testo=~/\w/){
	print "Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche";
}

#ok, tutti i dati sono a posto
$newNomeGiocatore="";
if($nomeGiocatore){
	 $newNomeGiocatore="\n<utente>$nomeGiocatore</utente>\n";
}
$newTitolo="";
if($titolo){
	 $newTitolo="\n<titolo>$titolo</titolo>";
}
$newTesto="";
if($testo){
	 $newTesto="\n<testo>$testo</testo>";
}

$newRensione= $newNomeGiocatore.$newTitolo.$newTesto;#frammento da inserire nell'xml


#inserimento nel file xml dei nuovi dati
 $fileXml='../xml/storie.xml';
 $parser=XML::LibXML->new();
 $doc=$parser->parse_file($fileXml);
 $radice=$doc->getDocumentElement;
 @recensioni=$radice->getElementsByTagName('recensione');

$newRensioneOk=$parser->parse_balanced_chunk($newRensione);

for($i=0; $i<scalar(@recensioni); $i++){
	 $recensioni[$i]->appendChild($newRensioneOk); #DOVE CAVOLO STA L PROBLEMAAAA!?!?!?!
}

#serializzazione
#open(OUT, ">$fileXml");
print OUT $doc->toString;
#close OUT;

# $url="readRecensioni.cgi";
#print "Location:$url\n\n";
#exit;


