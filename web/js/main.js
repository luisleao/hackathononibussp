var map;
	google.maps.visualRefresh = true;



var initializeMap = function() {

	var saopaulo = new google.maps.LatLng(-23.576732121654487, -46.633530120117186);
	var mapOptions = {
		zoom: 12,
		center: saopaulo,
		overviewMapControl: false,
		zoomControlOptions: { style: google.maps.ZoomControlStyle.SMALL },
		panControl: false,
		streetViewControl: false,
		mapTypeControl: false,

		//mapTypeControlOptions: { mapTypeIds: [MY_MAPTYPE_ID]},
		//mapTypeId: MY_MAPTYPE_ID,
		//scaleControl: false,
		//zoomControl: true,
	}

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

}







jQuery(document).ready(function($) {

	console.log("init");
	google.maps.event.addDomListener(window, 'load', initializeMap);
	

	$(".modal").modal({show: false});



});

