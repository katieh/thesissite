/* NOTE: This code is based on the following tutorials:
    - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
    - http://www.dreisbach.us/blog/building-dashboards-with-django-and-d3/
    - http://nvd3.org/livecode/index.html#codemirrorNav
*/
var keys = Object.keys(week_graphs)

// make line graphs for all of the variables
for (i in keys) {
    make_bar_chart(keys[i]);
}


function make_bar_chart(key) {


    height = 250

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.multiBarChart()
        .showControls(false)
        .height(height);

        chart.xAxis
        .axisLabel('Week')
        .tickFormat(d3.format('.2f'))
        .rotateLabels(-45)
        ;

        chart.yAxis
        .tickFormat(d3.format('.2f'))
        ;

        // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
        d3.select("#" + key + " svg")
        .datum(week_graphs[key])
        .transition().duration(500)
        .call(chart).style({'height': height});

        nv.utils.windowResize(chart.update);

        return chart;
    });
}