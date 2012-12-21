function Main() {

    var self = this;
    var m_footer = null;
    var m_date = '';

    this.initialize = function () {

        m_footer = $('#footer');

        self.getDate();
    };

    this.getDate = function() {
        $.getJSON($SCRIPT_ROOT + '/system/date',
            function(data) {
                m_date= data['date'];
                m_footer.text(m_date);
            });
    };
}

$(document).ready(function() {
    var home = new Main();
    home.initialize();
});