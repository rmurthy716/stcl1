createHTML();
function createHTML()
{
    var xmlhttp = new XMLHttpRequest();
    var current_url = window.location;
    var url = current_url.protocol + "//" + current_url.host + "/portInfo.json";
    var path = current_url.pathname;
    //console.log(path);
    xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	    var parsedJson = JSON.parse(xmlhttp.responseText);
	    //console.log(parsedJson);
            var json_arr = Object.keys(parsedJson).map(function(k) { return parsedJson[k] });
	    //var filteredPages = ["/PHY", "/FrontEnd", "/FPGA"];
	    //var arr = (filteredPages.indexOf(path) > -1) ?  filterArray(json_arr, path) : json_arr;
            //console.log(arr);
	    initializeButtons(json_arr[1])
	    parseJson(json_arr);
	}
    }

    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    // refresh every 2 seconds if polling toggle is on
    if($('#poll').is(":checked")) {
	setTimeout(createHTML, 2000);
    }
}
/**************************************************************************************/

function filterArray(arr, path){
    /*
      @param arr : Array to filter
      @param path : URL path
      
      Will filter out array based on path name. 
      The current possible paths to filter are #FPGAPage, #PHYPage, #FrontEndPage
     */
    var pathToDevice = {
	"/PHY" : "PHY",
	"/FPGA" : "FPGA",
	"/FrontEnd" : "Front_End"
    };
    var device = pathToDevice[path];
    var registerSetsArr = arr[1];
    var rc = [];
    //console.log("Path to device is " + device);
    for(var i = 0; i < registerSetsArr.length; i++) {
	// get register array from json array
	var registerSet = registerSetsArr[i];
	var registers = registerSet["registers"];
	var rcSet = {};
	rcSet["setName"] = registerSet["setName"];
	rcSet["registers"] = [];
	//console.log("Registers are " + registers);
	// filter on devices
	var filteredRegisters = registers.filter(function(register) {
	    return register["device"] == device;
	});
	//console.log("filtered registers are " + filteredRegisters);
	rcSet["registers"] = filteredRegisters;
	rc.push(rcSet);
    }
    //console.log("return is " + rc);
    return [arr[0], rc]
}

    
/**************************************************************************************/

function isTrue(value){
    if (typeof(value) == 'string'){
        value = value.toLowerCase();
    }
    switch(value){
    case true:
    case "true":
    case 1:
    case "1":
    case "on":
    case "yes":
        return true;
    default: 
        return false;
    }
}

/**************************************************************************************/

function initializeButtons(arr)
{
    //console.log(arr);
    var buttons = {
	"FEC Enabled": "#FEC",
	"AN Enable" : "#AN"
    };
    
    for(var i = 0; i < arr.length; i++) {
	var registerSet = arr[i];
	//console.log(registerSet);
	if(registerSet == null) {
	    //console.log("registerSet is Null!")
	    continue;
	}
	var registers = registerSet["registers"];
	//console.log(registers);
	for(var j = 0; j < registers.length; j++) {
	    var register = registers[j];
	    var attributes = register["values"];
	    for(var k = 0; k < attributes.length; k++) {
		var curAttribute = attributes[k].attribute;
		var curValue = attributes[k].actualValue;
		if(buttons.hasOwnProperty(curAttribute)) {
		    button = buttons[curAttribute]
		    // get current state and possible new state
		    var new_state = isTrue(curValue);
		    var current_state = isTrue($(button).is(":checked"));
		    
		    // only toggle the button if the states are different
		    // toggling of the buttons generate POST requests
		    // don't generate POST requests unless necessary 
		    if(new_state != current_state) {
			if(new_state) {
			    $(button).bootstrapToggle('on');
			}
			else {
			    $(button).bootstrapToggle('off');
			}
		    }
		}
	    }
	}
    }
}
/**************************************************************************************/

function getDeviceCounts(arr) {
    var deviceCounts = {
	"FPGA" : 0,
	"PHY" : 0,
	"Front End": 0
    };
    //console.log(arr);
    for(var i = 0 ; i < arr.length; i++)
    {
	registerSets = arr[i];
	//console.log(registerSets);
	if(registerSets == null) {
	    //console.log("registerSets is Null!")
	    continue;
	}
	registers = registerSets["registers"];
	for(var j = 0; j < registers.length; j++) { 
	    register = registers[j];
	    //console.log(register);
	    var htmlKeyId = register["device"];
	    deviceCounts[htmlKeyId] += 1;
	}
    }
    //console.log(deviceCounts);
    return deviceCounts;
}
/**************************************************************************************/

function createTitle(arr) {
    // first element gives us the board family
    var title = "<h2 style=\"margin-top: 0px;\">" + arr[0] + " Port Information<br></h2>";
    document.getElementById("title").innerHTML = title;
    //console.log(title);
}
    
    
/**************************************************************************************/

function comparisonNotEqual(actual, expected) {
    return (actual != expected);
}

function comparisonEqual(actual, expected) {
    return (actual == expected);
}

function comparisonLessEqual(actual, expected) {
    return (actual <= expected);
}

/**************************************************************************************/

function parseJson(arr) {
    // initialize  objects
    var comparisonFunctions = {
	"NEQ" : comparisonNotEqual,
	"EQ"  : comparisonEqual,
	"LEQ" : comparisonLessEqual
    };
    var outputObject = {
	"FPGA": "",
	"PHY": "",
	"Front_End": ""
    };
    var outputCounter = {
	"FPGA": 0,
	"PHY": 0,
	"Front_End": 0
    };

    var contextRows = {
	"success": "<tr class=\"success\">",
	"danger":  "<tr class=\"danger\">",
	"warning": "<tr class=\"warning\">",
	"info":    "<tr class=\"info\">",
	"":        "<tr>"
    };

    // create title element
    createTitle(arr);
    
    for(var key in outputObject) {
	// enclose all tables in one container
	outputObject[key] += "<h3><u>" + key + "</u></h3>";
    }
    // second element gives us the port data
    var registerSets = arr[1];
    createDiagnosisPage(registerSets);
    var deviceCounts = getDeviceCounts(registerSets);
    //console.log(registerSets)
    for (var i = 0; i < registerSets.length; i++)
    {
	var registerSet = registerSets[i];
	//console.log(registerSet);
	if(registerSet == null) {
	    console.log("registerSet is Null!")
	    continue;
	}
	var registers = registerSet["registers"];
	for(var j = 0; j < registers.length; j++) {
	    //console.log(registers[j]);
	    var register = registers[j];
	    //console.log(register);
            var htmlKeyId = register["device"];
	
	    // create row
	    var keyIdCounter = outputCounter[htmlKeyId];
	    
	    if((keyIdCounter % 3) == 0) {
		// if first element of our row then start
		// a new row div
		outputObject[htmlKeyId] += "<div class=\"row\">\n";
	    }
	    
	    // create column object for our register
	    outputObject[htmlKeyId] += "<div class=\"col-md-4\">\n";
	    
            // create header for our table with register name
            outputObject[htmlKeyId] += '<h4>' + register["name"] + '</h4>\n';
	    
            // create table for our attributes
            outputObject[htmlKeyId] += "<table class=\"table table-hover table-bordered\">\n";
            outputObject[htmlKeyId] += "<thead>\n";
            outputObject[htmlKeyId] += "<tr>\n";
            outputObject[htmlKeyId] += "<th>Attribute</th>\n";
	    outputObject[htmlKeyId] += "<th>Value</th>\n";
            outputObject[htmlKeyId] += "<th>Status</th>\n";
	    
	    // close table head
            outputObject[htmlKeyId] += "</thead>";
	    
	    // create table body for attributes
            outputObject[htmlKeyId] += "<tbody>\n";
            var attributes = register["values"];
	    
	    for(var k = 0; k < attributes.length; k++) {
		// create table reference entry
		var curAttribute = attributes[k].attribute;
		var curValue = attributes[k].actualValue;
		var comparisonOperatorString = attributes[k].comparisonOperator;
		//console.log("Combo operator string is " + comparisonOperatorString);
		//console.log(comparisonFunctions[comparisonOperatorString]);
		var status = comparisonFunctions[comparisonOperatorString](curValue, attributes[k].expectedValue);
		var statusMessages = attributes[k].statusMessages;
		if(status) {
		    var statusObject = statusMessages.trueStatus;
		   
		}
		else {
		    var statusObject = statusMessages.falseStatus;
		}

		var message = statusObject.message;
		var level = statusObject.level;
		if(message != "") {
		    outputObject[htmlKeyId] += contextRows[level];
		    outputObject[htmlKeyId] += "<td>" + curAttribute + "</td>\n";
		    outputObject[htmlKeyId] += "<td>" + curValue + "</td>\n";
		    outputObject[htmlKeyId] += "<td>" + message + "</td>\n";
		    
		    // close table reference
		    outputObject[htmlKeyId] += "</tr>\n";
		}
            }
            // close table body
            outputObject[htmlKeyId] += "</tbody>\n";
            outputObject[htmlKeyId] += "</table>";
	    
            // close the column
            outputObject[htmlKeyId] += "</div>";
	    
	    if(((outputCounter[htmlKeyId] % 3) == 2) || (outputCounter[htmlKeyId] == (deviceCounts[htmlKeyId] - 1)))
	    {
		/*
		  If we're at an element index which is a multiple of 3
		  Or in terms of our zero based index if index mod 3 is 2
		  Close the row since we have three tables per row.
		  If we don't have enough (3) tables for the end of the row
		  then close the row if we've reached the last register
		*/
		outputObject[htmlKeyId] += "</div>";
	    }
       	    // increment counter for html key
	    outputCounter[htmlKeyId] += 1;		
	}
    }
    for(var key in outputObject) {
	// only set html if there are attributes
	if(outputCounter[key] > 0) {
	    document.getElementById(key).innerHTML = outputObject[key];
	    //console.log(outputObject[key]);
	}
    }
}

function createDiagnosisPage(registerSets)
{
    var deviceToHtmlTag = {
	"FPGA": "PCSDiag",
	"Front_End": "FrontEndDiag",
	"PHY": "PHYDiag"
    }
    
    var comparisonFunctions = {
	"NEQ" : comparisonNotEqual,
	"EQ"  : comparisonEqual,
	"LEQ" : comparisonLessEqual
    };

    var outputObject = {
	"FPGA": "",
	"PHY": "",
	"Front_End" : ""
    };

    var fpgaLedValues = {
	"Block Lock" : {},
	"Sync": {},
	"BIP8" : {},
	"Length Errors": {},
	"Repeat Errors": {},
	"Marker Errors": {}
    }

    var phyLedValues = {
	"PMD Lock" : {},
	"PMD Signal" : {}
    }

    var frontEndLedValues = {
	"Tx Power": {},
	"Tx Signal": {},
	"Tx Lock": {},
	"Rx Power": {},
	"Rx Signal": {},
	"Rx Lock": {}
    }

    var deviceToLed = {
	"FPGA": fpgaLedValues,
	"PHY": phyLedValues,
	"Front_End": frontEndLedValues
    }
    
    // create our tables
    outputObject["FPGA"] += "<div class=\"row\">\n";
    outputObject["FPGA"] += "<div class=\"col-md-12\">\n";
    outputObject["FPGA"] += "<h4> <b><u>PCS Diagnosis </b></u></h4>\n";
    outputObject["FPGA"] += "<table class=\"table table-hover\">\n";
    outputObject["FPGA"] += "<thead>\n";
    outputObject["FPGA"] += "<tr>\n";
    outputObject["FPGA"] += "<th>Lane</th>\n";
    outputObject["FPGA"] += "<th>Block Lock</th>\n";
    outputObject["FPGA"] += "<th>Sync</th>\n";
    outputObject["FPGA"] += "<th> BIP8 </th>\n";
    outputObject["FPGA"] += "<th> Length Errors</th>\n";
    outputObject["FPGA"] += "<th> Repeat Errors</th>\n";
    outputObject["FPGA"] += "<th> Marker Errors</th>\n";
    outputObject["FPGA"] += "</tr>\n";
    outputObject["FPGA"] += "</thead>";
    outputObject["FPGA"] += "<tbody>\n";

    outputObject["PHY"] += "<div class=\"row\">\n";
    outputObject["PHY"] += "<div class=\"col-md-12\">\n";
    outputObject["PHY"] += "<h4> <b><u>PHY Diagnosis</b></u> </h4>\n";
    outputObject["PHY"] += "<table class=\"table table-hover\">\n";
    outputObject["PHY"] += "<thead>\n";
    outputObject["PHY"] += "<tr>\n";
    outputObject["PHY"] += "<th>PMD Lock</th>\n";
    outputObject["PHY"] += "<th>PMD Signal</th>\n";
    outputObject["PHY"] += "</tr>\n";
    outputObject["PHY"] += "</thead>";
    outputObject["PHY"] += "<tbody>\n";

    outputObject["Front_End"] += "<div class=\"row\">\n";
    outputObject["Front_End"] += "<div class=\"col-md-12\">\n";
    outputObject["Front_End"] += "<h4> Front End Diagnosis </h4>\n";
    outputObject["Front_End"] += "<table class=\"table table-hover\">\n";
    outputObject["Front_End"] += "<thead>\n";
    outputObject["Front_End"] += "<tr>\n";
    outputObject["Front_End"] += "<th>Lane</th>\n";
    outputObject["Front_End"] += "<th>Tx Power</th>\n";
    outputObject["Front_End"] += "<th>Tx Signal</th>\n";
    outputObject["Front_End"] += "<th>Tx Lock</th>\n";
    outputObject["Front_End"] += "<th>Rx Power</th>\n";
    outputObject["Front_End"] += "<th>Rx Signal</th>\n";
    outputObject["Front_End"] += "<th>Rx Lock</th>\n";
    outputObject["Front_End"] += "</tr>\n";
    outputObject["Front_End"] += "</thead>";
    outputObject["Front_End"] += "<tbody>\n";

    for(var i = 0; i < registerSets.length; i++)
    {
	var registerSet = registerSets[i];
	if(registerSet == null) {
	    continue;
	}

	var registers = registerSet["registers"];
	for(var j = 0; j < registers.length; j++)
	{
	    var register = registers[j];
	    var htmlkeyId = register["device"];
	    var attributes = register["values"];
	    var ledValues = deviceToLed[htmlkeyId];

	    for(var k = 0; k < attributes.length; k++)
	    {
		if("diagnosis" in attributes[k])
		{
		    var curValue = attributes[k].actualValue;
		    var comparisonOperatorString = attributes[k].comparisonOperator;
		    var status = comparisonFunctions[comparisonOperatorString](curValue, attributes[k].expectedValue);
		    var attribute = ledValues[attributes[k].diagnosis["attribute"]];
		    attribute[attributes[k].diagnosis["lane"]] = status;
		}
	    }
	}
    }

    // create PCS rows
    // kinda hard coded to 20 but lets try and be dynamic in future
    for(var c = 1; c <= 20; c++)
    {
	outputObject["FPGA"] += "<tr>";
	outputObject["FPGA"] += "<td>" + c + "</td>";
	outputObject["FPGA"] += "<td>" + boolToLed(fpgaLedValues["Block Lock"][c]) + "</td>";
	outputObject["FPGA"] += "<td>" + boolToLed(fpgaLedValues["Sync"][c]) + "</td>";
	outputObject["FPGA"] += "<td>" + boolToLed(fpgaLedValues["BIP8"][c]) + "</td>";
	outputObject["FPGA"] += "<td>" + boolToLed(fpgaLedValues["Length Errors"][c]) + "</td>";
	outputObject["FPGA"] += "<td>" + boolToLed(fpgaLedValues["Repeat Errors"][c]) + "</td>";
	outputObject["FPGA"] += "<td>" + boolToLed(fpgaLedValues["Marker Errors"][c]) + "</td>";
    }

    for(var b = 1; b <=4; b++)
    {
	outputObject["Front_End"] += "<tr>";
	outputObject["Front_End"] += "<td>" + b + "</td>";
	outputObject["Front_End"] += "<td>" + boolToLed(frontEndLedValues["Tx Power"][b]) + "</td>";
	outputObject["Front_End"] += "<td>" + boolToLed(frontEndLedValues["Tx Signal"][b]) + "</td>";
	outputObject["Front_End"] += "<td>" + boolToLed(frontEndLedValues["Tx Lock"][b]) + "</td>";
	outputObject["Front_End"] += "<td>" + boolToLed(frontEndLedValues["Rx Power"][b]) + "</td>";
	outputObject["Front_End"] += "<td>" + boolToLed(frontEndLedValues["Rx Signal"][b]) + "</td>";
	outputObject["Front_End"] += "<td>" + boolToLed(frontEndLedValues["Rx Lock"][b]) + "</td>";
    }
    console.log(frontEndLedValues);

    for(var key in outputObject) {
	var htmlId = deviceToHtmlTag[key];
	outputObject[key] += "</tbody></table></div>";
	document.getElementById(htmlId).innerHTML = outputObject[key];
    }
}
    
    
function boolToLed(value)
{
    var output = ""
    if(!value)
    {
	output += "<button type=\"button\" class=\"btn-circle-green\"></button>";
    }
    else
    {
	output += "<button type=\"button\" class=\"btn-circle-red\"></button>";
    }
    return output;
}

    
