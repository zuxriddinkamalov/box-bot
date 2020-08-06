//Django basic setup for accepting ajax requests.
// Cookie obtainer Django

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

function NewCat(){
  var title = document.getElementById("cat_title").value;
  var description = document.getElementById("cat_description").value;
  var order = document.getElementById("cat_order").value;
  var active = document.getElementById("cat_active");
  var language = document.getElementById("language").textContent;
  const image = document.getElementById('cat_image')


  if (active.checked){
    active = 1
  } else{
    active = 0
  }

  var fd = new FormData();

  fetch(image.src)
    .then(res => res.blob())
    .then(blob => {
      const file = new File([blob], 'dot.png', blob)
      fd.append('file', file)
      // fd.append('title', title)

      console.log(fd.getAll())
    })
  // fd.append('title', title)

  $.ajax({
      url : "/categories/new/", // the endpoint
      type : "POST", // http method
      data : fd, // data sent with the post request
      contentType: false,
      processData: false,

      // handle a successful response
      success : function(json) {
        console.log(json)
          //   var id = json
          //   var fd = new FormData();
          //   var image = $('#cat_image_file')[0].files[0];
          //   fd.append('file', image)

          //   $.ajax({
          //     url : "/categories/" + id + "/new/", // the endpoint
          //     type : "POST", // http method
          //     data : fd, // data sent with the post request
          //     contentType: false,
          //     processData: false,
          //     // handle a successful response
          //     success : function(json) {
          //         location.replace("/" + language + "/categories/")
          //     },
          //     error : function(xhr,errmsg,err) {
          //         $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
          //             " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          //         //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          //     }
          // }
          //   );
      },
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  }
  );
}

function DeleteCat(id){
  var language = document.getElementById("language").textContent;

  $.ajax({
    url : "/" + language + "/categories/"+ id + "/delete/", // the endpoint
    type : "POST", // http method
    data : { category: id}, // data sent with the post request

    // handle a successful response
    success : function(json) {
      location.replace("/" + language + "/categories/")
    },
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
          " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
  }
});
}


function EditCat(id){
  var title = document.getElementById("cat_title").value;
  var description = document.getElementById("cat_description").value;
  var order = document.getElementById("cat_order").value;
  var active = document.getElementById("cat_active");
  var language = document.getElementById("language").textContent;

  
  if (active.checked){
    active = 1
  } else{
    active = 0
  }

  $.ajax({
      url : "/" + language + "/categories/"+ id + "/edit/", // the endpoint
      type : "POST", // http method
      data : { category: id, title: title, description: description, order: order, active: active}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          if (image_changed){
              var fd = new FormData();
              var image = $('#cat_image_file')[0].files[0];
              fd.append('file', image)

              $.ajax({
                url : "/" + language + "/categories/"+ id + "/edit/", // the endpoint
                type : "POST", // http method
                data : fd, // data sent with the post request
                contentType: false,
                processData: false,
                // handle a successful response
                success : function(json) {
                    location.replace("/" + language + "/categories/")
                },
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            }
            );
          } else{
              location.replace("/" + language + "/categories/")
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

function EditProduct(id){
  var title = document.getElementById("cat_title").value;
  var description = document.getElementById("cat_description").value;
  var order = document.getElementById("cat_order").value;
  var active = document.getElementById("cat_active");
  var price = document.getElementById("cat_price").value;
  var category = document.getElementById("cat_select");
  var category = category.options[category.selectedIndex].value;
  // var category = $(this).children("option:selected").val();

  console.log(category)
  var language = document.getElementById("language").textContent;

  
  if (active.checked){
    active = 1
  } else{
    active = 0
  }

  $.ajax({
      url : "/" + language + "/products/"+ id + "/edit/", // the endpoint
      type : "POST", // http method
      data : { category: category, title: title, description: description, order: order, active: active, price: price}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          if (image_changed){
              var fd = new FormData();
              var image = $('#cat_image_file')[0].files[0];
              fd.append('file', image)

              $.ajax({
                url : "/" + language + "/products/"+ id + "/edit/", // the endpoint
                type : "POST", // http method
                data : fd, // data sent with the post request
                contentType: false,
                processData: false,
                // handle a successful response
                success : function(json) {
                    location.replace("/" + language + "/products/")
                },
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            }
            );
          } else{
              location.replace("/" + language + "/products/")
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


function DeleteProduct(id){
  var language = document.getElementById("language").textContent;

  $.ajax({
    url : "/" + language + "/products/"+ id + "/delete/", // the endpoint
    type : "POST", // http method
    data : { product: id}, // data sent with the post request

    // handle a successful response
    success : function(json) {
      location.replace("/" + language + "/products/")
    },
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
          " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
  }
});
}

function EditNews(id){
  var title = document.getElementById("cat_title").value;
  var description = document.getElementById("cat_description").value;
  var views = document.getElementById("cat_views").value;
  var active = document.getElementById("cat_active");
  var visible = document.getElementById("cat_visible");

  var language = document.getElementById("language").textContent;

  
  if (active.checked){
    active = 1
  } else{
    active = 0
  }

  if (visible.checked){
    visible = 1
  } else{
    visible = 0
  }

  $.ajax({
      url : "/" + language + "/news/"+ id + "/edit/", // the endpoint
      type : "POST", // http method
      data : { title: title, text: description, views: views, active: active, visible: visible}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          if (image_changed){
              var fd = new FormData();
              var image = $('#cat_image_file')[0].files[0];
              fd.append('file', image)

              $.ajax({
                url : "/" + language + "/news/"+ id + "/edit/", // the endpoint
                type : "POST", // http method
                data : fd, // data sent with the post request
                contentType: false,
                processData: false,
                // handle a successful response
                success : function(json) {
                    location.replace("/" + language + "/news/")
                },
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            }
            );
          } else{
              location.replace("/" + language + "/news/")
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


function DeleteNews(id){
  var language = document.getElementById("language").textContent;

  $.ajax({
    url : "/" + language + "/news/"+ id + "/delete/", // the endpoint
    type : "POST", // http method
    data : { product: id}, // data sent with the post request

    // handle a successful response
    success : function(json) {
      location.replace("/" + language + "/news/")
    },
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
          " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
  }
});
}

function EditEvents(id){
  var title = document.getElementById("cat_title").value;
  var description = document.getElementById("cat_description").value;
  var views = document.getElementById("cat_views").value;
  var active = document.getElementById("cat_active");
  var visible = document.getElementById("cat_visible");

  var language = document.getElementById("language").textContent;

  
  if (active.checked){
    active = 1
  } else{
    active = 0
  }

  if (visible.checked){
    visible = 1
  } else{
    visible = 0
  }

  $.ajax({
      url : "/" + language + "/events/"+ id + "/edit/", // the endpoint
      type : "POST", // http method
      data : { title: title, text: description, views: views, active: active, visible: visible}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          if (image_changed){
              var fd = new FormData();
              var image = $('#cat_image_file')[0].files[0];
              fd.append('file', image)

              $.ajax({
                url : "/" + language + "/events/"+ id + "/edit/", // the endpoint
                type : "POST", // http method
                data : fd, // data sent with the post request
                contentType: false,
                processData: false,
                // handle a successful response
                success : function(json) {
                    location.replace("/" + language + "/events/")
                },
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            }
            );
          } else{
              location.replace("/" + language + "/events/")
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


function DeleteNews(id){
  var language = document.getElementById("language").textContent;

  $.ajax({
    url : "/" + language + "/events/"+ id + "/delete/", // the endpoint
    type : "POST", // http method
    data : { product: id}, // data sent with the post request

    // handle a successful response
    success : function(json) {
      location.replace("/" + language + "/events/")
    },
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
          " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
  }
});
}