$(document).ready(function() {

    console.log('Preparing to correct user text')
    
    $('#loading').hide()

    $('#text_gen_button').click(function() {
        console.log('text gen button is clicked');
        var prompt = $('#text_gen_input').val();
        console.log('text gen input value is');
        console.log(prompt);
        var url = 'generate_text'

        $('#loading').show();

        $.post(
            url, 
            {
                'prompt': prompt
            },
            function(data) {
                console.log(data);
                var list_html = ""; 
                console.log(list_html);
                for (const [key, value] of Object.entries(data['generated_ls'])) {
                    var original_sentence = key;
                    var corrected_sentence = value[0];
                    var edits = value[1];
                    if (edits.length < 1) {
                        var starting_text = "<li>" + "There are no needed changes for the following: " + original_sentence + "</li>";
                    }
                    else {
                        var starting_text = "<li>" + "There are " + edits.length.toString()  + " suggested corrections to improve <em> \" " + original_sentence + "\"</em> to the following: <em> \"" + corrected_sentence + "\"</em>" + "<ol>";


                        for (let t = edits.length-1; t >= 0; t--){
                            starting_text += "<li> Change \"" + edits[t][1] + "\" to \"" + edits[t][4] + "\" ( " + edits[t][0] + " ) </li>";
                        }

  
                        starting_text += "</ol></li>";



                    }
                    // var starting_text = "<li id='generated_item_" + t + "'>" + data['generated_ls'][t] + "</li>";
                    list_html += starting_text
                    $("#generated_ul").html(list_html);
                }
                console.log(list_html);

                $("#loading").hide();
            }

        ).fail(function() {
          alert( "Something unexpected happened. Email ryanpapetti@gmail.com to report your findings." );
        });

    });

    $()
});