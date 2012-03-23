/**
 * @author margherita
 */
//funzione che controlla se il tipo dei dati è corretto
function controllaTipiRecensione(idElemento, idError) {
		var pos=document.getElementById(idElemento).value.search(/\D/);
		if(pos!=0){//pos!=0 vuol dire che il match non e riuscito. 
			document.getElementById(idError).style.display="inline";
			document.getElementById(idElemento).focus();
			return false;
		}
		else{
			document.getElementById(idError).style.display="none";}
			return true;
	} 