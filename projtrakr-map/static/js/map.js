// initialize the map
var map = L.map('map',
                {
                    zoomControl:false
                    }).setView([42.35, -71.08], 13);

L.control.zoom({
     position:'bottomright'
}).addTo(map);

// load a tile layer
L.tileLayer('http://tiles.mapc.org/basemap/{z}/{x}/{y}.png',
{
    attribution: 'Tiles by <a href="http://mapc.org">MAPC</a>, Data by <a href="http://mass.gov/mgis">MassGIS</a>',
    maxZoom: 17,
    minZoom: 9
}).addTo(map);


// bike lanes
L.tileLayer('http://tiles.mapc.org/trailmap-onroad/{z}/{x}/{y}.png',
{
    maxZoom: 17,
    minZoom: 9
}).addTo(map);

function PolygonStyle(feature){
      var fillColor,
          density = feature.properties.density;
      if ( density > 80 ) fillColor = "#006837";
      else if ( density > 40 ) fillColor = "#31a354";
      else if ( density > 20 ) fillColor = "#78c679";
      else if ( density > 10 ) fillColor = "#c2e699";
      else if ( density > 0 ) fillColor = "#ffffcc";
      else fillColor = "#f7f7f7";  // no data
      return { color: "#999", weight: 1, fillColor: fillColor, fillOpacity: .6 };
    };
    

$.getJSON("https://github.com/ultigeo/projectrack/blob/master/projtrakr-map/data/neighborhoods.geojson",function(hoodData){
  L.geoJson( hoodData,{
    style: PolygonStyle,
    onEachFeature: function( feature, layer ){
      layer.bindPopup( "<strong>" + feature.properties.Name + "</strong><br/>" + feature.properties.density + " rats per square mile" )
    }
  } ).addTo(map);
});

var ratIcon = L.icon({
    iconUrl: 'assets/images/layers.png',
    iconSize: [60,50]
  });
// load GeoJSON from an external file
$.getJSON("https://github.com/ultigeo/projectrack/blob/master/projtrakr-map/data/points.geojson",function(data){
  var points=L.geoJson(data,{
    pointToLayer: function(feature,latlng){
        onEachFeature: onEachFeature;
        var marker = L.marker(latlng,{icon: ratIcon});
        marker.bindPopup(feature.properties.Location + '<br/>' + feature.properties.OPEN_DT);
        return marker;
    }
    
  });
  var clusters=L.markerClusterGroup();
  
/*for ( var i = 0; i < points.length; ++i )
{
  var popup = points[i].name +
              '<br/>' + points[i].city +
              '<br/><b>IATA/FAA:</b> ' + points[i].iata_faa +
              '<br/><b>ICAO:</b> ' + points[i].icao +
              '<br/><b>Altitude:</b> ' + Math.round( points[i].alt * 0.3048 ) + ' m' +
              '<br/><b>Timezone:</b> ' + points[i].tz;
 
  var m = L.marker( [points[i].lat, points[i].lng], {icon: myIcon} )
                  .bindPopup( popup );
 
  markerClusters.addLayer( m );
}
*/

  clusters.addLayer(points);
  map.addLayer(clusters);
});

//About the map sidebar left
var sidebar = L.control.sidebar('sidebar').addTo(map);

//var sidebar = L.control.sidebar('sidebar', {
//    closeButton: true,
//    position: 'left'
//});
//map.addControl(sidebar);

//Pop-up side bar on the right
var rightSidebar = L.control.sidebar('sidebar', {
    closeButton:true,
    position: 'right'
});
map.addControl(rightSidebar);


setTimeout(function () {
    sidebar.show();
}, 500);

setTimeout(function () {
    rightSidebar.show();
}, 2500);


map.on('click', function () {
            sidebar.toggle();
        })

function onEachFeature(feature, layer) {
    layer.on({
        click: function populate() {
            document.getElementById('settings').innerHTML = "BLAH BLAH BLAH " + feature.properties.name + "<br>" + feature.properties.description;
        }
    });
}