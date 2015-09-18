createHTML();

function createHTML()
{
    var xmlhttp = new XMLHttpRequest();
    var current_url = window.location;
    var url = current_url.protocol + "//" + current_url.host + "/colossus.json";
    xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	    var parsedJson = JSON.parse(xmlhttp.responseText);
            var json_arr = Object.keys(parsedJson).map(function(k) { return parsedJson[k] });
            console.log(json_arr);
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

function initializeButton(button, value)
{
    // get current state and possible new state
    var new_state = isTrue(value);
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
/**************************************************************************************/

function getTagCounts(arr) {
    var tagCounts = {
	"FPGA" : 0,
	"PHY" : 0,
	"Front End": 0
    };

    // this sucks but we need to know how many tables
    // there are for each HTML key
    // Traverse JSON once for this
    for(var i = 0; i < data.length; i++) {
	var register = data[i];
	for(var key in register) {
	    if(key.indexOf("register") > -1) {
		var htmlKeyId = register[key].tag;
		tagCounts[htmlKeyId] += 1;
	    }
	}
    }
    return tagCounts;
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
    var buttons = {
	"FecEnabled": "#FEC",
	"AnEnable" : "#AN"
    };
    
    for(var key in outputObject) {
	// enclose all tables in one container
	outputObject[key] += "<h3><u>" + key + "</u></h3>";
    }
    // first element gives us the board family
    var title = "<h2 style=\"margin-top: 0px;\">" + arr[0] + " Port Information<br></h2>";
    document.getElementById("title").innerHTML = title;
    console.log(title);

    // second element gives us the port data
    data = arr[1];

    var tagCounts = getTagCounts(data);
    
    for(var i = 0; i < data.length; i++) {
        var register = data[i];
        for(var key in register) {
            // Mdio and I2c registers have additional keys
            // only care about register object
	    
            if(key.indexOf("register") > -1) {
		// get counter for formatting three tables per row
		var htmlKeyId = register[key].tag;
		var keyIdCounter = outputCounter[key];
		
		if((keyIdCounter % 3) == 0) {
		    // if first element of our row then start
		    // a new row div
		    outputObject[htmlKeyId] += "<div class=\"row\">\n";
		}
		
		// create column object for our register
		outputObject[htmlKeyId] += "<div class=\"col-md-4\">\n";
		
                // create header for our table with register name
                outputObject[htmlKeyId] += '<h4>' + register[key].name + '</h4>\n';
		
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
                var attributes = register[key].values;

		for(var j = 0; j < attributes.length; j++) {
                    // create table reference entry
                    var curAttribute = attributes[j].attribute;
                    var curValue = attributes[j].defaultValue;
                    outputObject[htmlKeyId] += "<tr>\n";
                    outputObject[htmlKeyId] += "<td>" + curAttribute + "</td>\n";
                    outputObject[htmlKeyId] += "<td>" + curValue + "</td>\n";

		    // close table reference
                    outputObject[htmlKeyId] += "</tr>\n";

		    // initialize button if applicable 
		    for(var buttonKey in buttons)
		    {
			if(curAttribute == buttonKey) {
                            initializeButton(buttons[buttonKey], curValue);
			}
                    } 
                }
                // close table body
                outputObject[htmlKeyId] += "</tbody>\n";
                outputObject[htmlKeyId] += "</table>";
		
                // close the column
                outputObject[htmlKeyId] += "</div>";
                if(((keyIdCounter % 3) == 2) || (keyIdCounter == tagCounts[htmlKeyId] - 1))
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
		outputCounter[key] += 1;		
            }
        }
    }
    for(var key in outputObject) {
	document.getElementById(key).innerHTML = outputObject[key];
	console.log(outputObject[key]);
    }
}

