
function myTinkerClassThingy() {

    var self = this;

    this.initialize = function() {
        var sensorDiv = $("#sensorData");
        sensorDiv.click(function() {
           self.getSensorData()
        });

        //this.getSensorData(sensorDiv)
    };

    this.getSensorData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/sensors', {
            a: "I am parameter a yo",
            b: "I am parameter b yo"
        }, function(data) {
            $("#sensorData").text(data.result[0]);
        });
    };
}

$(document).ready(function() {
    g_handler = new myTinkerClassThingy();
    g_handler.initialize();
});
