"use strict";

function Disks() {

    var self = this;

    var m_diskClickDiv = null;
    var m_diskHeaderDiv = null;
    var m_diskFullDiv = null;

    var m_diskData = [];
    var m_expandableContentDivUtil;

    var m_currentlyShowingDiskDetailsDiv = null;

    this.initialize = function() {
        m_diskClickDiv = $("#disksClickableDiv");
        m_diskHeaderDiv = $("#diskDataHeader");
        m_diskFullDiv = $('#diskDataFull');

        self.getSensorData();

        m_expandableContentDivUtil = new ExpandableContentDiv();
        m_expandableContentDivUtil.initialize(m_diskClickDiv, m_diskHeaderDiv, m_diskFullDiv);
    };


    this.getSensorData = function() {
        $.getJSON(SCRIPT_ROOT + '/system/disks',
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
        // Sort the disks by device name (ie. sda, sdb, ...)
        SortJsonArrayByProperty(m_diskData['disk_data'], 'device_name', 1);

        // Create the header at the top of the disk section
        var diskHeaderHtml = "Disks: " + '<span class="green">' + m_diskData['num_disks'] + '</span>';
        diskHeaderHtml += ", RAID Arrays: " + '<span class="green">' + m_diskData['num_raid_arrays'] + '</span>';
        m_diskHeaderDiv.html(diskHeaderHtml);

        // Place the disk summary blocks on the left side of disk section.
        d3.select("#diskList")
            .selectAll("div")
            .data(m_diskData['disk_data'])
            .enter()
            .append("div")
            .attr("class", "diskLineItem clickable")
            .html(function (d) {
                return self.createDiskSummaryDiv(d);
            });

        // Attach the click event for disk summary blocks.
        d3.select("#diskList")
            .selectAll(".diskLineItem").on("click", (function (d) {
               self.switchVisibleDiskDetailsPanel(d, $(this));
            }));

        // Create disk detail divs.
        d3.select("#diskDetails")
            .selectAll("div")
            .data(m_diskData['disk_data'])
            .enter()
            .append("div")
            .attr("class", "diskDetailsPanel invisible")
            .html(function (d) {
                return self.createDiskDetailsDiv(d);
            });
    };

    /**
     *  Creates HTML to display a disk summary block.
     * @param disk       -- JSON data of the disk.
     * @return {string}  -- HTML for the disk summary block.
     */
    this.createDiskSummaryDiv = function(disk) {
        // TODO: refactor the crap out of this.
        // TODO: show multiple partitions.

        //**************************************************************************************************************
        // Part 1: Determine a few of the characteristics of the device we are about to display.                       *
        //**************************************************************************************************************

        // Determine if this device is best characterized as
        // "HD"   -- a regular hard disk.
        // "RAID" -- a linux software raid virtual device.
        // "SSD"  -- a solid state drive.
        var deviceType = "SSD";
        if(isSSD(disk)) {
            if(isRaidDevice(disk)) {
                deviceType = "RAID";
            }
            else {
                deviceType = "HD";
            }
        }

        // Get usage percentage from first mounted partition. For now we are only showing "usage percentage" information
        // for the first partition we find. Later we'll want to be smart and extend this to show information about all
        // partitions if possible.
        var mountedPartition = null;
        if(disk.partitions != undefined) {
            for(var i = 0; i < disk.partitions.length; i++) {
                if (disk.partitions[i].is_mounted) {
                    mountedPartition = disk.partitions[i];
                    break;
                }
            }
        }


        //**************************************************************************************************************
        // Part 2: Build the html for this device's summary block.                                                     *
        //**************************************************************************************************************

        // Create the header.
        var html = '<div class="diskLineItemLeft">';
        html += disk.device_name + " " + disk.human_size;
        html += '</div>';
        html += '<div class="diskLineItemRight">' + deviceType + '</div>';
        html += '<div class="clear"></div>';

        // Figure out the text, width, and class for the percentage bar.
        var percentageText = "No Mounted Partition";
        var width = "100%";
        var percentageClass = "diskBarUsage";
        if(disk.usage === "raid") {
            percentageText = "RAID";
            percentageClass = "diskBarRaid";
        }
        else if (mountedPartition !== null){
            width = mountedPartition.used_percent;
            percentageText = width;
        }

        // Create the usage percentage bar.
        html += '<div class="diskBar">';
        html += '<div class="diskBarLabel">' + percentageText + '</div>';
        html += '<div class="' + percentageClass + '" style="width: ' + width + '"></div>';
        html += '</div>';


        return html;
    };

    /**
     * Switches the visible "disk details panel".
     *
     * This is the click event for a disk summary item.
     * @param diskData       - The JSON data for the clicked-on disk.
     * @param diskSummaryDiv - jquery object of the clicked-on disk summary div
     */
    this.switchVisibleDiskDetailsPanel = function(diskData, diskSummaryDiv) {
        if(m_currentlyShowingDiskDetailsDiv !== null) {
            m_currentlyShowingDiskDetailsDiv.addClass('invisible');
        }

        d3.selectAll(".diskDetailsPanel").each(function(d, i) {
            if(d.device_file == diskData.device_file) {
                $(this).removeClass('invisible');
                m_currentlyShowingDiskDetailsDiv = $(this);
            }
        });
    };

    /**
     * Creates HTML to display a disk details block.
     * @param disk      -- JSON data of the disk.
     * @return {string} -- HTML for the disk details block.
     */
    this.createDiskDetailsDiv = function(disk) {

        var device_file = disk['device_file'];
        var serial = disk['serial'];
        var human_size = disk['human_size'];
        var revision = disk['revision'];
        var interface_bus = disk['interface'];
        var is_raid_member = disk['is_raid_member'];
        var rotational_media = disk['rotational_media'];
        var can_spindown = disk['can_spindown'];
        var native_path = disk['native_path'];
        var raid_info = disk['raid_info'];
        var usage = disk['usage'];
        var if_speed = disk['if_speed'];

        var html = '<div class="deviceDetailsLeft">' +
            device_file + "<br>" +
            "Size: " + human_size + "<br>" +
            "Serial Number: " + serial + "<br>" +
            "Revision: " + revision + "<br>" +
            "Interface: " + interface_bus + "<br>" +
            "Is Raid Member: " + is_raid_member + "<br>" +
            "Is Rotational Media: " + rotational_media + "<br>" +
            "Can Spindown: " + can_spindown + "<br>" +
            '</div>'
        return html;
    };
}


$(document).ready(function() {
    var disks = new Disks();
    disks.initialize();
});

