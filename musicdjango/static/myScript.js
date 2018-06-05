$(function(){
    console.log('Ready');

    // side-bar open/close actions
    $('#openNav').on('click', function() {
          $(".main").css({'margin-left': '250px'});
          $(".leftNav").css({width: '250px'});
          $(this).css({display: 'none'});
          $('#closeNav').css({display: 'block'});
    });
    $('#closeNav').on('click', function() {
          $(".main").css({'margin-left': '0'});
          $(".leftNav").css({width: '0px'});
          $('#openNav').css({display: 'block'});
          $(this).css({display: 'none'});
    });

    // DatePicker
    $( "#id_release_date" ).datepicker();

    // Filters
    $("#song-filter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".table tr, ul.collection li").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    // initialize Album dropdown for songs - empty with '-------'
    $("<option value='' selected='selected'>Please select</option>").insertBefore($("#id_artist option:first"));
    $("<option value='' selected='selected'>Please select</option>").insertBefore($("#id_album option:first"));

    $('#id_artist').change (function() {
        url = $('#songForm').attr('data-albums-url')
        // url = 'ajax_load_albums';
        val =  $('#id_artist').find(":selected").text();
        request_url = url + '?id=' + val;
        console.log('url ', request_url);
        /* we can't refer to models here,
          so we go to views.py/song_create via ajax with specific url ('load_album' in urls.py),
          sending atrist name and getting all albums for this artist to show in the album select options */
        $.ajax({
            url: request_url,
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: {
                'artist': val
            },
            success: function (data) {
                console.log('data ', data)
                // remove all options before appending new ones
                $('#id_album').find('option').remove();
                $('#id_album + span').remove();
                if (!data.length) {
                     $('#id_album').after(
                         $('<span class="empty-err">First, please add album for this artist</span>') // show album is empty for this artist
                     );

                }
                $.each(data, function(index, text){
                    title = text.fields.title
                    console.log('val ', title, typeof(title), title.length)
                    $('#id_album').append(
                        // setting
                         $('<option></option>').val(index+1).html(title) // show album names in select based on selected artist
                     );
                });
            }
        })
        return false;
    });
});
