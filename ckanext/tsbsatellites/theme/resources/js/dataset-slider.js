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
    return new Date(date_string.split('-'));
  }

  $( "#dataset-slider-widget" ).dateRangeSlider({
    valueLabels:"change",
    delayOut: 4000,
    defaultValues: {
      min: getDate('begin'),
      max: getDate('end')
    }
  })
  .on("userValuesChanged", function(e, data){
    var current_url = document.URL;
    current_url = updateQueryStringParameter(current_url, 'ext_begin_date', convertDate(data.values.min));
    current_url = updateQueryStringParameter(current_url, 'ext_end_date', convertDate(data.values.max));
    window.location = current_url;
  });
});
