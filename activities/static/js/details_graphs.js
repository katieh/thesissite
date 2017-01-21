/* NOTE: This code is based on the following tutorials:
    - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
    - http://www.dreisbach.us/blog/building-dashboards-with-django-and-d3/
    - http://nvd3.org/livecode/index.html#codemirrorNav
*/

// TODO: fix resizing bug!!

height = 250

/* speed graph */
nv.addGraph(function() {

    var chart = nv.models.lineChart()
    .useInteractiveGuideline(true)
    ;

    chart.xAxis
    .axisLabel('Distance')
    .tickFormat(d3.format('d'))
    ;

    chart.yAxis
    .axisLabel('Speed (mph)')
    .tickFormat(d3.format('.2f'))
    ;

    // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
    d3.select('#speed_chart svg')
    .datum(JSON.parse(speed.replace(/&quot;/g,'"')))
    .transition().duration(500)
    .call(chart).style({'height': height });
    ;

    nv.utils.windowResize(chart.update);

    return chart;
});

/* heartrate graph */
nv.addGraph(function() {

    // // TODO: fix activity... we shouldn't have &quot there in the first place!
    // console.log(activity)
    // console.log(JSON.parse(activity.replace(/&quot;/g,'"')))
    // console.log(data())

    var chart = nv.models.lineChart()
    .useInteractiveGuideline(true)
    ;

    chart.xAxis
    .axisLabel('Distance')
    .tickFormat(d3.format('d'))
    ;

    chart.yAxis
    .axisLabel('Heart Rate (bpm)')
    .tickFormat(d3.format('d'))
    ;

    // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
    d3.select('#heartrate_chart svg')
    .datum(JSON.parse(heartrate.replace(/&quot;/g,'"')))
    .transition().duration(500)
    .call(chart).style({'height': height });
    ;

    nv.utils.windowResize(chart.update);

    return chart;
});

/* altitude graph */
nv.addGraph(function() {

    // // TODO: fix activity... we shouldn't have &quot there in the first place!
    // console.log(activity)
    // console.log(JSON.parse(activity.replace(/&quot;/g,'"')))
    // console.log(data())

    var chart = nv.models.lineChart()
    .useInteractiveGuideline(true)
    ;

    chart.xAxis
    .axisLabel('Distance')
    .tickFormat(d3.format('d'))
    ;

    chart.yAxis
    .axisLabel('Altitude (meters)')
    .tickFormat(d3.format('.2f'))
    ;

    // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
    d3.select('#altitude_chart svg')
    .datum(JSON.parse(altitude.replace(/&quot;/g,'"')))
    .transition().duration(500)
    .call(chart).style({'height': height });
    ;

    nv.utils.windowResize(chart.update);

    return chart;
});

/* cadence graph */
nv.addGraph(function() {

    // // TODO: fix activity... we shouldn't have &quot there in the first place!
    // console.log(activity)
    // console.log(JSON.parse(activity.replace(/&quot;/g,'"')))
    // console.log(data())

    var chart = nv.models.lineChart()
    .useInteractiveGuideline(true)
    ;

    chart.xAxis
    .axisLabel('Distance')
    .tickFormat(d3.format('d'))
    ;

    chart.yAxis
    .axisLabel('Cadence (spm)')
    .tickFormat(d3.format('d'))
    ;

    // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
    d3.select('#cadence_chart svg')
    .datum(JSON.parse(cadence.replace(/&quot;/g,'"')))
    .transition().duration(500)
    .call(chart).style({'height': height });
    ;

    nv.utils.windowResize(chart.update);

    return chart;
});