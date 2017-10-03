/**
 * Created by micha (02468) on 8/24/17.
 */

/* Shows the dialog element before the deletion of an event
 * Uses a data-countid field to identify which calendar shall be deleted
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


/* Uses AJAX to asynchroniously loading the events for the respective calendar without reloading the whole page
 * Uses the template events.html to inject this page into the main page
 */
function ajax_loadEvents(className, id, name) {
  xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      $(className).html(xhttp.responseText); // injects the html code of events.html into the current page
  }
  if (this.status == 500) {
      $(className).html('An error occured while loading the events!')
  }
  else {
      $(className).html('<p class="ms-font-l ms-fontColor-yellow">Bitte warten ...</p>'); // injects the html code of events.html into the current page
  }
  };

  console.log('id of ajax calendar ' + id, name, className);
  xhttp.open("GET", "list_events?cal_id="+id+"&cal_name="+name, true);
  xhttp.send();

  $(className).addClass('open');
  $(className).removeClass('hide');
  console.log('remove Class from ' + className)
}


/* Toggles the events which are displayed for one calendar. Called upon click on the blue frame */
function toggleListEvents(id) {

  className = '.events'+id;
  if ($(className).hasClass('open')) {
      console.log('classname: ' + className);
      $(className).addClass('hide');
  }
}

/* Toggles the content of displaying all rooms with the respective events
 * It furthermore redirects to the main page after each click to avoid being stuck in virtual subpages after form submissions
 */
function toggleViewRooms() {
  window.location = '/main';
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


/* Toggles the content of the form to add a new calendar */
function toggleCreateRoom() {

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
