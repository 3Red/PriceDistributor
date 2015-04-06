function GetHashData() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var hashEnvelope = JSON.parse(xmlhttp.responseText);
            var marketObject = [];
            var keys = [];
            for (var key in hashEnvelope.HGETALL) {
                try{
                    SetupData(JSON.parse(hashEnvelope.HGETALL[key]), key);
                    keys.push(key);
                } catch (err) { }
            }
            ExpireData(keys);
            setTimeout(GetData, speed);
        }
    }

    xmlhttp.open("GET", "/HGETALL/stocks.json", true);
    xmlhttp.send();
}