$(document).ready(function() {
    function transcribe() {
        let text = $('textarea#text').val();
        $.post(
            tengwar_url,
            {text},
            function(response) {
                $("textarea#tengwar").val(JSON.parse(response).transcribed);
            }
        );
    }

    $("textarea#text").keypress(function (e) {
        if (e.which == 13 && !e.shiftKey) {
            transcribe()
        }
    });

    $("button").click(function() {
        transcribe();
    });
});