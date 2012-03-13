#!/usr/bin/perl
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
my $errore=0;

#Header del file HTML, lo stampo in ogni caso
print<<EOF;
Content-type:text/html\n\n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title xml:lang="en">Home-WordAdventure</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="avventure testuali, storie su cui si puï¿½ giocare e interagire con il testo" />
    <meta name="author" content="Laura Varagnolo"/>
	<meta name="language" content="italian it"/>
     <link type="text/css" rel="stylesheet" href="css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
	 <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>
	<div id="head">
    	<img id="logo" src="" alt=""/>
        <h1 xml:lang="en">Word Adventure</h1>
        <span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span>
    </div>
    <div id="menu">
    	<ul id="menuLista">
        	<li class="mainItem" id="attivo">Home</li>
            <li class="mainItem" id="avventure"><a href="Avventure.html" tabindex="1" accesskey="a">Avventure</a></li>
            <li class="mainItem" id="giocatori"><a href="" tabindex="2" accesskey="g">Giocatori</a></li>
            <li class="mainItem" id="mappa"><a href="" tabindex="3" accesskey="m">Mappa</a></li>
        </ul>
    </div>
    <div id="storia">
EOF

#Quale storia sto usando? Lo vedo dalla Query String
my $buffer=$ENV{'QUERY_STRING'};
my @qstring=split(/=/,$buffer);

#Se il nome della variabile non è ID, qualcuno sta cercando di modificare la query string!
if ($qstring[0] ne 'id') {print<<EOF;
ERRORE! ACCESSO NON AUTORIZZATO!
    </div>

    <div id="piede">

    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>

    </div>
</body>
</html>
EOF
exit;}

#Apro il file xml e cerco la storia
my $xp = XML::XPath->new(filename =>  'codice/xml/storie.xml');
my $radicestoria = $xp->find("//storia[\@id='$qstring[1]']");
my $esistonostorie = $xp->find("count(//storia[\@id='$qstring[1]'])");

#Se non ci sono storie con quell'ID, restituisco errore
if ($esistonostorie==0) {print<<EOF;
ERRORE! STORIA INESISTENTE!
    </div>

    <div id="piede">

    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>

    </div>
</body>
</html>
EOF
exit;
}

#Ho controllato tutto: inizio a prendere le variabili dal POST method
read($STDIN, $buffer, $ENV('CONTENT_LENGTH'));
my @pairs = split (/&/, $buffer);
foreach my $pair (@pairs) {
	(my $name, my $value) = split(/=/, $pair);
	my $value =~ tr/+/ /;
	my $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        my $name =~ tr/+/ /;
        my $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if($name ne "azione" && $name ne "stanza" && $name ne "ultimaazionecorretta"){
		$name=~ tr/^oggetto//;
	}
	my $input{$name} = $value;
		
	}
}
my $numvarpost=@input;
if($numvarpost==0){

	#Siamo all'inizio della storia!
	my $testoiniziale = $radicestoria->find("/incipit/text()");
	print "<p>$testoiniziale</p>";
	my $testostanza = $radicestoria->find("/stanza[\@inizio='true']/testoIniziale/text()");
	print "<p>$testostanza</p>";
}else{

	#Non siamo all'inizio della storia: dobbiamo controllare quale azione è stata eseguita
	my @azione = split(/ /,$input{'azione'});
	
	#L'azione corrisponde ad una direzione? Se sì carico quella stanza
	my @direzioni=("nord","sud","ovest","est","sopra","sotto");
	my $trovato=0;
	foreach my $direzione (@direzione){
		if($trovato==0 && ($azione[0] eq $direzione || ($azione[0] eq 'vai' && ($azione[1] eq $direzione || $azione[2] eq $direzione)))) {
			$trovato=1;
			my $esistedirezione=$radicestoria->find("count(/stanza[\@id='$input['stanza']'/direzioni/nord)");
			if($esistedirezione==0) {
			
				#Non si può andare in questa direzione! Ricarico la stanza precedente
				print "<p>Non puoi andare in questa direzione.</p>";
				my $testostanza=$radicestoria->find("/stanza[\@id='$input['stanza']'/testoIniziale/text()");
				print "<p>$testostanza</p>";
				$errore=1;
			}else{

				#Devo controllare se serve un oggetto o no!
				$servonooggetti=$radicestoria->find("/stanza[\@id='$input['stanza']'/direzioni/$direzione\[\@oggettoNecessario]");
				if($servonooggetti==1){
					print "<p>Ti serve un qualche oggetto per andare in quella direzione.</p>";
					$errore=1;
				}else{
					#Direzione lecita! Carico quella stanza.
					my $idstanza=$radicestoria("/stanza[\@id='$input['stanza']'/direzioni/$direzione/text()");
					my $testostanza=$radicestoria->find("/stanza[\@id='$idstanza'/testoIniziale/text()");
					print "<p>$testostanza</p>";
					my $stanzacorrente=$idstanza;
					my $azionecorrente="";
				}
			}
		}
	}
	if($trovato==0){

		#L'azione non era una direzione! Comincio a cercare tra le azioni disponibili.
		#Prima seleziono i verbi.
		my $nodiazione=$radicestoria->find("/stanza[\@id='$input['stanza']'/azioni[verbo='$azione[0]']");

		#Ora devo ricercare l'oggetto dell'azione, ma prima devo togliere eventuali articoli.
		if($azione[1]eq"il" || $azione[1]eq"lo" || $azione[1]eq"la" || $azione[1]eq"i" || $azione[1]eq"gli" || $azione[1]eq"le" || $azione[1]eq"un" || $azione[1]eq"una" || $azione[1]eq"uno"){
			my $oggettoazione=$azione[2];
			my $contatorearrayazione=2;
		}else{
			my $oggettoazione=$azione[1];
			my $contatorearrayazione=1;
		}
		$oggettoazione= s/"^l\'"//;

		#Cerco se esiste un'azione che abbia quell'oggetto
		my $numnodiazione=$nodiazione->find("count(.[oggetto='$oggettoazione']"));
		if($numnodiazione==0){

			#Non esiste nessuna azione con quel verbo e quell'oggetto
			print "<p>Azione non consentita (o non ho capito l'azione che volevi eseguire!)</p>";
			$errore=1;
		}else{
			$nodiazione=$nodiazione->find(".[oggetto='$oggettoazione']"));

			#Devo verificare se l'azione prevede un secondo oggetto
			my $nodiazionesecoggetto=$nodiazione->find("count(.[secondoOggetto])");
			if(($nodiazionesecoggetto>0 && $#azione==$contatorearrayazione) || ($nodiazionesecoggetto==0 && $#azione>$contatorearrayazione)){

				#Nell'xml c'è un secondo oggetto, ma nella stringa no, oppure nella stringa
				#c'è un secondo oggetto ma nell'xml no: azione rifiutata
				print "<p>Azione non consentita (o non ho capito l'azione che volevi eseguire!)</p>";
				$errore=1;
			}elsif($nodiazionesecoggetto>0 && $#azione>$contatorearrayazione){

				#Sia nell'xml sia nella stringa c'è un secondo oggetto: confrontiamoli
				#Anche qui devo prima togliere gli articoli, e anche le proposizioni.
				$contatorearrayazione=$contatorearrayazione+1;
				my @paroledascartare=("il","lo","la","i","gli","le","di","a","da","in","con","su","per","tra","fra","sopra","sotto");
				my $trovataparola=0;
				foreach $parola (@paroledascartare){
					if($azione["$contatorearrayazione"]==$parola){
						$trovataparola=1;
					}
				}
				if($trovataparola==1){
					$contatorearrayazione=$contatorearrayazione+1;
				}

				#Ora siamo sicuri che $azione[$contatoreazione] contiene il secondo oggetto:
				#Possiamo confrontarli.
				my $secondooggetto=$nodiazione->find("count(.[secondoOggetto])");
				if($secondooggetto==0){

					#Il secondo oggetto è sbagliato. Messaggio di errore.
					print "<p>Azione non consentita (o non ho capito l'azione che volevi eseguire!)</p>";
					$errore=1;
				}
			}
		}
		if($errore==0){

			#L'azione è corretta. Verifico che possa farla!
			my $ebloccata=$nodiazione->find("count(.[bloccataDa])");
			if($ebloccata==1){
				my $azionecheblocca=$nodiazione->find(".[bloccataDa]");
				if($azionecheblocca!=$input{'azioneeseguita'}){

					#Non posso eseguire l'azione! Messaggio di errore.
					print "<p>Azione non consentita (o non ho capito l'azione che volevi eseguire!)";
					$errore=1;
				}
			}
		}
		if($errore==1){

			#C'è stato un errore: ristampo la schermata precedente.
			my $testoazionevecchia=$radicestoria->find("/stanza[\@id=$input{'stanza'}]/azioni[\@id=$input{'ultimaazionecorretta'}]/testoRisposta/text()");
			my $testostanza=$radicestoria->find("/stanza[\@id=$input{'stanza'}]/testoIniziale/text()");
			print "<p>$testostanza</p>\n<p>$testoazionevecchia</p>";
			my $stanzacorrente=$input{'stanza'};
			my $azionecorrente=$input{'ultimaazionecorretta'};
		}else{

			#Nessun errore! Questa azione mi garantiva oggetti?
			my $idazione=$nodiazione->find(".\@id");
			$ottengooggetti=$nodiazione->find("count(./oggettoOttenuto/)");
			if($ottengooggetti==1){
				$oggettoottenuto=$nodiazione->find("./oggettoOttenuto/text()");
				foreach $inputvar (keys $input){
					if($inputvar==$oggettoottenuto){
						$input{"$inputvar"}=1;
					}
				}
			}

			#Stampo i risultati
			my $testoazionenuova=$radicestoria->find("/stanza[\@id=$input{'stanza'}/azioni[\@id='$idazione']/testoRisposta/text()";
			my $testostanza=$radicestoria->find("/stanza[\@id=$input{'stanza'}/testo/text()"
			print "<p>$testostanza</p>\n<p>$testoazionevecchia</p>";
			my$stanzacorrente=$input{'stanza'};
			my$azionecorrente=$idazione;
		}
	}
}
print<<EOF;
<form action="storia.cgi?id=$qstring[1]" method="post">
	<input type="text" name="azione" />
	<input type="hidden" name="stanza" value="$stanza" />
	<input type="hidden" name="ultimaazionecorretta" value="$azionecorrente" />
EOF

#Oggetti: dico alla prossima pagina quali possiedo
my @oggetti=$radicestoria->find("/stanza/azioni/oggettoOttenuto/text()");
foreach $oggetto (@oggetti){
	print "<input type=\"hidden\" name=\"oggetto$oggetto\" value=\"$input{$oggetto}\" />\n";
}
print<<EOF;
	<input type="submit" name="Invia" value="Invia" />
</form>
    </div>
    
    <div id="piede">

    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>
   
    </div>
</body>
</html>
EOF

