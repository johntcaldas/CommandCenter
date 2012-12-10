
function Home() {

    var self = this;
    var m_sensorContainerDiv = null;
    var m_sensorHeaderDiv = null;
    var m_sensorFullDiv = null;
    var m_sensorData = [];
    var m_fullDataShowing = false;

    this.initialize = function() {
        m_sensorContainerDiv = $("#sensorData");
        m_sensorHeaderDiv = $("#sensorDataHeader");
        m_sensorFullDiv = $('#sensorDataFull');

        m_sensorContainerDiv.click(function() {
           self.toggleFullSensorData()
        });

        m_sensorFullDiv.hide();

        this.getSensorData();
    };


    this.getSensorData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/sensors', {
            a: "I am parameter a yo",
            b: "I am parameter b yo"
        },
        function(data) {
            m_sensorData = data;
            m_sensorHeaderDiv.text("CPU: " + m_sensorData['cpu_temp'] +
                                   " MB: " + m_sensorData['mb_temp'] +
                                   " VID: " + m_sensorData['vid_temp']);

            var sensors_by_line = m_sensorData['sensors_by_line'];
            var tableHTML = "<table>";
            for(var i = 0; i < sensors_by_line.length; i++) {
                var currLine = sensors_by_line[i];

                tableHTML += "<tr>";

                var pattern = /.*\b:/;
                var regex = new RegExp(pattern);
                var match = regex.exec(currLine);

                if(match !== null) {
                    tableHTML += "<td>" + match + "</td>";

                    pattern = /\b:(.*)/;
                    regex = new RegExp(pattern);
                    match = regex.exec(currLine);
                    if(match !== null) {
                        tableHTML += "<td>" + match[1] + "</td>";
                    }
                }
                else {
                    tableHTML += "<td>" + currLine + "</td>"
                    tableHTML += "<td>&nbsp;</td>"
                }

                tableHTML += "</tr>";
            }
            tableHTML += "</table>";

            m_sensorFullDiv.html(tableHTML);

        });
    };


    this.toggleFullSensorData = function () {
        if(m_fullDataShowing) {
            m_sensorFullDiv.hide();
            m_fullDataShowing = false;
        }
        else {
            m_sensorFullDiv.show();
            m_fullDataShowing = true;
        }
    };
}


$(document).ready(function() {
    var home = new Home();
    home.initialize();
});
