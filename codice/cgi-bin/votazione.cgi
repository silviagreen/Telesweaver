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



#controlli sui dati inseriti
$newStarRating="";
 if($star1){
 	$newStarRating="\n<>$star1</>\n";
}
if($star2){
 	$newStarRating="\n<>$star2</>\n";
}
if($star3){
	$newStarRating="\n<>$star3</>\n";
}
if($star4){
	$newStarRating="\n<>$star4</>\n";
}
if($star5){
	$newStarRating="\n<>$star1</>\n";
}
 			

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


my $newStarRatingOk=$parser->parse_balanced_chunk($newStarRating);

 $storie[i]->appendChild($newStarRatingOk);


#serializzazione
open(OUT, ">$fileXml");
print OUT $doc->toString;
close(OUT);

#non stampa nulla xke viene semplicemente visualizzata dal browser all'aggiornamento della pagina
print "Location:readRecensioni.cgi?id=$idStoria\n\n";#redirect

}
exit;


