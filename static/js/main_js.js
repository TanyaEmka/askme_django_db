base_ajax_url = '/ajax_urls/';
$('.vote').on('click', function (e) {
    let elem = e.target;
    if (elem !== this) {
        elem = elem.parentNode;
    }
    console.log("CLICK ON LIKE BUTTON")
    let object = elem.getAttribute('data-object');
    let action = elem.getAttribute('data-action');
    let user_id = elem.getAttribute('data-user');
    let object_id = elem.getAttribute('data-id');
    let datastring = {'object': object, 'action': action, 'user_id': user_id, 'object_id': object_id};
    $.ajax({
            url: base_ajax_url + "vote/",
            type: 'POST',
            data: datastring,
            success: function (response) {
                $('#vote'+object_id).html(response);
            }
        }
    );
});