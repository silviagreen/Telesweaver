<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:e="http://www.storie.com">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>

<xsl:template match="/">	
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
	<title>Elenco delle storie</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="keywords" content="avventure testuali, gioco interattivo, colleziona oggetti, testo, storia, game"/>
    <meta name="description" content="avventure testuali, storie su cui si pu� giocare e interagire con il testo" />
    <meta name="author" content="Lapolla Margherita"/>
	<meta name="language" content="italian it"/>
     <link type="text/css" rel="stylesheet" href="../html/css/desktop.css" media="handheld, screen and (min-width:481px), only screen and (min-device-width:481px)" />
     <link type="text/css" rel="stylesheet" href="css/Device.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" /> 
     <link type="text/css" rel="stylesheet" href="css/Print.css" media="print" />
</head>
<body>

    	
        <h1 xml:lang="en"><span> Adventure</span></h1>
        <!--<span class="log"><a href="login.html" xml:lang="en">Login</a> <a href="registrazione.html">Registrati</a></span>-->
  <div id="container">
    <div id="menu">
    	<ul id="menuLista">
        	<li id="home"><a href="../html/Home.html" tabindex="1" accesskey="h">Home</a></li>
            <li id="attivo">Avventure</li>
            <li id="mappa"><a href="" tabindex="2" accesskey="m">Mappa</a></li>
        </ul>
    </div>
 
    <div class="corpo">
    <h2>Le nostre storie</h2>
	<dl class="storie"> 
		<xsl:for-each select="e:storie/e:storia">
			<dt>
				<xsl:value-of select="e:titolo"/>
				<ul>
					<li><a href="storie.cgi?id={@id}" >Gioca</a></li>
					<li><a href="../../../../recensioni.cgi?id={@id}" >Recensioni</a></li>
				</ul>
			</dt>	
			<dd><xsl:value-of select="e:descrizione"/></dd>
		</xsl:for-each>
	</dl>
   </div>	   
 </div>
   
    
    <div id="piede">
	 <a href="http://validator.w3.org/check?uri=referer">
	 <img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>

   	 <a href="http://validator.w3.org/check?uri=referer">
	<img src="http://www.w3.org/Icons/valid-css.gif" alt="Valid CSS 2" height="31" width="88" /></a>   
    </div>

</body>
</html>
</xsl:template >

</xsl:stylesheet> 
