/**
 * Created by micha on 8/24/17.
 */
$(function() {
    var DialogElements = jQuery(".ms-Dialog");
    var DialogComponents = [];

    for (var i = 0; i < DialogElements.length; i++) {
      (function() {
        DialogComponents[i] = new fabric['Dialog'](DialogElements[i]);
      }());
    }
    // When clicking the button, open the dialog
    jQuery(".dialog-button").click(function() {
        dialog_id = $(this).data('countid');
        openDialog(dialog_id-1); //decrement due to later use as array index
    });

    function openDialog(i) {
      // Open the dialog
        console.log("dialogid " + i);
        DialogComponents[i].open();
    }

    //enable submit without any submit button
    $(".submit-button").click(function() {
     $("#list_events").submit();
    });
});

function ajax_loadEvents(className, id, name) {
  xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      $(className).html(xhttp.responseText);
  }};

  console.log('id of ajax calendar ' + id, name, className);
  xhttp.open("GET", "/list_events?cal_id="+id+"&cal_name="+name, true);
  xhttp.send();

  $(className).addClass('open');
  $(className).removeClass('hide');
  console.log('remove Class from ' + className)
}

/* Toggle views */
function toggleListEvents(id) {

  className = '.events'+id;
  if ($(className).hasClass('open')) {
      console.log('classname: ' + className);
      $(className).addClass('hide');
  }
}

function toggleViewRooms() {
  if ($('.viewCalendars').hasClass('open')){
    $('.viewCalendars').removeClass('open');
    $('.viewCalendars').addClass('hide');
  }
  else {
    $('.viewCalendars').addClass('open');
    $('.viewCalendars').removeClass('hide');

    /* Close the other view */
    $('.createRoom').removeClass('open');
    $('.createRoom').addClass('hide')
  }
  $('.ms-MessageBar').addClass('hide');
}

function toggleCreateRoom() {
  console.log('openCreateRoom');
  if ($('.createRoom').hasClass('open')){
    $('.createRoom').removeClass('open');
    $('.createRoom').addClass('hide');
  }
  else {
    $('.createRoom').addClass('open');
    $('.createRoom').removeClass('hide');

    /* Close the other view */
    $('.viewCalendars').removeClass('open');
    $('.viewCalendars').addClass('hide')
  }
  $('.ms-MessageBar').addClass('hide');
}
