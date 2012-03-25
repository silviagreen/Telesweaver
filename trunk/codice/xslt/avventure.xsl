<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:e="http://www.storie.com">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>

<xsl:template match="/">	
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Elenco delle storie - TalesWeaver</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="elenco avventure testuali a cui si può giocare" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
	<link rel="icon" href="../html/css/img/book.png" type="image/x-icon" />
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="screen" />
     <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" /> 
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>

    	
        <h1 xml:lang="en"><span></span> TalesWeaver</h1>
        <!--<span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span>-->
  <div id="container">
   <div id="path">Ti trovi in: Avventure</div>
    <div id="menu">
    	<ul id="menuLista">
        	<li><a href="../html/Home.html" tabindex="1">Home</a></li>
            <li>Avventure</li>
            <li><a href="../html/manuali.html" tabindex="2">Manuali</a></li>
	   <li><a href="../html/mappa.html" tabindex="3">Mappa</a></li>
	   <li><a href="../cgi-bin/lista.cgi" tabindex="4">Soluzioni</a></li>
        </ul>
    </div>
 
    <div class="corpo">
    <h2>Le nostre storie</h2>
	<dl class="storie"> 
		<xsl:for-each select="e:storie/e:storia">
			<dt>
				<xsl:value-of select="e:titolo"/>
				<ul>
					<li><a href="../cgi-bin/storia.cgi?id={@id}" >Gioca</a></li>
					<li><a href="../cgi-bin/readRecensioni.cgi?id={@id}" >Recensioni</a></li>
				</ul>
			</dt>	
			<dd><xsl:value-of select="e:descrizione"/><a class="su" href="#container">Torna su</a></dd>
			
		</xsl:for-each>
	</dl>
   </div>	   
 </div>
   
    
    <div id="piede">
					<img src="../html/css/img/css.gif" alt="CSS Valid!"/>
        			<img src="../html/css/img/xhtml10.png" alt="XHTML 1.0 Valid!"/>
    </div>

</body>
</html>
</xsl:template >

</xsl:stylesheet> 
