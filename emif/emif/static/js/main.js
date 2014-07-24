function showExportMessage(){
    $('#exporting-message').fadeIn('fast');


// Validation of quicksearch
$('#quicksearch').submit(function() {

        var quick_search = $('#edit-search-block-form--3', $(this)).val().trim();

        if(!quick_search || quick_search.length == 0)
            return false;

        return true;
});

    setTimeout(function() {
      $('#exporting-message').fadeOut('fast');  
    }, 4000);
}

$(function(){
    $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
    // Avoid following the href location when clicking
    event.preventDefault(); 
    // Avoid having the menu to close when clicking
    event.stopPropagation(); 
    // If a menu is already open we close it
    $('ul.dropdown-menu [data-toggle=dropdown]').parent().removeClass('open');
    // opening the one you clicked on
    $(this).parent().addClass('open');

    var menu = $(this).parent().find("ul");
    var menupos = $(menu).offset();

    if (menupos.left + menu.width() > $(window).width()) {
        var newpos = -$(menu).width();
        menu.css({ left: newpos });    
    } else {
        var newpos = $(this).parent().width();
        menu.css({ left: newpos });
    }

});    
})
