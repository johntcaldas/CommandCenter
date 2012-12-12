function Top() {

    var self = this;
    var m_topClickDiv;
    var m_topFullDiv;
    var m_topHeaderDiv;
    var m_topTable;
    var m_topData = [];
    var m_fullDataShowing = false;

    this.initialize = function () {

        m_topClickDiv = $('#topClickableDiv');
        m_topFullDiv = $('#topDataFull');
        m_topHeaderDiv = $('#topDataHeader');
        m_topTable = $('#topTable');

        m_topClickDiv.click(function() {
            self.toggleFullTopData()
        });

        m_topFullDiv.hide();

        self.getTopData();
    };

    this.getTopData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/top',
            function(data) {
                m_topData = data;

                if(m_topData['success']) {
                    self.placeTopDataOnPage();
                }
                else {
                    self.placeErrorMessageOnPage();
                }
            });
    };

    this.toggleFullTopData = function() {
        if(m_fullDataShowing) {
            m_topFullDiv.hide(300);
            m_fullDataShowing = false;
        }
        else {
            m_topFullDiv.show(300);
            m_fullDataShowing = true;
        }
    };

    this.placeTopDataOnPage = function () {
        m_topHeaderDiv.html(m_topData['first_line']);

        var columns = [];
        var column_names = m_topData['column_names'];
        for(var i = 0; i < column_names.length; i++) {
            columns[i] = {};
            columns[i]['sTitle'] = column_names[i];
        }

        m_topTable.dataTable({
            "aaData":m_topData['rows'],
            "aoColumns": columns
        });
    };

    this.placeErrorMessageOnPage = function () {

    };
}

$(document).ready(function() {
    var top = new Top();
    top.initialize();
});
