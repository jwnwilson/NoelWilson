$(document).ready(function() {
	
	alert("shits about to get real");
	// Load intro data into blog
	//loadXMLDoc("blog_introText.txt","blog_intro");
	loadData("blog_introText.txt","blog_intro");
});


function loadXMLDoc(filePath, elementID)
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById(elementID).innerHTML=xmlhttp.responseText;
		}
	}
	xmlhttp.open("GET",filePath,true);
	xmlhttp.send();
}
function loadData(url, elementID)
{
	$.ajax({
			url: ("{% url "+ url +" %}"),
			data: {'count': game.count },
			type: 'post',
			async: 'false',
			success: function(data) {
				$( ('#' +elementID) ).show();
				$( ('#' +elementID) ).html(data);
			},
			error: function () {
				console.log("ERROR: loadData for " + url);
			},
		});
}
