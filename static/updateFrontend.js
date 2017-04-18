var BASEURL = "http://127.0.0.1:5000";
var textEnum =
    {
        DISCHARGE_RATE: 1,
        GAGE_HEIGHT: 2,
        FAQ: 3
    };
var gageHeightTexts = ["Loading text..."];
var dischargeRateTexts = ["Loading text..."];
var faqTexts = ["Loading text..."];
var rainfallText = "Loading text...";
// These lists are used to keep track of which texts have already been displayed
var dischargeRateTextsUsed = [];
var gageHeightTextsUsed = [];
var faqTextsUsed = [];
var delay = 15000;
var display_rainfall = true;
// Figure out what text to display next
// dischargeRate: true if this text is for discharge rate, false if for gage height
function getText(text)
{
    var curTexts = gageHeightTexts;
    var curTextsUsed = gageHeightTextsUsed;
    if (text === textEnum.DISCHARGE_RATE)
    {
        curTexts = dischargeRateTexts;
        curTextsUsed = dischargeRateTextsUsed;
    }
    else if (text === textEnum.FAQ)
    {
        curTexts = faqTexts;
        curTextsUsed = faqTextsUsed;
    }
    var updated = false;
    if (curTexts.length === curTextsUsed.length)
    {
        // If we've already used all the available texts,
        // delete all the indexes and start over
        curTextsUsed.splice(0, curTextsUsed.length)
    }
    var curIndex = -1;
    while (!updated)
    {
        if(display_rainfall && text === textEnum.FAQ)
        {
            display_rainfall = false;
            return rainfallText;
        }
        else {
            curIndex = Math.floor(Math.random() * curTexts.length);
            var usedIndex = $.inArray(curIndex, curTextsUsed);
            if (usedIndex === -1) {
                curTextsUsed.push(curIndex);
                updated = true;
            }
            if(text === textEnum.FAQ) {
                display_rainfall = true;
            }
        }
    }
    return curTexts[curIndex];
}
// Fade out and fade in a div, change its text
function updateDiv(divID, text)
{
    $(divID).fadeOut('slow', function() {
        $(divID).html(text);
        setTimeout(function() { $(divID).fadeIn('slow'); }, 500);
    });
}

function changeTexts()
{
    function delayedCall()
    {
        // Calls changeTexts after delay
        setTimeout(changeTexts, delay)
    }
    updateDiv("#dischargeRateText", getText(textEnum.DISCHARGE_RATE));
    updateDiv("#gageHeightText", getText(textEnum.GAGE_HEIGHT));
    updateDiv("#faqText", getText(textEnum.FAQ));
    setTimeout(delayedCall, delay);
}
function updateTextLists()
{
    function delayedCall()
    {
        // Calls updateTextLists after delay of half an hour
        setTimeout(updateTextLists, 1800000)
    }
    $.getJSON(BASEURL.concat("/descriptor"), function(texts)
    {
        $.each(texts, function(key, val)
        {
            if(key === "discharge")
            {
                dischargeRateTexts = val;
            }
            else if(key === "faq")
            {
                faqTexts = val;
            }
            else if(key === "gage")
            {
                gageHeightTexts = val;
            }
            else if(key === "rainfall")
            {
                rainfallText = val[0];
            }
        });
    });
    setTimeout(delayedCall, 1800000);
}

function updateGraphs(days)
{
    function delayedCall()
    {
        // Calls updateGraphs after delay of half an hour
        setTimeout(updateGraphs, 1800000)
    }
    $.get(BASEURL.concat("/graph/GageHeight/".concat(String(days))), function(img)
    {
        $("#GageHeight").fadeOut(1000, function() {
            $("#GageHeight").attr("src","data:image/png;base64,".concat(img));
        }).fadeIn(500);
    });
    $.get(BASEURL.concat("/graph/DischargeRate/".concat(String(days))), function(img)
    {
        $("#DischargeRate").fadeOut(1000, function() {
            $("#DischargeRate").attr("src","data:image/png;base64,".concat(img));
        }).fadeIn(500);
    });
    setTimeout(delayedCall, 1800000)
}
updateGraphs(10);
updateTextLists();
setTimeout(changeTexts, 10000);