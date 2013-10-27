var map;
	google.maps.visualRefresh = true;


var current_line;
var current_time = 0;
var polylines = [];
var markers = {};

var tmrInterval;
var mapOptions;
var saopaulo;


var PARAMS = {
	0: {
		name: "Ida",
		cor: "#0000FF"
	},
	1: {
		name: "Volta",
		cor: "#555510"
	},
	interval: 1,
	date: new Date(2013, 6, 1)

}





var addMarker = function(cod_veiculo, veiculo){
	console.log("addmarker ", veiculo);


	//TODO: adicionar marcador na lista, deixar oculto e exibir quando o tempo tiver AVL
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(veiculo[0][1], veiculo[0][2]),
      map: map,
      animation: google.maps.Animation.DROP,
      //icon: icon_grey,
      //visible: false
    });

    marker.infoWindow = new google.maps.InfoWindow();

    google.maps.event.addListener(marker, 'click', function(event){
		if (this.infoWindow) this.infoWindow.open(map, this);
    });

    veiculo.marker = marker;
    markers[cod_veiculo] = marker;
}


var carregou_avl = function(){
	for (var sentido_idx in current_line.sentidos) {
		if (!current_line.sentidos[sentido_idx].carregou_avl){
			return false;
		}
	}
	return true;
}

var carregou_blt = function(){
	for (var sentido_idx in current_line.sentidos) {
		if (!current_line.sentidos[sentido_idx].carregou_blt){
			return false;
		}
	}
	return true;
}






var atualiza_tempo = function(){
	// so rodar se tiver carregado AVL de todos os sentidos
	if (!carregou_avl)
		return;

	if (carregou_avl() && !current_line.carregou_sentidos) {
		//TODO: criar marcadores dos veiculos
		for(cod_veiculo in current_line.veiculos) {
			addMarker(cod_veiculo, current_line.veiculos[cod_veiculo]);
		}
		current_line.carregou_sentidos = true;
	}

	// não conta tempo enquanto nao carregar AVL

	current_time++;
	if (current_time >= 86400)
		current_time = 0;

	var data = PARAMS.date.getTime() + current_time*1000;



	$(".datetime").text(new Date(data).toString("dd/MM/yyyy HH:mm:ss")); //new Date(data/1000 + (current_time))); //formataTempo(current_time));
};


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
          .toString('HH:mm:ss');;
}

var loadLine = function(line){
	current_line = null;
	console.log("carregando linha ", line);

	jQuery.getJSON("/data/linhas/"+line+".json", function(data){
		console.log(line, data);
		current_line = data;
		current_line.veiculos = {};
		current_line.carregou_sentidos = false;


		//desenhar no mapa o tracado dos sentidos da linha
		clearPolylines();

		$(".linha .numero").text(current_line.id);
		$(".name_linha").text(" " + current_line.name).prepend($("<small/>").text(current_line.id));

		$(".sentidos").empty();

		for (var sentido_idx in current_line.sentidos) {

			var sentido = current_line.sentidos[sentido_idx];
			var travel_time = formataTempo(sentido.travel_time);

			// carregar AVL
			sentido.carregou_avl = false;
			jQuery.getJSON("/data/linhas/avl/"+line.replace("-","")+sentido_idx+"_avl.json", function(data) {
				var sentido_idx = data.cod_linha.substring(data.cod_linha.length-1);
				var sentido = current_line.sentidos[sentido_idx];

				for (var veiculo_id in data.veiculos) {
					var avls = data.veiculos[veiculo_id]; //eh um array
					if (!current_line.veiculos[veiculo_id]) {
						current_line.veiculos[veiculo_id] = [];
					}

					for (avl_idx in avls) {
						avl_item = avls[avl_idx];
						avl_item[0] = parseInt(avl_item[0]); //TODO: BUG - corrigir importacao do AVL e passar inteiro direto
						avl_item.push(parseInt(sentido_idx)); //TODO: BUG - formatar codigo da linha e criar campo com sentido
						current_line.veiculos[veiculo_id].push(avl_item);
					}
				}
				sentido.carregou_avl = true;
			});


			// carregar BLT
			sentido.carregou_blt = false;
			jQuery.getJSON("/data/linhas/blt/"+line.replace("-","")+sentido_idx+"_blt.json", function(data) {
				console.log("data blt", data);
				//TODO: ver dados BLT e inserir na planilha
				/*
				var sentido_idx = data.cod_linha.substring(data.cod_linha.length-1);
				for (var veiculo_id in data.veiculos) {
					if (!sentido.veiculos[veiculo_id]) {
						sentido.veiculos[veiculo_id] = [];
					}
					veiculo_avl = sentido.veiculos[veiculo_id];
					var avls = data.veiculos[veiculo_id]; //eh um array
					for (avl_idx in avls) {
						avl_item = avls[avl_idx];
						avl_item[0] = parseInt(avl_item[0]); //TODO: BUG - corrigir importacao do AVL e passar inteiro direto
						avl_item.push(parseInt(sentido_idx)); //TODO: BUG - formatar codigo da linha e criar campo com sentido
					}
					//concatenar arrays de avl
					veiculo_avl.concat(avls);
				}
				*/
				sentido.carregou_blt = true;

			}); //.fail(function(){}).complete(function(){console.log("complete", sentido_idx);});


			var layer_sentido = $(document.createElement("div")).addClass("sentido_item").attr("id", "sentido_" + sentido_idx);
			var span_partida = $("<small/>").text("partida: ");


			var glyphicon_time = $("<span/>").addClass("glyphicon glyphicon-time");
			var glyphicon_road = $("<span/>").addClass("glyphicon glyphicon-road");
			var glyphicon_list = $("<span/>").addClass("glyphicon glyphicon-list");

			var glyphicon_left = $("<span/>").addClass("glyphicon glyphicon-chevron-left");
			var glyphicon_right = $("<span/>").addClass("glyphicon glyphicon-chevron-right");





			layer_sentido.append($("<span/>").addClass("item name").text(" " + sentido.name).prepend(span_partida)).append($("<br/>")); //sentido_idx == 0 ? glyphicon_right : glyphicon_left));
			layer_sentido.append($("<span/>").addClass("item travel_time").attr("title", "Tempo do percurso").text(" " + travel_time).prepend(glyphicon_time)).append($("<br/>"));
			layer_sentido.append($("<span/>").addClass("item travel_distance").attr("title", "Distância do percurso").text(" " + (sentido.shapes.total_distance_traveled/1000).toFixed(2) + " km").prepend(glyphicon_road)).append($("<br/>"));
			layer_sentido.append($("<span/>").addClass("item total_travels").attr("title", "Total de viagens").text(" " + sentido.total_travels + " viagens").prepend(glyphicon_list)).append($("<br/>"));
			//layer_sentido.append($("<div/>").addClass("working").text(sentido.working));
			layer_sentido.append($("<span/>").addClass("item spark travel_" + sentido_idx).attr("title", "Viagens por horas [00-23]"));


			$(".sentidos").append(layer_sentido);
			$(".sentidos .travel_" + sentido_idx).sparkline(sentido.travels, { type: 'bar', barColor: '#aaffff', zeroAxis: false, disableTooltips: true });
			
			console.log(sentido_idx, sentido.travel_time, travel_time);
			drawPolyLine(sentido.shapes.points, PARAMS[sentido_idx].cor);
		}


		$(".sentidos .item").tooltip();

		//carregar traçados de IDA e VOLTA
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


		current_time = 0;
		if (atualiza_tempo) window.clearInterval(atualiza_tempo);
		tmrInterval = window.setInterval(atualiza_tempo, PARAMS.interval);


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

