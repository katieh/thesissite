/* NOTE: This code is based on the following tutorials:
    - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
    - http://www.dreisbach.us/blog/building-dashboards-with-django-and-d3/
    - http://nvd3.org/livecode/index.html#codemirrorNav
*/

console.log("hi")

nv.addGraph(function() {

    // TODO: fix activity... we shouldn't have &quot there in the first place!
    console.log(activity)
    console.log(JSON.parse(activity.replace(/&quot;/g,'"')))
    console.log(data())

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
    d3.select('#chart svg')
    .datum(JSON.parse(activity.replace(/&quot;/g,'"')))
    .transition().duration(500)
    .call(chart)
    ;

    nv.utils.windowResize(chart.update);

    return chart;
});



function data() {
  var sin = [],
      cos = [];

  for (var i = 0; i < 100; i++) {
    sin.push({x: i, y: Math.sin(i/10)});
    cos.push({x: i, y: .5 * Math.cos(i/10)});
  }

  return [
    {
      values: sin,
      key: 'Sine Wave',
      color: '#ff7f0e'
    },
    {
      values: cos,
      key: 'Cosine Wave',
      color: '#2ca02c'
    }
  ];
}