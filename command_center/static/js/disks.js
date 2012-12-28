"use strict";

function Disks() {

    var self = this;

    var m_diskClickDiv = null;
    var m_diskHeaderDiv = null;
    var m_diskFullDiv = null;

    var m_diskData = [];
    var m_expandableContentDivUtil;

    this.initialize = function() {
        m_diskClickDiv = $("#disksClickableDiv");
        m_diskHeaderDiv = $("#diskDataHeader");
        m_diskFullDiv = $('#diskDataFull');

        self.getSensorData();

        m_expandableContentDivUtil = new ExpandableContentDiv();
        m_expandableContentDivUtil.initialize(m_diskClickDiv, m_diskHeaderDiv, m_diskFullDiv);
    };


    this.getSensorData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/disks',
            function(data) {
                m_diskData = data;
                if(m_diskData['success']) {
                    self.placeDiskDataOnPage();
                }
                else {
                    // Handle error
                }
            });
    };

    this.placeDiskDataOnPage = function() {
        d3.select("#diskDataFull")
            .append("ul")
            .selectAll("li")
            .data(m_diskData['disks'])
            .enter()
            .append("li")
            .text(function (d) {
                return d.partition_table + ": " + d.bus;
            });
    };
}


$(document).ready(function() {
    var disks = new Disks();
    disks.initialize();
});

