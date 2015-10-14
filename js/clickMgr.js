initializeView()
manageClicks();

function initializeView()
{
    $("#Mdio").hide();
    $("#I2C").hide();
    $("#Bar1").hide();
    $("#PCSDiag").hide();
    $("#PHYDiag").hide();
    $("#FrontEndDiag").hide();
}
    
function manageClicks()
{
    handlePollChange();
    handleANChange();
    handleFECChange();
    handleAutoRecovery();
    handleAutoRecoveryChange();
    handleRecoverLink();
    handlePageChange();
}

function handlePollChange()
{
    $(function() {
	  $("#poll").change(function() {
	 createHTML();
	  })
    })
}

function handleAutoRecoveryChange()
{
    $(function() {
	$("#AutoRecovery").change(function() {
	    if($('#AutoRecovery').is(":checked")) {
		handleAutoRecovery();
	    }
	})
    })
}

function handleANChange()
{
    $(function() {
	$("#AN").change(function() {
	    $.post("AN", {"Attribute": "AN", "Value": ($("#AN").is(":checked"))});
	})
    })
}

function handleFECChange()
{
    $(function() {
	$("#FEC").change(function() {
	    $.post("FEC", {"Attribute": "FEC", "Value": ($("#FEC").is(":checked"))});
        })
    })
}

function handleAutoRecovery()
{
    if($('#AutoRecovery').is(":checked")) {
	$.post("Recover Link", {"Attribute": "RecoverLink"});
	setTimeout(handleAutoRecovery, 3000);
    }

}

function handleRecoverLink()
{
    $(function() {
	$("#RecoverLink").click(function() {
	    $.post("Recover Link", {"Attribute": "RecoverLink"});
	})
    })
}

function handlePageChange()
{
    // device page management
    handleFrontEndPage();
    handlePhyPage();
    handleFpgaPage();
    handleAllDevicesPage();

    // developer mode page management
    handleMdioPage();
    handleI2cPage();
    handleBar1Page();
    handleAllProtocolsPage();

    handlePCSDiagnosisPage();
    handlePHYDiagnosisPage();
    handleFrontEndDiagnosisPage();
}

function handleFrontEndPage()
{
    $(function() {
	$("#FrontEndPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#Front_End").fadeIn(600);
	})
    })
}

function handlePhyPage()
{
    $(function() {
	$("#PHYPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#PHY").fadeIn(600);
	})
    })
}

function handleFpgaPage()
{
    $(function() {
	$("#FPGAPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#FPGA").fadeIn(600);
	})
    })
}

function handleAllDevicesPage()
{
    $(function() {
	$("#AllPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#Front_End").fadeIn(600);
	    $("#PHY").fadeIn(600);
	    $("#FPGA").fadeIn(600);
	})
    })
}

function handleMdioPage()
{
    $(function() {
	$("#MdioPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#Mdio").fadeIn(600);
	})
    })
}

function handleI2cPage()
{
    $(function() {
	$("#I2CPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#I2C").fadeIn(600);
	})
    })
}

function handleBar1Page()
{
    $(function() {
	$("#Bar1PageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#Bar1").fadeIn(600);
	})
    })
}

function handleAllProtocolsPage()
{
    $(function() {
	$("#AllProtocolsPageId").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#Mdio").fadeIn(600);
	    $("#I2C").fadeIn(600);
	    $("#Bar1").fadeIn(600);
	})
    })
}

function handlePCSDiagnosisPage()
{
    $(function() {
	$("#PCSDiagnosis").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#PCSDiag").fadeIn(600);
	})
    })
}

function handlePHYDiagnosisPage()
{
    $(function() {
	$("#PHYDiagnosis").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#PHYDiag").fadeIn(600);
	})
    })
}

function handleFrontEndDiagnosisPage()
{
    $(function() {
	$("#FrontEndDiagnosis").click(function() {
	    $("#Front_End").hide();
	    $("#PHY").hide();
	    $("#FPGA").hide();
	    $("#Mdio").hide();
	    $("#I2C").hide();
	    $("#Bar1").hide();
	    $("#PCSDiag").hide();
	    $("#PHYDiag").hide();
	    $("#FrontEndDiag").hide();
	    $("#FrontEndDiag").fadeIn(600);
	})
    })
}


    











    

