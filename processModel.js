document.addEventListener("submit", function() 
{
	var email = document.getElementById("email-input").value;
	console.log(email);

	var classifier = document.getElementById("selection").value;
	console.log(classifier);
});