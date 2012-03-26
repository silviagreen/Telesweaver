#!/usr/bin/perl
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
use utf8;
use encoding("iso-8859-1");
use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";

print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Soluzione - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game, recensioni"/>
    <meta name="description" content="recensioni delle avventure testuali con cui si può giocare nel sito" />
    <meta name="author" content="Laura Varagnolo"/>
	<meta name="language" content="italian it"/>
	<link rel="icon" href="../html/css/img/book.png" type="image/x-icon" />
<meta http-equiv="Content-Script-Type" content="text/javascript" /> 
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="screen" /> 
	 <link type="text/css" rel="stylesheet" href="../html/css/mobile.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
  
</head>
<body>
	
        <h1 xml:lang="en"><span></span>TalesWeaver</h1>
   <div id="container"> 
   <div id="path">Ti trovi in: <a href="../cgi-bin/lista.cgi">Soluzioni</a> &gt; Soluzione Storia</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
            <li><a href="../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa</a></li>
	    <li><a href="lista.cgi" tabindex="5">Soluzioni</a></li>
        </ul>
    </div>
<div class="corpo">
EOF

#Quale storia sto usando? Lo vedo dalla Query String
my $buffer=$ENV{'QUERY_STRING'};
my @qstring=split(/=/,$buffer);



#Se il nome della variabile non è ID, qualcuno sta cercando di modificare la query string!
if ($qstring[0] ne 'id') {print<<EOF;
<p class=\"genericError\">ERRORE! ACCESSO NON AUTORIZZATO!</p>
 </div>

    <div id="piede">

   				<img src="../html/css/img/css.gif" alt="CSS Valid!"/>
        			<img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</div>
</body>
</html>
EOF
exit;
}

#Apro il file xml e cerco la storia
my $xp = XML::XPath->new(filename =>  '../xml/soluzioni.xml');
my $radicestoria = $xp->find("//soluzione[storia='$qstring[1]'");
my $esistonostorie = $xp->find("count(//soluzione[storia='$qstring[1]'])");

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
#cerco il titolo di quella storia
my $xp2 = XML::XPath->new(filename =>  '../xml/storie.xml');
my $radicestoria2 = $xp2->find("//storia[\@id='$qstring[1]']");
my $esistonostorie2 = $xp2->find("count(//storia[\@id='$qstring[1]'])");
$titolo=$xp2->find('//storia[@id='.$qstring[1].']/titolo')->string_value;

print<<EOF;
	<h1 id="soluzioniTitle">Soluzione della storia "$titolo"</h1>

<ul id="listaSoluzione">
EOF

foreach my $species ($xp->find("//soluzione[storia='$qstring[1]']/testo")->get_nodelist){
print <<EOF;
	<li>
EOF
	print $species->string_value."</li>";

    print "\n";
}

print <<EOF;
</ul>
<a id="tornaSu" href="#menu">Torna su</a>
EOF

print<<EOF;
</div>

    <div id="piede">

   				<img src="../html/css/img/css.gif" alt="CSS Valid!"/>
        			<img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>

    </div>
</div>
</body>
</html>	
EOF
