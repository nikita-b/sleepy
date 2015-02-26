$('.datepicker').pickadate({
    hiddenName: true,
    max: true
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(function () {
  $('[data-toggle="popover"]').popover()
})

moment.locale('ru')



$(".interpretation").click(function() {
  $(".field-interpretation").toggle("slow");
});

$('.description-field').popover('show')


$(function(){
  $('.postrow').hover(function(){
    $('.more-dream:only-child').addClass('more-dream-show');
  }, function(){
    $('.more-dream').removeClass('more-dream-show');
  })
});