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
        m_nav_list_items.filter(':first').addClass('navTabSelected');
    };

    this.tabClick = function(tab) {

        // TODO: there's got to be a smarter way to do this without the redundant switch statements
        // preferably dynamically, where we just strip out the 'li_' from the li's to get the corresponding
        // div id.

        // First set all tabs to not selected
        m_nav_list_items.each(function(index) {
            if(this !== tab) {
                $(this).removeClass('navTabSelected');
                var currId = $(this).attr('id');

                switch(currId) {
                    case "li_home":
                        $('#home').addClass("invisible");
                        break;
                    case "li_disks":
                        $('#disks').addClass("invisible");
                        break;
                    case "li_about":
                        $('#about').addClass("invisible");
                        break;
                    default:
                        break;
                }
            }
        });

        // Then select 'this' tab
        $(tab).addClass('navTabSelected');
        var selectedId = $(tab).attr('id');

        switch(selectedId) {
            case "li_home":
                $('#home').removeClass("invisible");
                break;
            case "li_disks":
                $('#disks').removeClass("invisible");
                break;
            case "li_about":
                $('#about').removeClass("invisible");
                break;
            default:
                break;
        }
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