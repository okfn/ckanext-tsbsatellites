$(function() {
  function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
      return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
      return uri + separator + key + "=" + value;
    }
  }

  function convertDate(date) {
    day = date.getDate();
    month = date.getMonth();
    year = date.getFullYear()
    return year + '-' + month + '-' + day
  }

  function getDate(attr) {
    var date_string = $( "#dataset-slider" ).attr("data-" + attr);
    if (0 !== date_string.length) {
      return new Date(date_string.split('-'));
    }
    return ''
  }
  function init_slider() {
    var slider_options = {
      valueLabels:"change",
      delayOut: 4000,
      bounds: {
        min: getDate('begin'),
        max: getDate('end')
      }
    };
    var min = getDate('default-begin');
    var max = getDate('default-end');
    if ('' !== min && '' !== max) {
      slider_options['defaultValues'] = {
        min: min,
        max: max
      };
    } else {
      slider_options['defaultValues'] = {
        min: getDate('begin'),
        max: getDate('end')
      };
    }
    console.log(slider_options);
    $( "#dataset-slider-widget" ).dateRangeSlider(slider_options)
    .on("userValuesChanged", function(e, data){
      $('#ext_begin_date').val(convertDate(data.values.min));
      $('#ext_end_date').val(convertDate(data.values.max));
    });
  }
  init_slider();


  $("#ext_date_submit").on("click", function() {
    var current_url = document.URL;
    current_url = updateQueryStringParameter(current_url, 'ext_begin_date', $('#ext_begin_date').val());
    current_url = updateQueryStringParameter(current_url, 'ext_end_date', $('#ext_end_date').val());
    window.location = current_url;
  });

  $( "#ext_begin_date" ).datepicker();
  $( "#ext_end_date" ).datepicker();
});
