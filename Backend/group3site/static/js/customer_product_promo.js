$(document).ready(function() {
    $("[name$='product']").empty()
    $("[name$='product']").on("change", function(e) {
        console.log("Changed")
        value = $(this).val()
        element = $(this)
        $.ajax({
        url: "/get_product_promo_prices/" + value + "/" +  $("[name='promo']").val() + "/" ,
        dataType: 'json',
        success: function (data) {
            element.parent().parent().find("[name$='normal_price']").val( parseFloat(data.current_price).toFixed(2))
            element.parent().parent().find("[name$='promo_price']").val( parseFloat(data.promo_price).toFixed(2))
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
            console.log(data)
            $("[name$='product']").empty()
            $("[name$='product']").each(function(i,selector ) {
                $.each(data.products, function(i,e ) {
                    out = $('<option value=' + e.product__pk + ' >' + e.product__product_name + '</option>');
                    selector.append(out.get(0))
                });
            });
            $("[name$='product']").trigger("change")
        }
    });
    });

    $("[name$='promo_price'],[name$='quantity']").on("change", function(e) {
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

    $("[name$='line_total']").on("change", function(e) {
        total = 0;
        $("[name$='line_total']").each(function(i,selector ) {
            total += $(this).val()
        });
        $("[name='total_spent']").val(total)
    });

    $("[name='promo']").trigger("change")
});