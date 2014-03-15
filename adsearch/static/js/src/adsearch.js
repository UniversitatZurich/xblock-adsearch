function AdSearchBlock(runtime, element) {
    function searchQuery(data) {
        $('.results', element).attr('src','http://www.bing.com/search?q='+encodeURIComponent(data.query));
        $('.results', element).show();
    }

    var handlerUrl = runtime.handlerUrl(element, 'search');

    $('.search', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({query: $('.query', element).val()}),
            success: searchQuery
        });
    });

};
