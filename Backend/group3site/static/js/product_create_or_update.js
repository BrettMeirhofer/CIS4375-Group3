$(document).ready(function() {
    $('.js-example-basic-single').select2();
      $('tbody').on("change", "tr .money", function(ev) {
        ev.target.value = parseFloat(ev.target.value).toFixed(2);
      });

      $('.money').each(function(i,e ) {
        e.value = parseFloat(e.value).toFixed(2);
      });

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

    $('td input[type=url]').change(function() {
        $(this).parent().find("img").attr("src", $(this).val())
        $(this).css("display", "inline-block")
    });

    $('td input[type=url]').each(function() {
        $(this).parent().append("<img style='height:50px;width:50px;display:inline-block;vertical-align: middle' src="+ $(this).val() +"></img>")
        $(this).css("display", "inline-block")
    });
});