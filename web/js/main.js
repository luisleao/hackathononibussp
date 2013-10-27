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






var mapOptions;
var saopaulo;


var initializeMap = function() {

	saopaulo = new google.maps.LatLng(-23.576732121654487, -46.633530120117186);
	mapOptions = {
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

	//loadLine("106A-10");

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

		$(".linha .numero").text(current_line.id);
		$(".name_linha").text(current_line.name);

		$(".sentidos").empty();

		for(sentido_idx in current_line.sentidos) {
			var sentido = current_line.sentidos[sentido_idx];
			var travel_time = formataTempo(sentido.travel_time);

			var layer_sentido = $(document.createElement("div")).addClass("sentido_item").attr("id", "sentido_" + sentido_idx);


			var glyphicon_time = $("<span/>").addClass("glyphicon glyphicon-time");
			var glyphicon_road = $("<span/>").addClass("glyphicon glyphicon-road");
			var glyphicon_list = $("<span/>").addClass("glyphicon glyphicon-list");

			var glyphicon_left = $("<span/>").addClass("glyphicon glyphicon-chevron-left");
			var glyphicon_right = $("<span/>").addClass("glyphicon glyphicon-chevron-right");

			var span_partida = $("<small/>").text("partida: ");



			layer_sentido.append($("<div/>").addClass("name").text(" " + sentido.name).prepend(span_partida)); //sentido_idx == 0 ? glyphicon_right : glyphicon_left));
			layer_sentido.append($("<div/>").addClass("travel_time").attr("title", "Tempo do percurso").text(" " + travel_time).prepend(glyphicon_time));
			layer_sentido.append($("<div/>").addClass("travel_distance").attr("title", "Distância do percurso").text(" " + (sentido.shapes.total_distance_traveled/1000).toFixed(2) + " km").prepend(glyphicon_road));
			layer_sentido.append($("<div/>").addClass("total_travels").attr("title", "Total de viagens").text(" " + sentido.total_travels + " viagens").prepend(glyphicon_list));
			//layer_sentido.append($("<div/>").addClass("working").text(sentido.working));
			layer_sentido.append($("<div/>").addClass("spark travel_" + sentido_idx));


			$(".sentidos").append(layer_sentido);
			$(".sentidos .travel_" + sentido_idx).sparkline(sentido.travels, { type: 'bar', zeroAxis: false, disableTooltips: true });
			
			console.log(sentido_idx, sentido.travel_time, travel_time);
			drawPolyLine(sentido.shapes.points, PARAMS[sentido_idx].cor);
		}

		//TODO: carregar dados de IDA e VOLTA
		if (polylines.length > 0) {
			var latlngbounds = new google.maps.LatLngBounds();
			for (polyline_idx in polylines) {
				console.log(polylines[polyline_idx].getPath().length);
				var path_array = polylines[polyline_idx].getPath().getArray();
				
				for (array_idx in path_array) {
					latlngbounds.extend(path_array[array_idx]);
				}
			}
			map.fitBounds(latlngbounds);

		} else {
			map.setOptions(mapOptions);
		}

		//map.setZoom(map.getZoom()+1);

		//TODO: carregar dados AVL e BILHETAGEM
		//TODO: criar markers para veiculos
		//TODO: posicionar markers conforme horario e ajuste de horario

		if (!$("body").hasClass("on"))
			$("body").addClass("on");

	});

};


var clearPolylines = function(){
	for (idx in polylines) {
		polylines[idx].setMap(null);
	}
	polylines = [];

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
	

	$(".modal").modal({show: false}).on("shown.bs.modal", function(){
		switch ($(this).attr("id")) {
			case "modal_selecionalinha":
				$("#input_linha").focus()
				break;
		}
	});


	$("#modal_selecionalinha").modal("show");

	$('#input_linha').typeahead({
			prefetch: 'data/lista_linhas.json',
			template: "<p><strong>{{value}}</strong>: {{full_name}}</p>",
			limit: 5,
			engine: Hogan
		}).on("typeahead:selected", function(obj, datum){
			loadLine(datum.value);
			$("#modal_selecionalinha").modal("hide");

		});


});

