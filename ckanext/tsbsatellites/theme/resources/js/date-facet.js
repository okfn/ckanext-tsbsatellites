(function(ckan, moment, document) {
  ckan.module('date-facet', function($, _) {
    return {
      options : {
        begin: null,
        end: null,
        default_begin: null,
        default_end: null
      },
      initialize: function () {
        $.proxyAll(this, /_/);

        this.el.removeClass('js-hide');
        $('input', this.el).datepicker({
          dateFormat: 'yy-mm-dd'
        });

        var defaultValues = {
          min: this._getDate(this.options.default_begin),
          max: this._getDate(this.options.default_end)
        };
        if (defaultValues.min === '' && defaultValues.max === '') {
          defaultValues.min = this._getDate(this.options.begin);
          defaultValues.max = this._getDate(this.options.end);
        }

        $('<div />')
          .insertAfter($('.module-heading', this.el))
          .dateRangeSlider({
            valueLabels:"change",
            delayOut: 4000,
            bounds: {
              min: this._getDate(this.options.begin),
              max: this._getDate(this.options.end)
            },
            defaultValues: defaultValues
          })
          .on('userValuesChanged', this._handleSliderChanged);

        $('button', this.el).on('click', this._handleUpdateURL);
      },
      _convertDate: function (date) {
        return moment(date).format('YYYY-MM-DD');
      },
      _getDate: function (date) {
        if (date.length !== 0 && date !== true) {
          return new Date(date.split('-'));
        }
        return '';
      },
      _handleSliderChanged: function (event, data) {
        $('input[name="begin"]', this.el).val(this._convertDate(data.values.min));
        $('input[name="end"]', this.el).val(this._convertDate(data.values.max));
      },
      _handleUpdateURL: function (event) {
        var url = document.URL;
        url = this._updateQueryStringParameter(url, 'ext_begin_date', $('[name="begin"]', this.el).val());
        url = this._updateQueryStringParameter(url, 'ext_end_date', $('[name="end"]', this.el).val());
        window.location = url;
      },
      _updateQueryStringParameter: function (uri, key, value) {
        var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
        var separator = uri.indexOf('?') !== -1 ? "&" : "?";
        if (uri.match(re)) {
          return uri.replace(re, '$1' + key + "=" + value + '$2');
        } else {
          return uri + separator + key + "=" + value;
        }
      }
    };
  });
}(window.ckan, window.moment, document));
