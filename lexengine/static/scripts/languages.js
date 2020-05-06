$(document).ready(function() {
    $('body').on('keypress', 'input', function(event) {
        if (event.which == '13') {
            $(this).focusout();
        }
    });

    $('tr').on('click', 'td[id]', function() {
        let td = $(this);
        let text = td.text();
        let id = td.attr('id');
        let name = td.attr('name');
        if (!td.children().length > 0) {
            td.html(
                `<input id=${id} name="${name}" value="${text}"></input>`
            );
            let input = td.children();
            if (input.attr('name') == 'eng_name') {
                input.prop('required', true);
            }
        };
        td.children()[0].focus();
    });

    $('tr').on('focusout', 'td[id] > input', function(event) {
        let id = $(this).attr('id');
        let val = $(this).val();
        let col = $(this).attr('name');
        $.post(language_edit_url, {id, val, col});

        $(this).replaceWith(val);

    });

    $("button[value='Delete']").click(function() {
        let id = $(this).attr('id');
        $.post(language_delete_url, {id});
    });
});