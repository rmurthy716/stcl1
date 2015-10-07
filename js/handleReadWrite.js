handleReadWrite();

function handleReadWrite()
{
    initializeForms();
    handleFormChange();
    handleSubmit();
}

function initializeForms()
{
    initializeMdioForm();
    initializeI2cForm();
    initializeBar1Form();
}

function initializeMdioForm()
{
    $('#mdioDevAddr').val("");
    $('#mdioDevAddr').attr("readonly", false);
    $('#mdioPortAddr').val("");
    $('#mdioPortAddr').attr("readonly", false);
    $('#mdioRegAddr').val("");
    $('#mdioData').val(""); 
}

function initializeI2cForm()
{
    $('#i2cDevAddr').val("");
    $('#i2cDevAddr').attr("readonly", false);
    $('#i2cBusSel').val("");
    $('#i2cBusSel').attr("readonly", false);
    $('#i2cRegAddr').val("");
    $('#i2cData').val("");
}

function initializeBar1Form()
{
    $('#bar1Addr').val("");
    $('#bar1Data').val("");
}

function handleFormChange()
{
    handleMdioChange();
    handleI2cChange();
}

function handleMdioChange()
{
    $('#mdiosel').change(function() {
	var mdioSelect = $('#mdiosel :selected').text();
	// hide the form while the changes take place
	$('#mdioForm').hide();
	if(mdioSelect == "None")
	{
	    initializeMdioForm();
	}
	else if(mdioSelect == "Broadcom Retimer")
	{
	    $('#mdioDevAddr').val("0x1");
	    $('#mdioDevAddr').attr("readonly", false);
	    $('#mdioPortAddr').val("0xe");
	    $('#mdioPortAddr').attr("readonly", true);
	}
	else if(mdioSelect == "Broadcom Gearbox")
	{
	    $('#mdioDevAddr').val("0x1");
	    $('#mdioDevAddr').attr("readonly", true);
	    $('#mdioPortAddr').val("0x0");
	    $('#mdioPortAddr').attr("readonly", true);
	}
	$('#mdioRegAddr').val("");
	$('#mdioData').val("");
	$('#mdioForm').fadeIn(600);
    })
}

function handleI2cChange()
{
    $('#i2csel').change(function() {
	var i2cSelect = $('#i2csel :selected').text();
	$('#i2cForm').hide();
	if(i2cSelect == "None")
	{
	    initializeI2cForm();
	}
	else if(i2cSelect == "QSFP Module")
	{
	    $('#i2cBusSel').val("0x9");
	    $('#i2cBusSel').attr("readonly", true);
	    $('#i2cDevAddr').val("0x50");
	    $('#i2cDevAddr').attr("readonly", true);
	}
	$('#i2cRegAddr').val("");
	$('#i2cData').val("");
	$('#i2cForm').fadeIn(600);
    })
}

function handleSubmit()
{
   handleMdioSubmit();
   handleI2cSubmit();
   handleBar1Submit();
}

function handleMdioSubmit()
{
    $(document).ready(function(){
	$('#mdioForm').submit(function(event){
	    var btn = $(this).find("input[type=submit]:focus" );
	    console.log(btn);
	    console.log(btn['0']['name']);
	    event.preventDefault();
	    var currentUrl = window.location;
	    var postUrl = currentUrl.protocol + "//" + currentUrl.host;
	    var postData = $(this).serialize();
	    // get the button value and add it to the data
	    // this is such a hack but it works 
	    postData += "&Attribute=" + btn['0']['name'];
	    console.log(postData);
	    $.ajax({
		url: postUrl,
		type: 'POST',
		data: postData,
		success: function(data) {
		    console.log(data);
		    var parsedData = JSON.parse(data);
		    console.log(parsedData);
		    var outputHtml = ""
		    if(parsedData["level"] == "success")
		    {
			outputHtml += "<div class=\"alert alert-success fade in\">";
		    }
		    else
		    {
			outputHtml += "<div class=\"alert alert-danger fade in\">";
		    }
		    outputHtml += "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>"
		    outputHtml += "<strong>" + parsedData["data"] + "</strong>";
		    outputHtml += "</div>";
		    document.getElementById("MdioStatus").innerHTML = outputHtml;
		}
	    });
	});
    });
}

function handleI2cSubmit()
{
    $(document).ready(function(){
	$('#i2cForm').submit(function(event){
	    var btn = $(this).find("input[type=submit]:focus" );
	    console.log(btn);
	    console.log(btn['0']['name']);
	    event.preventDefault();
	    var currentUrl = window.location;
	    var postUrl = currentUrl.protocol + "//" + currentUrl.host;
	    var postData = $(this).serialize();
	    // get the button value and add it to the data
	    // this is such a hack but it works
	    postData += "&Attribute=" + btn['0']['name'];
	    console.log(postData);
	    $.ajax({
		url: postUrl,
		type: 'POST',
		data: postData,
		success: function(data) {
		    console.log(data);
		    var parsedData = JSON.parse(data);
		    console.log(parsedData);
		    var outputHtml = ""
		    if(parsedData["level"] == "success")
		    {
			outputHtml += "<div class=\"alert alert-success fade in\">";
		    }
		    else
		    {
			outputHtml += "<div class=\"alert alert-danger fade in\">";
		    }
		    outputHtml += "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>"
		    outputHtml += "<strong>" + parsedData["data"] + "</strong>";
		    outputHtml += "</div>";
		    document.getElementById("I2cStatus").innerHTML = outputHtml;
		    
		}
	    });
	});
    });
}

function handleBar1Submit()
{
    $(document).ready(function(){
	$('#bar1Form').submit(function(event){
	    var btn = $(this).find("input[type=submit]:focus" );
	    console.log(btn);
	    console.log(btn['0']['name']);
	    event.preventDefault();
	    var currentUrl = window.location;
	    var postUrl = currentUrl.protocol + "//" + currentUrl.host;
	    var postData = $(this).serialize();
	    // get the button value and add it to the data
	    // this is such a hack but it works
	    postData += "&Attribute=" + btn['0']['name'];
	    console.log(postData);
	    $.ajax({
		url: postUrl,
		type: 'POST',
		data: postData,
		success: function(data) {
		    console.log(data);
		    var parsedData = JSON.parse(data);
		    console.log(parsedData);
		    var outputHtml = ""
		    if(parsedData["level"] == "success")
		    {
			outputHtml += "<div class=\"alert alert-success fade in\">";
		    }
		    else
		    {
			outputHtml += "<div class=\"alert alert-danger fade in\">";
		    }
		    outputHtml += "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>"
		    outputHtml += "<strong>" + parsedData["data"] + "</strong>";
		    outputHtml += "</div>";
		    document.getElementById("Bar1Status").innerHTML = outputHtml;
		    
		}
	    });
	});
    });
}
