$(function() {
  $( "#search" ).autocomplete({
    delay: 0,
    source: '/api/util/search',
    minLength: 2,
    focus: function( event, ui ) {
      $( "#search" ).val( ui.item.label );
      return false;
    },
    select: function( event, ui ) {
      $( "#search" ).val( ui.item.label );
    return false;
    }
  })
  .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
    var icon = "";
    if ( 'history' === item.category ) {
      icon = "<i class='icon-time'></i> ";
    }
    return $( "<li>" )
      .append( "<a>" + icon + item.label + "</a>" )
      .appendTo( ul );
  };
});
