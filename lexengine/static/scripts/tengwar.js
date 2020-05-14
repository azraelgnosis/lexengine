$(document).ready(function() {
    $("button").click(function() {
        let text = $('textarea#text').val();
        $.post(
            tengwar_url,
            {text},
            function(response) {
                $("textarea#tengwar").val(JSON.parse(response).transcribed);
            }
        );
    });
});