
    $(document).ready(function() {
      delete_rows = [];
      $('.select-row').change(function(ev) {
        id = parseInt($(ev.target).attr("rowid"))
        if (ev.target.checked){
            delete_rows.push(id)
        } else {
            delete_rows = delete_rows.filter(function(e) { return e !== id })
        }
        console.log(delete_rows)
      });
      $('.selectall').change(function(ev) {
        state = ev.target.checked
        $('.select-row').each(function(i,e ) {
            id = parseInt($(e).attr("rowid"))
            e.checked = state;
            if (state){
                delete_rows.push(id)
            } else {
                delete_rows = delete_rows.filter(function(e) { return e !== id })
            }
        });
        console.log(delete_rows)
      });
      $('.deletebutton').change(function(ev) {
        console.log("Success")
          $.post({
            url: {% url 'delete_rows' %},
            data: JSON.stringify({ "rows": delete_rows }),
            success: function (data) {
                console.log("Success")
            }
          });
          });
  });