$(document).ready(function() {
    product_data = undefined;

    $("tbody").on("change", "tr [name$='product']", function(e) {
        value = $(this).val()
        if (value == ""){
            console.log("empty")
            $(this).parent().parent().find("[name$='normal_price']").val( parseFloat("0").toFixed(2))
            $(this).parent().parent().find("[name$='promo_price']").val( parseFloat("0").toFixed(2))
            console.log($(this).parent().parent().find("[name$='normal_price']").val())
            $("[name$='promo_price']").trigger("change")
            return;
        } else {
            console.log("not empty")
        }


        $.ajax({
        url: "/get_product_promo_prices/" + value + "/" +  $("[name='promo']").val() + "/" ,
        dataType: 'json',
        success: (data) => {
            $(this).parent().parent().find("[name$='normal_price']").val( parseFloat(data.current_price).toFixed(2))
            $(this).parent().parent().find("[name$='promo_price']").val( parseFloat(data.promo_price).toFixed(2))
            $("[name$='promo_price']").trigger("change")
        }
    });

    });


    $("[name='promo']").on("change", function(e) {
        value = $(this).val()
        $.ajax({
        url: "/get_promo_products/" + value + "/" ,
        dataType: 'json',
        success: function (data) {
            product_data = data;
            $("[name$='product']").each(function(i,selector ) {
                old_val = $(selector).find(":selected").val();
                $(selector).empty()
                out = $('<option value="">---------</option>');
                selector.append(out.get(0))
                $.each(data.products, function(i,e ) {
                    out = $('<option value=' + e.product__pk + ' >' + e.product__product_name + '</option>');
                    selector.append(out.get(0))
                });

                $(selector).val(old_val)
                $(selector).trigger("change")

            });
        }
    });
    });


    $("tbody").on("change","tr [name$='promo_price'],[name$='quantity']", function(e) {
        element = $(this)
        promo_price = element.parent().parent().find("[name$='promo_price']")
        normal_price = element.parent().parent().find("[name$='normal_price']")
        line_total = element.parent().parent().find("[name$='line_total']")
        line_discount = element.parent().parent().find("[name$='line_discount']")
        quantity = element.parent().parent().find("[name$='quantity']")
        line_total.val(promo_price.val() * quantity.val())
        line_discount.val((normal_price.val()-promo_price.val()) * quantity.val())

        line_total.trigger("change")
        line_discount.trigger("change")
    });

    $("tbody").on("change", "tr [name$='line_total']", function(e) {
        total = 0.0;
        discount = 0.0;
        $("[name$='line_total']").each(function(i,selector ) {
            total += parseFloat($(this).val())
        });
        $("[name$='line_discount']").each(function(i,selector ) {
            discount += parseFloat($(this).val())
        });
        $("[name='total_spent']").val(total.toFixed(2))
        $("[name='total_discount']").val(discount.toFixed(2))
    });

    $('#add-variant-button').on("add:row", function(e) {
        $("[name='promo']").trigger("change")
    });

    $("[name='promo']").trigger("change")
});