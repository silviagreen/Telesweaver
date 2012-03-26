#!/usr/bin/perl
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
use utf8;
use encoding("iso-8859-1");
use CGI::Carp qw(fatalsToBrowser);

#Apro il file xml e cerco le storie
my $xp = XML::XPath->new(filename =>  '../xml/storie.xml');
my $radicestoria = $xp->find("//storia");
my $esistonostorie = $xp->find("count(//storia)");

print "Content-type: text/html\n\n";

print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Soluzioni - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game, recensioni"/>
    <meta name="description" content="recensioni delle avventure testuali con cui si può giocare nel sito" />
    <meta name="author" content="Laura Varagnolo"/>
	<meta name="language" content="italian it"/>
	
<meta http-equiv="Content-Script-Type" content="text/javascript" /> 
	<link rel="icon" href="../html/css/img/book.png" type="image/x-icon" />
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="screen" /> 
	<link type="text/css" rel="stylesheet" href="../html/css/mobile.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
    
</head>
<body>
	
        <h1 xml:lang="en"><span></span>TalesWeaver</h1>
   <div id="container"> 
   <div id="path">Ti trovi in: Soluzioni</div> 
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li><a href="../xml/storie.xml" tabindex="2">Avventure</a></li>
            <li><a href="../html/manuali.html" tabindex="3">Manuali</a></li>
	    <li><a href="../html/mappa.html" tabindex="4">Mappa</a></li>
	    <li>Soluzioni</li>
        </ul>
    </div>
<div class="corpo">
	<h1 id="soluzioniTitle">Soluzioni delle Avventure</h1>
	<p>In questa sezione potrai trovare la soluzione di ogni storia. Le soluzioni possono non portare ad una soluzione vera e propria ma essere dei semplici indirizzamenti per aiutare ad arrivare alla soluzione. Si consiglia di leggere le soluzioni solamente se ci si trova in difficolt&agrave con il proseguimento del gioco.</p>
EOF

if ($esistonostorie==0) {
	print "<p>Al momento non è stata inserita alcuna storia e quindi non si ha alcuna soluzione.</p>";
}
else{
print<<EOF;
<ul id="listaStorie">
EOF

foreach my $species ($xp->find('//storia')->get_nodelist){
	$id=$species->find('@id')->string_value;
print <<EOF;
	<li><a href="../cgi-bin/soluzioni.cgi?id=$id">
EOF
	print $species->find('titolo')->string_value."</a></li>";

    print "\n";
}

print <<EOF;
</ul>
EOF
}
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
