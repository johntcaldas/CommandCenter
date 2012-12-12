function Top() {

    var self = this;

    var m_topClickDiv;
    var m_topFullDiv;
    var m_topHeaderDiv;

    var m_topTable;
    var m_topData = [];
    var m_expandableContentDivUtil;


    this.initialize = function () {
        m_topClickDiv = $('#topClickableDiv');
        m_topFullDiv = $('#topDataFull');
        m_topHeaderDiv = $('#topDataHeader');
        m_topTable = $('#topTable');

        self.getTopData();

        m_expandableContentDivUtil = new ExpandableContentDiv();
        m_expandableContentDivUtil.initialize(m_topClickDiv, m_topHeaderDiv, m_topFullDiv);
    };


    this.getTopData = function() {
        $.getJSON($SCRIPT_ROOT + '/system/top',
            function(data) {
                m_topData = data;

                if(m_topData['success']) {
                    self.placeTopDataOnPage();
                }
                else {
                    m_expandableContentDivUtil.placeErrorMessageOnPage();
                }
            });
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
            "aoColumns": columns,
            "bPaginate": false,
            "sScrollY": "30em",
            "bJQueryUI": true,
            "aoColumnDefs": [
                { "sWidth": "20%", "aTargets": [ -1 ] }
            ]
        });
    };
}


$(document).ready(function() {
    var top = new Top();
    top.initialize();
});
