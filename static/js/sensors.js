
function Home() {

    var self = this;

    var m_sensorClickDiv = null;
    var m_sensorHeaderDiv = null;
    var m_sensorFullDiv = null;

    var m_sensorData = [];
    var m_expandableContentDivUtil;


    this.initialize = function() {
        m_sensorClickDiv = $("#sensorsClickableDiv");
        m_sensorHeaderDiv = $("#sensorDataHeader");
        m_sensorFullDiv = $('#sensorDataFull');

        self.getSensorData();

        m_expandableContentDivUtil = new ExpandableContentDiv();
        m_expandableContentDivUtil.initialize(m_sensorClickDiv, m_sensorHeaderDiv, m_sensorFullDiv);
    };


    this.getSensorData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/sensors', {
            a: "I am parameter a yo",
            b: "I am parameter b yo"
        },
        function(data) {
            m_sensorData = data;
            if(m_sensorData['success']) {
                self.placeSensorDataOnPage();
            }
            else {
                m_expandableContentDivUtil.placeErrorMessageOnPage();
            }
        });
    };


    this.placeSensorDataOnPage = function() {

        var cpu_temp = m_sensorData['cpu_temp'];
        var mb_temp = m_sensorData['mb_temp'];
        var vid_temp = m_sensorData['vid_temp'];

        // If these come back empty (ie. server could not find them in 'sensors' output) then use '??'
        if(cpu_temp === '') cpu_temp = '??';
        if(mb_temp === '') mb_temp = '??';
        if(vid_temp === '') vid_temp = '??';

        // Create the clickable header.
        m_sensorHeaderDiv.html("cpu: " + "<span class=green>" + cpu_temp + "</span> | " +
            " mb: " + "<span class=green>" + mb_temp + "</span> | " +
            " vid: " + "<span class=green>" + vid_temp + "</span>");


        // Create the div the expands and appears when you click the header.
        var sensors_by_line = m_sensorData['sensors_by_line'];
        var tableHTML = "<table>";

        // This is a hack, but we're leaving off the last line so that the table looks better.
        // At the time of this writing the last line is : (crit = +90.0°C, hyst = +88.0°C)
        for(var i = 0; i < sensors_by_line.length - 2; i++) {
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
    };
}


$(document).ready(function() {
    var sensors = new Home();
    sensors.initialize();
});
