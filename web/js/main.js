var map;
	google.maps.visualRefresh = true;



var initializeMap = function() {

	var brazil = new google.maps.LatLng(-23.576732121654487, -46.633530120117186);
	var mapOptions = {
		zoom: 12,
		center: brazil,
		mapTypeControl: true,
		panControl: false,
		scaleControl: false,
		streetViewControl: false,
		zoomControl: true,
		//mapTypeControlOptions: { mapTypeIds: [MY_MAPTYPE_ID]},
		//mapTypeId: MY_MAPTYPE_ID,
		navigationControlOptions: { style: google.maps.NavigationControlStyle.SMALL },

	}

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

}







jQuery(document).ready(function($) {

	console.log("init");
	google.maps.event.addDomListener(window, 'load', initializeMap);
	


});

