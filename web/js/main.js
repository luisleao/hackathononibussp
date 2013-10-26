var map;
	google.maps.visualRefresh = true;


var current_line;
var polylines = [];



var PARAMS = {
	0: {
		name: "Ida",
		cor: "#0000FF"
	},
	1: {
		name: "Volta",
		cor: "#555510"
	}
}








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

	loadLine("106A-10");

};

var formataTempo = function(seconds) {
	//TODO: formatar tempo em 00h 00'00"
	return (new Date).clearTime()
          .addSeconds(seconds)
          .toString('H:mm:ss');;
}

var loadLine = function(line){
	current_line = null;
	console.log("carregando linha ", line);

	jQuery.getJSON("/data/linhas/"+line+".json", function(data){
		console.log(line, data);
		current_line = data;

		//desenhar no mapa o tracado dos sentidos da linha
		clearPolylines();

		$(".linha").text(current_line.id);
		$(".name_linha").text(current_line.name);


		$(".sentidos").empty();

		for(sentido_idx in current_line.sentidos) {
			var sentido = current_line.sentidos[sentido_idx];
			var travel_time = formataTempo(sentido.travel_time);

			var layer_sentido = $(document.createElement("div"));
			



			console.log(sentido_idx, sentido.travel_time, travel_time);
			$(".travel_time").text(travel_time);
			//console.log(sentido_idx, data.sentidos[sentido_idx].shapes.points);
			drawPolyLine(sentido.shapes.points, PARAMS[sentido_idx].cor);
		}

		//TODO: carregar dados de IDA e VOLTA

/*
working: "USD",
travel_time: 26584,
name: "Itaim Bibi",
travel_discance: 0,
shape_id: 43387,
total_travels: 157
*/



		//TODO: carregar dados AVL e BILHETAGEM
		//TODO: criar markers para veiculos
		//TODO: posicionar markers conforme horario e ajuste de horario

	});

};


var clearPolylines = function(){
	for (idx in polylines) {
		polylines[idx].setMap(null);
		delete(polylines[idx]);
	}
}

var drawPolyLine = function(shapes, color){
	//console.log("POLY ", color, shapes);
	var points = [];
	for (idx in shapes) {
		var point = shapes[idx];
		points.push(new google.maps.LatLng(point.lat, point.lng))
	}


	polyline = new google.maps.Polyline({
		path: points,
		geodesic: true,
		strokeColor: color,
		strokeOpacity: 0.7,
		strokeWeight: 2
	});
	polyline.setMap(map);

	polylines.push(polyline);

   	//TODO: remover linha a seguir
	var lengthInMeters = google.maps.geometry.spherical.computeLength(polyline.getPath());
   	console.log("distancia ", lengthInMeters)




};



jQuery(document).ready(function($) {

	console.log("init");
	google.maps.event.addDomListener(window, 'load', initializeMap);
	

	$(".modal").modal({show: false});


	$("#modal_selecionalinha").modal("show");


});

