
function Home() {

    var self = this;
    var m_sensorData = [];
    var m_fullDataShowing = false;

    this.initialize = function() {
        var sensorDiv = $("#sensorData");
        sensorDiv.click(function() {
           self.toggleFullSensorData()
        });

        //this.getSensorData(sensorDiv)
    };


    this.getSensorData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/sensors', {
            a: "I am parameter a yo",
            b: "I am parameter b yo"
        }, function(data) {
            m_sensorData = data;
            self.showAbridgedSensorData()
        });
    };


    this.toggleFullSensorData = function () {
        if(m_fullDataShowing) {
            self.showAbridgedSensorData();
            m_fullDataShowing = false;
        }
        else {
            self.showFullSensorData();
            m_fullDataShowing = true;
        }
    };


    this.showAbridgedSensorData = function() {
        $("#sensorData").text("CPU: " + m_sensorData['cpu_temp'] +
                              " MB: " + m_sensorData['mb_temp'] +
                              " VID: " + m_sensorData['vid_temp']);
    };


    this.showFullSensorData = function() {
        $('#sensorData').text("Full YO")
    };
}


$(document).ready(function() {
    var home = new Home();
    home.initialize();
    home.getSensorData();
});
