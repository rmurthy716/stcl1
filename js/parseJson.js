createHTML();

function createHTML()
{
    var xmlhttp = new XMLHttpRequest();
    var url = "http://hw-ci-n11u-01.calenglab.spirentcom.com:51485/colossus.json";
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
}


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

function initializeButton(button, value)
{
    var state = isTrue(value);
    if(state) {
      $(button).bootstrapToggle('on');
    }
    else {
	$(button).bootstrapToggle('off');
    }
}    

function parseJson(arr) {
    var out = "";
    // first element gives us the board family
    var title = "<h2 style=\"margin-top: 0px;\">" + arr[0] + " Port Information<br></h2>";
    document.getElementById("title").innerHTML = title;
    console.log(title);
    // second element gives us the port data
    data = arr[1];
    // enclose all tables in one container
    out += "<div class=\"container\">\n";
    for(var i = 0; i < data.length; i++) {
        if((i % 3) == 0) {
            // if first element of our row then start
            // a new row div
            out += "<div class=\"row\">\n";
        }
        // create column object for our register
        var register = data[i];
        for(var key in register) {
            // Mdio and I2c registers have additional keys
            // only care about register object
            if(key.indexOf("register") > -1) {
                // create header for our table with register name
                out += "<div class=\"col-lg-4\">\n";
                out += '<h3>' + register[key].name + '</h3>\n';
                // create table for our attributes
                out += "<table class=\"table table-hover\">\n";
                out += "<thead>\n";
                out += "<tr>\n";
                out += "<th>Attribute</th>\n";
                out += "<th>Value</th>\n";
                // close table head
                out += "</thead>";
                // create table body for attributes
                out += "<tbody>\n";
                var attributes = register[key].values;
                for(var j = 0; j < attributes.length; j++) {
                    // create table reference entry
                    var curAttribute = attributes[j].attribute;
                    var curValue = attributes[j].defaultValue;
                    out += "<tr>\n";
                    out += "<td>" + curAttribute + "</td>\n";
                    out += "<td>" + curValue + "</td>\n";
                    // close table reference
                    out += "</tr>\n";
                    // initialize buttons
                    if(curAttribute === "FecEnabled") {
                        initializeButton('#FEC', curValue);
                    }
                    else if(curAttribute === "ANEnable") {
                        initializeButton('#AN', curValue);
                    } 
                }
                // close table body
                out += "</tbody>\n";
                out += "</table>";
                // close the column
                out += "</div>";
                if(((i % 3) == 2) || (i == (data.length - 1)))
                {
                    /*
                          If we're at an element index which is a multiple of 3
                          Or in terms of our zero based index if index mod 3 is 2
                          Close the row since we have three tables per row.
                          If we don't have enough (3) tables for the end of the row
                          then close the row if we've reached the last register
                    */
                    out += "</div>";
                }
		
            }
        }
    }
    // close the container
    out += "</div>";
    document.getElementById("section").innerHTML = out;
    console.log(out);
}

