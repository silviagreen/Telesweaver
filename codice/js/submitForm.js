function submitForm(idForm){
	var submit=document.getElementById("submitRating");
	submit.style.display="none";//se js è abilitato, viene tolto il bottone di submit ed il submit viene fatto dal js
	document.forms[idForm].submit();
	
}
