(function($) {

    $('#tweets li a').click(function(e){
        e.preventDefault();
        $(this).find('.main').toggle();
        $(this).find('.data').toggle();
    });

})(jQuery);