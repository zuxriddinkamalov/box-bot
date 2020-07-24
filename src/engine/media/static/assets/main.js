//Django basic setup for accepting ajax requests.
// Cookie obtainer Django
console.log("connected")


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});


function EditCart(id){
  console.log(image_changed)
  var title = document.getElementById("cat_title").value;
  var description = document.getElementById("cat_description").value;
  var order = document.getElementById("cat_order").value;
  var active = document.getElementById("cat_active");
  
  if (active.checked){
    active = 1
  } else{
    active = 0
  }

  $.ajax({
      url : "/ru/categories/"+ id + "/edit/", // the endpoint
      type : "POST", // http method
      data : { category: id, title: title, description: description, order: order, active: active}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          if (image_changed){
          var fd = new FormData();
          var image = $('#cat_image_file')[0].files[0];
          fd.append('file', image)

          $.ajax({
            url : "/ru/categories/"+ id + "/edit/", // the endpoint
            type : "POST", // http method
            data : fd, // data sent with the post request
            contentType: false,
            processData: false,
            // handle a successful response
            success : function(json) {
                location.replace("/ru/categories/")
                console.log(json)
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
        );
      } else{
          location.replace("/ru/categories/")
      }
      },
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  }
  );
}