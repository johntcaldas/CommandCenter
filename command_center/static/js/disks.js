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
        var diskHeaderHtml = "Disks: " + '<span class="green">' + m_diskData['num_disks'] + '</span>';
        diskHeaderHtml += ", RAID Arrays: " + '<span class="green">' + m_diskData['num_raid_arrays'] + '</span>';
        m_diskHeaderDiv.html(diskHeaderHtml);

        SortJsonArrayByProperty(m_diskData['disk_data'], 'device_name', 1);

        d3.select("#diskList")
            .selectAll("div")
            .data(m_diskData['disk_data'])
            .enter()
            .append("div")
            .attr("class", "diskLineItem")
            .html(function (d) {

                // TODO: refactor the crap out of this.
                // TODO: show multiple partitions.

                var html = '<div class="diskLineItemLeft">';
                html += d.device_name + " " + d.human_size;
                html += '</div>';

                html += '<div class="diskLineItemRight">'
                if(d.rotational_media.indexOf('Yes') !== -1) {
                    if(d.device_name.indexOf('md') !== -1) {
                        html += "RAID";
                    }
                    else {
                        html += "HD";
                    }
                }
                else {
                    html += "SSD";
                }
                html += '</div>';

                html += '<div class="clear"></div>';


                var raid = false;
                if(d.usage === "raid") {
                    raid = true;
                }

                // Get usage percentage from first mounted partition.
                var mountedPartition = null;
                if(d.partitions != undefined) {
                    for(var i = 0; i < d.partitions.length; i++) {
                        if (d.partitions[i].is_mounted) {
                            mountedPartition = d.partitions[i];
                            break;
                        }
                    }
                }


                html += '<div class="diskBar">';


                html += '<div class="diskBarLabel">';
                if(raid) html += "RAID";
                else html += mountedPartition.used_percent;
                html += '</div>';

                var width = "0%";
                if(mountedPartition !== null) {
                    width = mountedPartition.used_percent;
                    html += '<div class="diskBarUsage" style="width: ' + width + '"></div>';
                }
                else if(raid) {
                    html += '<div class="diskBarRaid"></div>';
                }

                html += '</div>';
                return html;
            });
    };
}


$(document).ready(function() {
    var disks = new Disks();
    disks.initialize();
});

