
make_line_chart(athletes_graph["distance"], "distance")
make_line_chart(athletes_graph["sRPE"], "sRPE")


function make_line_chart(data, key) {
    height = 250

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.lineChart()
        .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
        .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
        .height(height)

        chart.xAxis
        // modified from http://stackoverflow.com/questions/19459687/understanding-nvd3-x-axis-date-format
        .tickFormat(function(d) {
            return d3.time.format('%m/%d/%y')(new Date(d))
        })
        .rotateLabels(-45)
        ;

        chart.yAxis
        .tickFormat(d3.format('.2f'))
        ;

        // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
        d3.select("#" + key + " svg")
        .datum(data)
        .transition().duration(500)
        .call(chart).style({'height': height});

        nv.utils.windowResize(chart.update);

        return chart;
    });
}