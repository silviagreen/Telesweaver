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
	

$nomeGiocatore=$query->param('nome');
$titolo=$query->param('titolo');
$testo=$query->param('testoRecensione');
$idStoria=$query->param('idStoria');
my $ok='si';
my $stampato='no';
print "Content-type: text/html\n\n";

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

#if($ok && (!$nomeGiocatore || !$testo || !$titolo)){

#	if($stampato eq 'no'){	
#	print "Content-type: text/html\n\n";
#	$stampato='si';
#}
	
#	print "Mancano alcuni dati";
#	$ok='no';
#}

if($ok eq 'si' && !$nomeGiocatore){
	$ok='no';
#print "Content-type: text/html\n\n";
	&printTop;
	print "<class=\"error\" p>Nome giocatore mancante</p>";
	&printBottom;
}
if($ok eq 'si' && !$titolo){
#print "Content-type: text/html\n\n";
	&printTop;
	print "<class=\"error\" p>Titolo mancante</p>";
}
if($ok eq 'si' && !$testo){
#print "Content-type: text/html\n\n";
	&printTop;
	print "<class=\"error\" p>Testo mancante</p>";
	&printBottom;
	$ok='no';
}
if($ok eq'si' && (!$nomeGiocatore=~/\w/ && !$titolo=~/\w/ && !$testo=~/\w/)){$ok='no';
#print "Content-type: text/html\n\n";
	&printTop;
	print "<class=\"error\" p>Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche</p>";
&printBottom;
	
}
if($ok eq 'si' &&(!$nomeGiocatore=~/\w/ || !$titolo=~/\w/ || !$testo=~/\w/)){$ok='no';
#print "Content-type: text/html\n\n";
	&printTop;
	print "<class=\"error\" p>Formato dei campi non corretto, devono essere tutti stringhe alfanumeriche</p>";
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


