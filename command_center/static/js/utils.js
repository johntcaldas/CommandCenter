"use strict";

function ExpandableContentDiv() {

    var self = this;
    var m_clickDiv;
    var m_contentDiv;
    var m_headerDiv;
    var m_fullContentShowing = false;

    this.initialize = function (clickDiv, headerDiv, contentDiv) {
        m_clickDiv = clickDiv;
        m_contentDiv = contentDiv;
        m_headerDiv = headerDiv;

        m_contentDiv.hide();

        m_clickDiv.click(function() {
            self.toggleFullContentData()
        });
    };

    this.toggleFullContentData = function() {
        if(m_fullContentShowing) {
            m_contentDiv.hide(300);
            m_fullContentShowing = false;
        }
        else {
            m_contentDiv.show(300);

            // So the data table knows when to size itself.
            // TODO: this is specific to 'top' .. how to pull it out?
            setTimeout(function() {
                var table = $.fn.dataTable.fnTables(true);
                if ( table.length > 0 ) {
                    $(table).dataTable().fnAdjustColumnSizing();
                }
            }, 300);

            m_fullContentShowing = true;
        }
    };

    this.placeErrorMessageOnPage = function () {
        m_headerDiv.html("There was a problem loading the data.");
    };
}