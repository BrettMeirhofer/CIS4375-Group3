$(document).ready(function() {
    // Controls replacing select widgets with select2 widgets
    $('.js-example-basic-single').select2();

        // Controls money formatting
      $('tbody').on("change", "tr .money", function(ev) {
        ev.target.value = parseFloat(ev.target.value).toFixed(2);
      });

      $('.money').on("change", function(ev) {
        ev.target.value = parseFloat(ev.target.value).toFixed(2);
      });

      $('.money').each(function(i,e ) {
        console.log("Test")
        e.value = parseFloat(e.value).toFixed(2);
      });


    // Controls phone number formatting
        $('.phone').on('input', function() {
      let text=$(this).val()
      text=text.replace(/\D/g,'')
      if(text.length>3) text=text.replace(/.{3}/,'$&-')
      if(text.length>7) text=text.replace(/.{7}/,'$&-')
      $(this).val(text);
    });

    $('.phone').each(function() {
      let text=$(this).val()
      text=text.replace(/\D/g,'')
      if(text.length>3) text=text.replace(/.{3}/,'$&-')
      if(text.length>7) text=text.replace(/.{7}/,'$&-')
      $(this).val(text);
    });
    // Controls primary image checkboxes
    $("tbody").on("change", "tr [name$='primary_image']", function(e) {
        target_element = $(this)
        if (target_element.is(':checked')){
        $("[name$='primary_image']").each (function() {
            console.log($(this))
            console.log($(target_element))
            if (!$(this).is(target_element)){
                $(this).prop( "checked", false );
            }
        });
        }

    });


    // Controls creating img widget for preview widgets
    $('tbody').on("change", "tr td input[type=url]", function() {
        console.log("Changed")
        $(this).parent().find("img").attr("src", $(this).val())
        $(this).css("display", "inline-block")
    });

    $('td input[type=url]').each(function() {
        $(this).parent().append("<img class='img-preview' style='height:50px;width:50px;display:inline-block;vertical-align: middle' src="+ $(this).val() +"></img>")
        $(this).css("display", "inline-block")
    });
    $('#add-variant-button').on("add:row", function(e) {
        $(".img-preview").remove();
        $('td input[type=url]').each(function() {
            $(this).parent().append("<img class='img-preview' style='height:50px;width:50px;display:inline-block;vertical-align: middle' src="+ $(this).val() +"></img>")
            $(this).css("display", "inline-block")
    });
    });
});