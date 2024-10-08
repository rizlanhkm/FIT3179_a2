var vg_1 = "js/map.vg.json";
vegaEmbed("#map_chart", vg_1).then(function(result) {
    // Access the Vega view instance as result.view
}).catch(console.error);

var vg_2 = "js/chart.vg.json";
vegaEmbed("#line_chart", vg_2).then(function(result) {
    // Access the Vega view instance as result.view
}).catch(console.error);