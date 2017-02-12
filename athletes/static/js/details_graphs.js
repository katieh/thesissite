// TODO: fix histogram labels
// TODO: fix histogram size (they should fill out box)
// TODO: set bins properly
// TODO: highlight bin that this activity is in!
// TODO: let people choose between "average" and "max"

var keys = Object.keys(field_graphs)

// make line graphs for all of the variables
for (i in keys) {

    make_line_graph(keys[i]);
}

keys = Object.keys(field_histograms)

// make histograms for all of the variables
for (i in keys) {
    make_histogram(keys[i])
}


/* NOTE: This code is based on the following tutorials:
    - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
    - http://www.dreisbach.us/blog/building-dashboards-with-django-and-d3/
    - http://nvd3.org/livecode/index.html#codemirrorNav
*/
function make_line_graph(key) {


    height = 250

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.lineChart()
        .useInteractiveGuideline(true)
        .height(height);

        chart.xAxis
        .axisLabel('Distance')
        .tickFormat(d3.format('d'))
        ;

        chart.yAxis
        .axisLabel('Speed (mph)')
        .tickFormat(d3.format('.2f'))
        ;

        // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
        d3.select("#" + key + " svg")
        .datum(field_graphs[key])
        .transition().duration(500)
        .call(chart).style({'height': height});

        nv.utils.windowResize(chart.update);

        return chart;
    });
}

function  get_histogram_xaxis_label(key) {
    if (key == "speed-histogram") {
        return "Speed"
    }
    else if (key == "elevation_gained-histogram") {
        return "Elevation Gained"
    }
    else if (key == "cadence-histogram") {
        return "Cadence"
    }
    else if(key == "hr-histogram") {
        return "Heart Rate"
    }
    else {
        throw "key does not have a defined label!"
    }
}

/* NOTE: This code is based on the following example:
    - https://github.com/novus/nvd3/blob/master/examples/historicalBarChart.html
*/
function make_histogram(key) {

    height = 250

    nv.addGraph(function() {
        var chart = nv.models.historicalBarChart()
        .height(height);

        // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly,
        // return themselves, not the parent chart, so need to chain separately
        chart.xAxis
            .axisLabel(get_histogram_xaxis_label(key))
            .tickFormat(d3.format(',.1f'));
        chart.yAxis
            .axisLabel("Count")
            .tickFormat(d3.format('d'));
        chart.forceY([field_histograms[key]['metadata']['ymin'], 
            field_histograms[key]['metadata']['ymax']])
        chart.forceX([field_histograms[key]['metadata']['xmin'], 
            field_histograms[key]['metadata']['xmax']])
        chart.showXAxis(true);
        d3.select("#" + key + " svg")
            .datum(field_histograms[key]['graph'])
            .transition()
            .call(chart).style({'height': height});


        nv.utils.windowResize(chart.update);
        return chart;
    });

}

