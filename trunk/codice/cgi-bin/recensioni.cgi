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


	

$nomeGiocatore=$query->param('nome');
$titolo=$query->param('titolo');
$testo=$query->param('testoRecensione');
$idStoria=$query->param('idStoria');
$ok='si';
$stampato='no';


#controlli sui dati inseriti

if(!$nomeGiocatore && !$titolo && !$testo){
	print "Content-type: text/html\n\n";
	print "Non hai inserito alcun dato";
	$stampato='si';
	$ok='no';
}

if($ok && (!$nomeGiocatore || !$testo || !$titolo)){

	if($stampato eq 'no'){	
	print "Content-type: text/html\n\n";
	$stampato='si';
}
	
	print "Mancano alcuni dati";
	$ok='no';
}

if($ok && !$nomeGiocatore){
	print "Nome giocatore mancante";
	$ok='no';
}
if($ok && !$titolo){
	print "Titolo mancante";
}
if($ok && !$testo){
	print "Testo mancante";
	$ok='no';
}
if($ok && (!$nomeGiocatore=~/\w/ && !$titolo=~/\w/ && !$testo=~/\w/)){
	print "Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche";
	$ok='no';
}
if($ok &&(!$nomeGiocatore=~/\w/ || !$titolo=~/\w/ || !$testo=~/\w/)){
	print "Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche";
	$ok='no';
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
$month="0".(($tm->mon)+1);}
else {
$month=(($tm->mon)+1);
}

$date=($tm->year+1900)."-".$month."-".($tm->mday);
$newRensione= "\n<recensione>".$newTitolo.$newTesto.$newNomeGiocatore."<data>".$date."</data>\n</recensione>\n";#frammento da inserire nell'xml

#print "Content-type: text/html\n\n";
	#print $newRensione;

#inserimento nel file xml dei nuovi dati

 #$xp = XML::XPath->new(filename =>  '../xml/storie.xml');
 #$radiceStoria = $xp->find("//storia[\@id='$idStoria']");
 $fileXml='../xml/storie.xml';
 $parser=XML::LibXML->new();



 $doc=$parser->parse_file($fileXml);
 $radice=$doc->getDocumentElement;
 @storie=$radice->getElementsByTagName('storia');


$newRensioneOk=$parser->parse_balanced_chunk($newRensione);

 $storie[i]->appendChild($newRensioneOk);


#serializzazione
open(OUT, ">$fileXml");
print OUT $doc->toString;
close(OUT);




print "Location:readRecensioni.cgi?id=$idStoria\n\n";

}
exit;


