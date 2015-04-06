var previous_response_length = 0;
var previous_partial = undefined;

function GetSubData() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 3) {
            if (previous_response_length != 0) {
                var resp = xmlhttp.responseText.slice(previous_response_length);

                if (previous_partial != undefined) {
                    resp = previous_partial + resp;
                    previous_partial = undefined;
                }

                var idx = -1;
                do {
                    idx = resp.indexOf("}{");
                    if (idx == -1) {
                       

                        if (resp.charAt(resp.length - 1) == "}") {  //is this a full message
                            try{
                                var pubEnvelope = JSON.parse(resp);
                            }
                            catch (err)
                            {
                                idx = -1;
                            }

                        }
                        else {
                            previous_partial = resp;
                        }
                    }
                    else {
                        try{
                            var pubEnvelope = JSON.parse(resp.slice(0, idx + 1));
                            resp = resp.slice(idx + 1, resp.length);
                        }
                        catch (err) {
                            idx = -1;
                        }
                    }
                    if (pubEnvelope != undefined) {
                        var marketObject = JSON.parse(pubEnvelope.SUBSCRIBE[2]);
                        SetupData(marketObject);
                    }

                } while (idx != -1)
            }
            previous_response_length = xmlhttp.responseText.length;
        }
    }
    xmlhttp.timeout = 1000;
    xmlhttp.ontimeout = function () {
        xmlhttp.abort();
        GetData();
    };
    xmlhttp.open("GET", "/SUBSCRIBE/stocks.json", true);
    xmlhttp.send();
}
