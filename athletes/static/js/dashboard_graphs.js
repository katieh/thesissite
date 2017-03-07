/* NOTE: This code is based on the following tutorials:
    - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
    - http://www.dreisbach.us/blog/building-dashboards-with-django-and-d3/
    - http://nvd3.org/livecode/index.html#codemirrorNav
*/

console.log(tag_graphs)

var week_graphs_keys = Object.keys(week_graphs)

// make line graphs for all of the variables
for (i in week_graphs_keys) {
    make_bar_chart(week_graphs[week_graphs_keys[i]], week_graphs_keys[i]);
}

// graph tags
make_bar_chart(tag_graphs['user_tags'], 'user_tags')
make_bar_chart(tag_graphs['performance_injury'], 'performance_injury')

function make_line_chart(data, key) {
    height = 250

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.lineChart()
        .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
        .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
        .transitionDuration(350)  //how fast do you want the lines to transition?
        .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
        .showYAxis(true)        //Show the y-axis
        .showXAxis(true)        //Show the x-axis
        .height(height)

        chart.xAxis
        .axisLabel('Date')
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

function make_bar_chart(data, key) {


    height = 250

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.multiBarChart()
        .showControls(false)
        .height(height);

        chart.xAxis
        .axisLabel('Week')
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