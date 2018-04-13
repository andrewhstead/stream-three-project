$(function() {
  $("#default-form").submit(function() {
      var form = this;
      var card = {
        name:   $("#id_name_on_card").val(),
        number:   $("#id_card_number").val(),
        expMonth: $("#id_expiry_month").val(),
        expYear:  $("#id_expiry_year").val(),
        cvc:      $("#id_cvv").val()
      };

      $("#submit_order").attr("disabled", true);
       Stripe.createToken(card, function(status, response) {
        if (status === 200) {
          console.log(status, response);
          $("#credit-card-errors").hide();
          $("#id_stripe_id").val(response.id);
          form.submit();

        } else {
          $("#stripe-error-message").text(response.error.message);
          $("#credit-card-errors").show();
          $("#submit_order").attr("disabled", false);
        }
      });
      return false;
  });
});