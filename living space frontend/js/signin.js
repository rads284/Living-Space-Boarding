function ValidateEmail() 
{
	var x = document.forms["signin"]["username"].value;
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(x))
	{
		return ValidatePassword();
	}
	else
	{
		document.getElementById("usernameerror").innerHTML = "Incorrect username";
		document.getElementById("usernameerror").style.display = "block";
		return (false);
	}
	
}
function ValidatePassword()
{
	document.getElementById("usernameerror").style.display = "none";
	var y = document.forms["signin"]["password"].value;
	if(y.length >=6) {
	return true;
	} else {
	document.getElementById("passworderror").innerHTML = "Incorrect password";
	document.getElementById("passworderror").style.display = "block";
	return false;
	}
}