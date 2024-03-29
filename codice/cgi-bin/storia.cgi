#!/usr/bin/perl
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;

#Header del file HTML, lo stampo in ogni caso
print<<EOF;
Content-type:text/html\n\n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title xml:lang="en">Gioca-TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="avventure testuali, storie su cui si puï¿½ giocare e interagire con il testo" />
    <meta name="author" content="Casartelli Nicolas"/>
	<meta name="language" content="italian it"/>
	<link rel="icon" href="../html/css/img/book.png" type="image/x-icon" />
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="screen" />
 <link type="text/css" rel="stylesheet" href="../html/css/mobile.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
   
</head>
<body>
	 <h1 xml:lang="en"><span id="title"></span>TalesWeaver</h1>
      <!--  <span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span> -->
   <div id="container"> 
   <div id="path">Ti trovi in: <a href="../xml/storie.xml">Avventure</a> &gt; Gioca</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li class="mainItem">
				<a href="../html/Home.html" tabindex="3">Home</a>
					</li>
					<li class="mainItem">
						<a href="../xml/storie.xml" tabindex="4">Avventure</a>
					
					</li>
					<li class="mainItem">
						<a href="../html/manuali.html" tabindex="5">Manuali</a>
					</li>
					<li class="mainItem">
						<a href="../html/mappa.html" tabindex="6">Mappa</a>
					</li>
					<li class="mainItem">
						<a href="../cgi-bin/lista.cgi" tabindex="7">Soluzioni</a>
					</li>
        </ul>
    </div>
<div class="corpo">	
EOF

#Quale storia sto usando? Lo vedo dalla Query String
my $buffer=$ENV{'QUERY_STRING'};
my @qstring=split(/=/,$buffer);

#Se il nome della variabile non è ID, qualcuno sta cercando di modificare la query string!
if ($qstring[0] ne 'id') {
  print<<EOF;
<p class=\"genericError\">ERRORE! ACCESSO NON AUTORIZZATO!</p>
    </div>
</div>
    <div id="piede">
    <img src="../html/css/img/css.gif" alt="CSS Valid!"/>
    <img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</body>
</html>
EOF
 exit;
}

#Apro il file xml e cerco la storia
my $xp = XML::XPath->new(filename =>  '../xml/storie.xml');
my $radicestoria = $xp->find("//storia[\@id='$qstring[1]']");
my $esistonostorie = $xp->find("count(//storia[\@id='$qstring[1]'])");

#Se non ci sono storie con quell'ID, restituisco errore
if ($esistonostorie==0) {
  print<<EOF;
<p class=\"genericError\">ERRORE! STORIA INESISTENTE!</p>
    </div>
</div>
    <div id="piede">

   
    <img src="../html/css/img/css.gif" alt="CSS Valid!"/>
    <img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</body>
</html>
EOF
  exit;
}

#Ho controllato tutto: inizio a prendere le variabili dal POST method
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
my @pairs = split (/&/, $buffer);
foreach my $pair (@pairs) {
  (my $name, my $value) = split(/=/, $pair);
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $name =~ tr/+/ /;
  $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $input{$name} = $value;
}
if($input{'invia'}ne'PROSEGUI'){
	
  #Siamo all'inizio della storia!
  my $testoiniziale = $xp->find("//storia[\@id='$qstring[1]']/incipit/text()");
  print "<p>$testoiniziale</p>";
  my $testostanza = $xp->find("//storia[\@id='$qstring[1]']/stanza[\@inizio='true']/testoIniziale/text()");
  print "<p>$testostanza</p>";
  $stanzacorrente = $xp->find("//storia[\@id='$qstring[1]']/stanza[\@inizio='true']/\@id");

  #Inizializzo valori per gli oggetti
  my $oggetti=$xp->findnodes("//storia[\@id='$qstring[1]']/stanza/azione/oggettoOttenuto");
  foreach my $oggetto ($oggetti->get_nodelist()) {
    $contentoggetto=$oggetto->toString();
    my @array=split(/>/,$contentoggetto);
    @array=split(/</,$array[1]);
    $input{"oggetto$array[0]"}=0;
  }
}else{
	
  #Non siamo all'inizio della storia: dobbiamo controllare quale azione è stata eseguita
  my @azione = split(/ /,$input{'azione'});

  #L'azione corrisponde ad una direzione? Se sì carico quella stanza
  my @direzioni=("nord","sud","ovest","est","sopra","sotto");
  my $trovato=0;
  foreach my $direzione (@direzioni){
    if($trovato==0 && (lc($azione[0]) eq $direzione || (lc($azione[0]) eq 'vai' && (lc($azione[1]) eq $direzione || lc($azione[2]) eq $direzione)))) {
      $trovato=1;
      my $esistedirezione=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/direzioni/direzione[nome=\"$direzione\"])");
      if($esistedirezione==0) {
			
        #Non si può andare in questa direzione! Ricarico la stanza precedente
        print "<p>Non puoi andare in questa direzione.</p>";
        $errore=1;
        $stanzacorrente=$input{'stanza'};
        $azionecorrente=$input{'ultimaazionecorretta'};
      }else{

        #Devo controllare se serve un oggetto o no!
        my $servonooggetti=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/direzioni/direzione[nome=\"$direzione\" and oggettoNecessario])");
        if($servonooggetti!=0){
          my $oggettonecessario=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/direzioni/direzione[nome=\"$direzione\"]/oggettoNecessario");
          if($input{"oggetto$oggettonecessario"}==0){
            my $testoerr=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/direzioni/direzione[nome=\"$direzione\" and oggettoNecessario and testoFallimento])");
              if($testoerr==1) {
                my $testofall=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/direzioni/direzione[nome=\"$direzione\"]/testoFallimento");
                  print "<p>$testofall</p>";
                }else{
                  print "<p>Ti serve un oggetto per andare in questa direzione.</p>";
                }
                $errore=1;
                $stanzacorrente=$input{'stanza'};
                $azionecorrente=$input{'ultimaazionecorretta'};
              }
            }
            if(!defined($errore)){
              #Direzione lecita! Carico quella stanza.
              my $idstanza=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/direzioni/direzione[nome=\"$direzione\"]/stanzaDestinazione/text()");
              my $testostanza=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=\'$idstanza\']/testoIniziale/text()");
              print "<p>$testostanza</p>";
              $stanzacorrente=$idstanza;
              $azionecorrente=$input{'ultimaazionecorretta'};
            }
          }
        }
      }
      if($trovato==0){
        #L'azione non era una direzione! Comincio a cercare tra le azioni disponibili.
        #Ora devo ricercare l'oggetto dell'azione, ma prima devo togliere eventuali articoli.
        if(lc($azione[1])eq"il" || lc($azione[1])eq"lo" || lc($azione[1])eq"la" || lc($azione[1])eq"i" || lc($azione[1])eq"gli" || lc($azione[1])eq"le" || lc($azione[1])eq"un" || lc($azione[1])eq"una" || lc($azione[1])eq"uno" || lc($azione[1])eq"di" || lc($azione[1])eq"a" || lc($azione[1])eq"da" || lc($azione[1])eq"in" || lc($azione[1])eq"con" || lc($azione[1])eq"su" || lc($azione[1])eq"per" || lc($azione[1])eq"tra" || lc($azione[1])eq"fra" || lc($azione[1])eq"sopra" || lc($azione[1])eq"sotto"){
          $oggettoazione=lc($azione[2]);
          $contatorearrayazione=2;
        }else{
          $oggettoazione=lc($azione[1]);
          $contatorearrayazione=1;
        }

        #Cerco se esiste un'azione che abbia quell'oggetto
	$action=lc($azione[0]);

        my $numnodiazione=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[verbo='$action' and oggetto='$oggettoazione'])");
        if($numnodiazione==0){
        #Non esiste nessuna azione con quel verbo e quell'oggetto
          print "<p class=\"genericError\">Azione non consentita (o non ho capito l'azione che volevi eseguire!) </p>";
          $errore=1;
          $stanzacorrente=$input{'stanza'};
        }else{
          $nodiazione=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[verbo='$action' and oggetto='$oggettoazione']");
          #Devo verificare se l'azione prevede un secondo oggetto
          my $nodiazionesecoggetto=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[verbo='$action' and oggetto='$oggettoazione' and secondoOggetto])");
          if(($nodiazionesecoggetto>0 && $#azione==$contatorearrayazione) || ($nodiazionesecoggetto==0 && $#azione>$contatorearrayazione)){

            #Nell'xml c'è un secondo oggetto, ma nella stringa no, oppure nella stringa
            #c'è un secondo oggetto ma nell'xml no: azione rifiutata
            print "<p class=\"genericError\">Azione non consentita (o non ho capito l'azione che volevi eseguire!)</p>";
            $errore=1;
            $stanzacorrente=$input{'stanza'};
          }elsif($nodiazionesecoggetto>0 && $#azione>$contatorearrayazione){

            #Sia nell'xml sia nella stringa c'è un secondo oggetto: confrontiamoli
            #Anche qui devo prima togliere gli articoli, e anche le proposizioni.
            $contatorearrayazione=$contatorearrayazione+1;
            my @paroledascartare=("il","lo","la","i","gli","le","di","a","da","in","con","su","per","tra","fra","sopra","sotto");
            my $trovataparola=0;
            foreach $parola (@paroledascartare){
              if($azione["$contatorearrayazione"] eq $parola){
                $trovataparola=1;
              }
            }
            if($trovataparola==1){
              $contatorearrayazione=$contatorearrayazione+1;
            }

            #Ora siamo sicuri che $azione[$contatoreazione] contiene il secondo oggetto:
            #Possiamo confrontarli.
	    $secondo=lc($azione[$contatorearrayazione]);
            my $secondooggetto=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[verbo='$action' and oggetto='$oggettoazione' and secondoOggetto='$secondo'])");
            if($secondooggetto==0){

              #Il secondo oggetto è sbagliato. Messaggio di errore.
              print "<p class=\"genericError\">Azione non consentita (o non ho capito l'azione che volevi eseguire!)</p>";
              $errore=1;
              $stanzacorrente=$input{'stanza'};
            }else{
              $azioneid=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[verbo='$action' and oggetto='$oggettoazione' and secondoOggetto='$azione[$contatorearrayazione]']/\@id");
            }
          }else{
            $azioneid=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[verbo='$action' and oggetto='$oggettoazione']/\@id");
          }
        }
        if(!defined($errore)){
          #L'azione è corretta. Verifico che possa farla!
          my $ebloccata=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[\@id='$azioneid']/sbloccataDa)");
          if($ebloccata==1){
            my $azionecheblocca=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[\@id='$azioneid']/sbloccataDa");
            if("$azionecheblocca" ne "$input{'ultimaazionecorretta'}"){
              #Non posso eseguire l'azione! Messaggio di errore.
              print "<p class=\"genericError\">Azione non consentita (o non ho capito l'azione che volevi eseguire!) </p>";
              $errore=1;
            }
          }
        }
        if(!defined($errore)){
          #Nessun errore! Questa azione mi garantiva oggetti?
          $ottengooggetti=$xp->find("count(//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[\@id='$azioneid']/oggettoOttenuto)");
          if($ottengooggetti==1){
            $oggettoottenuto=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id='$input{'stanza'}']/azione[\@id='$azioneid']/oggettoOttenuto/text()");
            $oggettoottenuto="oggetto".$oggettoottenuto;
            foreach $inputvar (keys %input){
              if($inputvar eq $oggettoottenuto){
                $input{"$inputvar"}=1;
              }
            }
          }
          #Stampo i risultati
          my $testoazionenuova=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=$input{'stanza'}]/azione[\@id='$azioneid']/testoRisposta");
          my $testostanza=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=$input{'stanza'}]/testoIniziale");
          print "<p>$testostanza</p>\n<p>$testoazionenuova</p>";
          $stanzacorrente=$input{'stanza'};
          $azionecorrente=$azioneid;
        }
      }
    }
    if(defined($errore)){

    #C'è stato un errore: ristampo la schermata precedente.
    my $testoazionevecchia="";
      if($input{'ultimaazionecorretta'} ne "") {
        my $testoazionevecchia=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/azioni[\@id=$input{'ultimaazionecorretta'}]/testoRisposta/text()");
      }
      my $testostanza=$xp->find("//storia[\@id='$qstring[1]']/stanza[\@id=\'$input{'stanza'}\']/testoIniziale/text()");
      print "<p>$testostanza</p>\n<p>$testoazionevecchia</p>";
      my $stanzacorrente=$input{'stanza'};
      my $azionecorrente=$input{'ultimaazionecorretta'};
    }
    print<<EOF;
<form id="gioco" action="storia.cgi?id=$qstring[1]" method="post">
	<fieldset >
	<legend>Agisci</legend>
	<label for="azione">Inserisci azione o direzione</label>
	<input id="azione" type="text" name="azione" tabindex="1"/>
	<input type="hidden" name="stanza" value="$stanzacorrente" />
	<input type="hidden" name="ultimaazionecorretta" value="$azionecorrente" />

EOF

    #Oggetti: dico alla prossima pagina quali possiedo
    my $oggetti=$xp->findnodes("//storia[\@id='$qstring[1]']/stanza/azione/oggettoOttenuto");
    foreach my $oggetto ($oggetti->get_nodelist()) {
      $contentoggetto=$oggetto->toString();
      my @array=split(/>/,$contentoggetto);
      @array=split(/</,$array[1]);
      my $ogg="oggetto$array[0]";
      print "<input type=\"hidden\" name=\"oggetto$array[0]\" value=\"$input{$ogg}\" />\n";
    }

    foreach my $oggetto ($oggetti->get_nodelist()) {
      $contentoggetto=$oggetto->toString();
      my @array=split(/>/,$contentoggetto);
      @array=split(/</,$array[1]);
      $input{"oggetto$array[0]"}=0;
    }

    print<<EOF;
	<input type="submit" name="invia" id="invia" value="PROSEGUI" tabindex="2"/>
	</fieldset>
</form>
    </div>
  </div>  
    <div id="piede">

        <img src="../html/css/img/css.gif" alt="CSS Valid!"/>
    <img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>
   
    </div>
</body>
</html>
EOF

