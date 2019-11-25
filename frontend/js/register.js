function ValidateEmail() 
{
	var x = document.forms["registerform"]["username"].value;
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(x))
	{
		return ValidatePassword();
	}
	else
	{
		document.getElementById("usernameerror").innerHTML = "Enter a valid email address";
		document.getElementById("usernameerror").style.display = "block";
		return (false);
	}
	
}
function ValidatePassword()
{
	document.getElementById("usernameerror").style.display = "none";
	var y = document.forms["registerform"]["password"].value;
	if(y.length >=6) {
	return ValidateMobile();
	} else {
	document.getElementById("passworderror").innerHTML = "Password must have atleast six characters";
	document.getElementById("passworderror").style.display = "block";
	return false;
	}
}
function ValidateMobile()
{
	document.getElementById("passworderror").style.display = "none";
	var z = document.forms["registerform"]["phonenumber"].value;
	if (/^\d+$/.test(z))
	{
		if(z.length ==10) {
		return true;
		}
		else
		{
			document.getElementById("mobileerror").innerHTML = "Enter a valid mobile number";
			document.getElementById("mobileerror").style.display = "block";
			return false;	
		}
	}
	else {
	document.getElementById("mobileerror").innerHTML = "Enter a valid mobile number";
	document.getElementById("mobileerror").style.display = "block";
	return false;
	}
}
