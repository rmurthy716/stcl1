createHTML();
function createHTML()
{
    var xmlhttp = new XMLHttpRequest();
    var current_url = window.location;
    var url = current_url.protocol + "//" + current_url.host + "/colossus.json";
    var path = current_url.pathname;
    console.log(path);
    xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	    var parsedJson = JSON.parse(xmlhttp.responseText);
            var json_arr = Object.keys(parsedJson).map(function(k) { return parsedJson[k] });
	    var filteredPages = ["/PHY", "/FrontEnd", "/FPGA"];
	    var arr = (filteredPages.indexOf(path) > -1) ?  filterArray(json_arr, path) : json_arr;
            console.log(arr);
	    initializeButtons(json_arr[1])
	    parseJson(arr);
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
	"/FrontEnd" : "Front End"
    };
    var device = pathToDevice[path];
    var registerSetsArr = arr[1];
    var rc = [];
    console.log("Path to device is " + device);
    for(var i = 0; i < registerSetsArr.length; i++) {
	// get register array from json array
	var registerSet = registerSetsArr[i];
	var registers = registerSet["registers"];
	var rcSet = {};
	rcSet["setName"] = registerSet["setName"];
	rcSet["registers"] = [];
	console.log("Registers are " + registers);
	// filter on devices
	var filteredRegisters = registers.filter(function(register) {
	    return register["device"] == device;
	});
	console.log("filtered registers are " + filteredRegisters);
	rcSet["registers"] = filteredRegisters;
	rc.push(rcSet);
    }
    console.log("return is " + rc);
    return [arr[1], rc]
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
    console.log(arr);
    var buttons = {
	"FecEnabled": "#FEC",
	"ANEnable" : "#AN"
    };
    
    for(var i = 0; i < arr.length; i++) {
	var registerSet = arr[i];
	console.log(registerSet);
	var registers = registerSet["registers"];
	console.log(registers);
	for(var j = 0; j < registers.length; j++) {
	    var register = registers[j];
	    var attributes = register["values"];
	    for(var k = 0; k < attributes.length; k++) {
		var curAttribute = attributes[k].attribute;
		var curValue = attributes[k].expectedValue;
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
    console.log(arr);
    for(var i = 0 ; i < arr.length; i++)
    {
	registerSets = arr[i];
	console.log(registerSets);
	registers = registerSets["registers"];
	for(var j = 0; j < registers.length; j++) { 
	    register = registers[j];
	    console.log(register);
	    var htmlKeyId = register["device"];
	    deviceCounts[htmlKeyId] += 1;
	}
    }
    console.log(deviceCounts);
    return deviceCounts;
}
/**************************************************************************************/

function createTitle(arr)
{
    // first element gives us the board family
    var title = "<h2 style=\"margin-top: 0px;\">" + arr[0] + " Port Information<br></h2>";
    document.getElementById("title").innerHTML = title;
    console.log(title);
}
    
    
/**************************************************************************************/

function parseJson(arr) {
    // initialize constant objects 
    var outputObject = {
	"FPGA": "",
	"PHY": "",
	"Front End": ""
    };
    var outputCounter = {
	"FPGA": 0,
	"PHY": 0,
	"Front End": 0
    };

    // create title element
    createTitle(arr);
    
    for(var key in outputObject) {
	// enclose all tables in one container
	outputObject[key] += "<h3><u>" + key + "</u></h3>";
    }
    // second element gives us the port data
    var registerSets = arr[1];
    var deviceCounts = getDeviceCounts(registerSets);
    console.log(registerSets)
    for (var i = 0; i < registerSets.length; i++)
    {
	var registerSet = registerSets[i];
	console.log(registerSet);
	var registers = registerSet["registers"];
	for(var j = 0; j < registers.length; j++) {
	    console.log(registers[j]);
	    var register = registers[j];
	    console.log(register);
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
            outputObject[htmlKeyId] += "<table class=\"table table-hover\">\n";
            outputObject[htmlKeyId] += "<thead>\n";
            outputObject[htmlKeyId] += "<tr>\n";
            outputObject[htmlKeyId] += "<th>Attribute</th>\n";
            outputObject[htmlKeyId] += "<th>Value</th>\n";
	    
	    // close table head
            outputObject[htmlKeyId] += "</thead>";
	    
	    // create table body for attributes
            outputObject[htmlKeyId] += "<tbody>\n";
            var attributes = register["values"];
	    
	    for(var k = 0; k < attributes.length; k++) {
		// create table reference entry
		var curAttribute = attributes[k].attribute;
		var curValue = attributes[k].actualValue;
		outputObject[htmlKeyId] += "<tr>\n";
		outputObject[htmlKeyId] += "<td>" + curAttribute + "</td>\n";
		outputObject[htmlKeyId] += "<td>" + curValue + "</td>\n";
		
		// close table reference
		outputObject[htmlKeyId] += "</tr>\n"; 
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
	    console.log(outputObject[key]);
	}
    }
}

