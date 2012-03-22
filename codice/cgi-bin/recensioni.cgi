#!/usr/bin/perl
use XML::LibXSLT;
use XML::LibXML;
use CGI;
use CGI::Carp qw(fatalsToBrowser);#serve per visualizzare gli errori sul browser

my $query=new CGI();

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
my $newNomeGiocatore="";
if($nomeGiocatore){
	my $newNomeGiocatore="\n<utente>$nomeGiocatore</utente>\n";
}
my $newTitolo="";
if($titolo){
	my $newTitolo="\n<titolo>$titolo</titolo>";
}
my $newTesto="";
if($testo){
	my $newTesto="\n<testo>$testo</testo>";
}

my $newRensione=my $newNomeGiocatore.my $newTitolo.my $newTesto;#frammento da inserire nell'xml


#inserimento nel file xml dei nuovi dati
my $fileXml='../xml/storie.xml';
my $parser=XML::LibXML->new();
my $doc=$parser->parse_file($fileXml);
my $radice=$doc->getDocumentElement;
my @recensioni=$radice->getElementsByTagName('recensione');

my $newRensioneOk=$parser->parse_balanced_chunk(my $newRensione);

for($i=0; $i<scalar(@recensioni); $i++){
	my $recensioni[$i]->appendChild(my $newRensioneOk); #DOVE CAVOLO STA L PROBLEMAAAA!?!?!?!
}

#serializzazione
#open(OUT, ">$fileXml");
print OUT $doc->toString;
#close OUT;

#my $url="readRecensioni.cgi";
#print "Location:$url\n\n";
#exit;


