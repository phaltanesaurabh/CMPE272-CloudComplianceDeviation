
function createBarChart() {
	
    $('#homePageBarChart').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Weekly Report'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: [
                'Day 1',
                'Day 2',
                'Day 3',
                'Day 4',
                'Day 5',
                'Day 6',
                'Day 7'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'No. of Events'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'HIPAA',
            data: [7, 1, 4, 7, 12, 5, 9]

        }, {
            name: 'PCI',
            data: [5, 8, 8, 4, 6, 9, 2]

        }, {
            name: 'NIST',
            data: [2, 8, 9, 4, 7, 8, 9]

        }]
    });
}



function weekCreate() {
    var endDate;

    var selectCurrentWeek = function() {
        window.setTimeout(function () {
            $('.week-picker').find('.ui-datepicker-current-day a').addClass('ui-state-active')
    var startDate;
        }, 1);
    }

    $('.week-picker').datepicker( {
        showOtherMonths: true,
        selectOtherMonths: true,
        onSelect: function(dateText, inst) { 
            var date = $(this).datepicker('getDate');
            startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
            endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
            var dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
            $('#startDate').text($.datepicker.formatDate( dateFormat, startDate, inst.settings ));
            $('#endDate').text($.datepicker.formatDate( dateFormat, endDate, inst.settings ));

            selectCurrentWeek();
        },
        beforeShowDay: function(date) {
            var cssClass = '';
            if(date >= startDate && date <= endDate)
                cssClass = 'ui-datepicker-current-day';
            return [true, cssClass];
        },
        onChangeMonthYear: function(year, month, inst) {
            selectCurrentWeek();
        }
	
    });

    //$('.week-picker .ui-datepicker-calendar tr').live('mousemove', function() { $(this).find('td a').addClass('ui-state-hover'); });
    //$('.week-picker .ui-datepicker-calendar tr').live('mouseleave', function() { $(this).find('td a').removeClass('ui-state-hover'); });

}

jQuery(document).ready(function() {
	//Total count of log events
	//var totalCountURL = "http://52.23.100.76/ccms/get_counts.php";
var count;

	$.ajax({
        	type: "POST",
        	dataType: "json",
      		url: "http://52.23.100.76/ccms/get_counts.php",
		data : {'type' : 'hipaacount'},
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		console.log(count);
		$('#HIPAACount').text(count.count);}
		});

	$.ajax({
        	type: "POST",
        	dataType: "json",
      		url: "http://52.23.100.76/ccms/get_counts.php",
		data : {'type' : 'pcicount'},
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		console.log(count);
		$('#PCICount').text(count.count);}
		});

	$.ajax({
        	type: "POST",
        	dataType: "json",
      		url: "http://52.23.100.76/ccms/get_counts.php",
		data : {'type' : 'nistcount'},
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		console.log(count);
		$('#NISTCount').text(count.count);}
		});
	
	$.ajax({
        	type: "POST",
        	dataType: "json",
      		url: "http://52.23.100.76/ccms/get_counts.php",
		data : {'type' : 'fedrampcount'},
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		console.log(count);
		$('#FEDRAMPCount').text(count.count);}
		});
	

	$.ajax({
        	type: "POST",
        	dataType: "json",
      		url: "http://52.23.100.76/ccms/get_counts.php",
		data : {'type' : 'totalCount'},
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		console.log(count);
		$('#totalCount').text(count.count);}
		});

     
	$.ajax({
        	type: "POST",
        	dataType: "json",
		data : {'type' : 'unknownip'},
      		url: "http://52.23.100.76/ccms/get_counts.php",
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		$('#UnknowIP').text(count.count);}
		});


	$.ajax({
        	type: "POST",
        	dataType: "json",
		data : {'type' : 'undesiredEvents'},
      		url: "http://52.23.100.76/ccms/get_counts.php",
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		$('#UnEvCnt').text(count.count);}
		});

	$.ajax({
        	type: "POST",
        	dataType: "json",
		data : {'type' : 'SeverLogCount'},
      		url: "http://52.23.100.76/ccms/get_counts.php",
                success: function(ajax_data) { 
		count = $.parseJSON(ajax_data);
		$('#SeverLogs').text(count.count);}
		});

	//total count of HIPAA, PCI and NIST
	//totalCountURL = "http://cors.io/?u=http://52.23.100.76:9200/spark_analytics/_count";
	//$.getJSON( totalCountURL, {format: "json"}, function( response ) { $('#UnEvCnt').text(response.count);});

	//total count of UnknowIP
	//totalCountURL = "http://cors.io/?u=http://52.23.100.76:9200/spark_analytics/ip_analytics/_count";
	//$.getJSON( totalCountURL, {format: "json"}, function( response ) { $('#UnknowIP').text(response.count);});
	
	//total count of SeverLogs
	//totalCountURL = "http://cors.io/?u=http://52.23.100.76:9200/spark_analytics/_count";
	//$.getJSON( totalCountURL, {format: "json"}, function( response ) { $('#SeverLogs').text(response.count);});
	
	//donutChart();

});

