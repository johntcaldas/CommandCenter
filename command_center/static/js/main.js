function Main() {

    var self = this;
    var m_nav_list_items = null;
    var m_footer = null;
    var m_date = '';

    this.initialize = function () {
        m_nav_list_items = $('#topnav li');
        m_footer = $('#footer');
        self.setupTabbedNavigation();
        self.getDate();
    };

    this.setupTabbedNavigation = function() {
        // First set click handlers on the list elements.
        m_nav_list_items.each(function(index) {
           $(this).click(function(){
               self.tabClick(this);
           });
        });

        // Then set the first to selected.
        m_nav_list_items.find('li:first').addClass('navTabSelected');
    };

    this.tabClick = function(tab) {
        // First set all tabs to not selected
        m_nav_list_items.each(function(index) {
           $(this).removeClass('navTabSelected');
        });

        // Then select 'this' tab
        tab.addClass('navTabSelected');
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