
function GetKeys() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var marketObject = JSON.parse(xmlhttp.responseText);
            GetStringData(marketObject.KEYS);
            ExpireData(marketObject.KEYS);
        }
    }

    xmlhttp.open("GET", "/KEYS/stocks:*", true);
    xmlhttp.send();
}

function GetStringData(keys) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var keyEnvelope = JSON.parse(xmlhttp.responseText);
            if (keyEnvelope.MGET != undefined && keyEnvelope.MGET[0] != false) {
                for (var i = 0; i < keyEnvelope.MGET.length; i++) {
                    try{
                        var marketObject = JSON.parse(keyEnvelope.MGET[i]);
                        SetupData(marketObject, keys[i]);
                    }catch(err){}
                }
            }
            setTimeout(GetData, speed);
        }
    }

    var url = "/MGET";
    for (var i = 0; i < keys.length; i++) {
        url += "/" + keys[i];
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}
