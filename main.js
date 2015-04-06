var stockTable;
var tableLookup = {};
var lastType = "";
var speed = 1000;

window.onload = function () {
    stockTable = document.getElementById("stockTable");
    GetData();
};

function GetData() {
    speed = 5000 - parseFloat( document.getElementById("speedRange").value );
    if (document.getElementById("subRad").checked == true) {
        if (lastType != "sub") {
            ClearData();
            lastType = "sub";
        }
        GetSubData();
    }
    else if (document.getElementById("stringRad").checked == true) {
        if (lastType != "string") {
            ClearData();
            lastType = "string";
        }
        GetKeys();
    }
    else {
        if (lastType != "hash") {
            ClearData();
            lastType = "hash";
        }
        GetHashData();
    }
}

function ClearData() {
    while (stockTable.rows.length > 1) {
        stockTable.deleteRow(1);
    }
    tableLookup = {}
}

function SetupData(marketObject, key) {
    var rowKey = key;
    if (rowKey == undefined) {
        rowKey = marketObject.symbol;
    }

    var newRow = tableLookup[rowKey];

    if (newRow == undefined) {
        var newRow = stockTable.insertRow(1);
        tableLookup[rowKey] = newRow;
        newRow.insertCell(0);
        newRow.insertCell(1);
        newRow.insertCell(2);
        newRow.insertCell(3);
        newRow.insertCell(4);
    }

    var symCell = newRow.cells[0];

    var bidQCell = newRow.cells[1];
    var bidCell = newRow.cells[2];
    var askCell = newRow.cells[3];
    var askQCell = newRow.cells[4];
    symCell.innerHTML = marketObject.symbol;
    symCell.className = "rowHeader";
    bidCell.innerHTML = marketObject.bid;
    askCell.innerHTML = marketObject.offer;
    bidQCell.innerHTML = marketObject.bid_depth;
    askQCell.innerHTML = marketObject.offer_depth;
}

function ExpireData(keys) {
    for (var symbol in tableLookup) {
        if (keys.indexOf(symbol) == -1) {
            tableLookup[symbol].cells[0].className = 'expired';
        }
    }
}