// Makes an AJAX request to populate the list of previous articles
// HTML is returned and inserted into the column
// Called after making database changes
function previous() {
  $.ajax({
    type: "GET",
    cache: false,
    url: "/previous",
    dataType: "html",
    success: function(data, status, xhr) {
      $('#previous-articles').html(data);
    },
    error: function(xhr, status, error) {
      $('#previous-articles').html(error);
    }
  });
};

// Make AJAX request to change published status of an article
function changePublish(type, issue, state, title) {
  $.ajax({
    type: "POST",
    cache: false,
    url: "/publish",
    data: JSON.stringify({
    	"type": type,
    	"issue": issue,
    	"state": state,
    	"title": title
    	}),
    contentType: "application/json",
    dataType: "json",
    success: function(data, status, xhr){
      if (data['result'] == 0) {
        alert(data['message']);
      } else {
        previous();
      }
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
};

// Insert template tags into main text

function insertHeaderTag() {
	insertAtCaret("body", '\r<h5>Heading</h5>\r');
};

function insertImageTag() {
	insertAtCaret("body", '\r<img src="/images/" alt="" class="img-fluid rounded my-4" />\r');
};

function insertLinkTag() {
	insertAtCaret("body", '<a href="" title="" class=""></a>');
};
	
function insertGPOOHinfo() {
	insertAtCaret("body", '\rIf you need a doctor when the practice is closed and it cannot wait until the practice reopens, you can contact the North and West Belfast GP Out-of-hours service on <a href="tel:02890744447">028 9074 4447</a>.\r');
};

function insertAtCaret(areaId, text) {
		var txtarea = document.getElementById(areaId);
		if (!txtarea) { return; }

		var scrollPos = txtarea.scrollTop;
		var strPos = 0;
		var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
			"ff" : (document.selection ? "ie" : false ) );
		if (br == "ie") {
			txtarea.focus();
			var range = document.selection.createRange();
			range.moveStart ('character', -txtarea.value.length);
			strPos = range.text.length;
		} else if (br == "ff") {
			strPos = txtarea.selectionStart;
		}

		var front = (txtarea.value).substring(0, strPos);
		var back = (txtarea.value).substring(strPos, txtarea.value.length);
		txtarea.value = front + text + back;
		strPos = strPos + text.length;
		if (br == "ie") {
			txtarea.focus();
			var ieRange = document.selection.createRange();
			ieRange.moveStart ('character', -txtarea.value.length);
			ieRange.moveStart ('character', strPos);
			ieRange.moveEnd ('character', 0);
			ieRange.select();
		} else if (br == "ff") {
			txtarea.selectionStart = strPos;
			txtarea.selectionEnd = strPos;
			txtarea.focus();
		}

		txtarea.scrollTop = scrollPos;
	}


// Functions to run when the document is ready
$(document).ready(function() {

  // Get previous articles
  previous();
  
  // Publish indicator
  $("#publish").on("change", function(){
    // this will contain a reference to the checkbox
    if (this.checked) {
        // the checkbox is now checked 
        $("#publish-indicator").removeClass("text-danger");
  		$("#publish-indicator").addClass("text-success");
  	} else {
  		$("#publish-indicator").removeClass("text-success");
  		$("#publish-indicator").addClass("text-danger");
    }
  });

  // Change subtitle based on article type
  $("#type").change(function() {
    $("#subtitle").html($("#type option:selected").text());
  });

  // Attach a submit handler to the form
  $("#update-form").submit(function(event) {

    // Change submit button when clicked
    $("#submit-button").removeClass("btn-success");
    $("#submit-button").removeClass("btn-danger");
    $("#submit-button").addClass("btn-primary");
    $("#submit-button").val("Submitting");
    $("#submit-button").attr("disabled", true);

    // Stop form from submitting normally
    event.preventDefault();

    // Get values from elements on the page using FormData object
    var data = new FormData($('form')[0]);

    // Get filename for upload and add to ddata to insert into database
    var filename = $('#file').val().split("\\").pop();
    data.append("image", filename);

    // AJAX request
    $.ajax({
      type: "post",
      url: "/update",
      data: data,
      processData: false,
      contentType: false,
      error: function(xhr, status, error) {
        $("#submit-button").val(error);
        $("#submit-button").addClass("btn-danger");
        $("#submit-button").attr("disabled", false);
      },
      success: function(data, status, xhr) {
        $("#submit-button").val(data['message']);
        $("#submit-button").attr("disabled", false);
        if (data['result'] == 0) {
          $("#submit-button").removeClass("btn-primary");
          $("#submit-button").addClass("btn-danger");
        } else {
          $("#submit-button").removeClass("btn-primary");
          $("#submit-button").addClass("btn-success");
          previous();
        }
      }
    }); // AJAX
  }); // Submit handler
  
}); // Document ready
