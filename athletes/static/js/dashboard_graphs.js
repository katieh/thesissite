/* NOTE: This code is based on the following tutorials:
    - http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
    - http://www.dreisbach.us/blog/building-dashboards-with-django-and-d3/
    - http://nvd3.org/livecode/index.html#codemirrorNav
*/

// make line graphs for all of the variables
make_multichart(week_graphs['distance'], week_graphs['y_max']['distance'], 'distance');
make_multichart(week_graphs['sRPE'], week_graphs['y_max']['sRPE'], 'sRPE');

// graph tags
make_multichart_no_legend(tag_graphs['user_tags'], tag_graphs["y_max"]['user_tags'], 'user_tags')
make_multichart(tag_graphs['performance_injury'], tag_graphs["y_max"]['performance_injury'], 'performance_injury')


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

function make_multichart(data, y_max, key) {
    height = 250

    d3.selection.prototype.moveToFront = function() {
    return this.each(function(){
        this.parentNode.appendChild(this);
    });
    };

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.multiChart()
        .height(height);

        chart.xAxis
        .tickFormat(function(d) {
            return d3.time.format('%m/%d/%y')(new Date(d))
        })
        .rotateLabels(-45)
        ;

        chart.yAxis1
        .tickFormat(d3.format('.1f'));
        chart.yAxis2
        .tickFormat(d3.format('.2f'))
        ;

        chart.yDomain1([0, y_max])

        // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
        d3.select("#" + key + " svg")
        .datum(data)
        .transition().duration(500)
        .call(chart).style({'height': height});


        d3.select("#" + key + " svg" + ' .lines1Wrap').moveToFront();
        d3.select("#" + key + " svg" + ' .lines2Wrap').moveToFront();

        nv.utils.windowResize(chart.update);

        return chart;
    });
}

function make_multichart_no_legend(data, y_max, key) {
    height = 250;


    d3.selection.prototype.moveToBack = function() {  
        return this.each(function() { 
            var firstChild = this.parentNode.firstChild; 
            if (firstChild) { 
                this.parentNode.insertBefore(this, firstChild); 
            } 
        });
    };

    // make the graph with the appropriate key
    nv.addGraph(function() {

        var chart = nv.models.multiChart()
        .height(height)
        .showLegend(false);

        chart.xAxis
        .tickFormat(function(d) {
            return d3.time.format('%m/%d/%y')(new Date(d))
        })
        .rotateLabels(-45)
        ;

        chart.yAxis1
        .tickFormat(d3.format('.1f'))
        chart.yAxis2
        .tickFormat(d3.format('.2f'))
        ;

        chart.yDomain1([0, y_max])

        // modifide from http://stackoverflow.com/questions/9244824/how-to-remove-quot-from-my-json-in-javascript
        d3.select("#" + key + " svg")
        .datum(data)
        .transition().duration(500)
        .call(chart).style({'height': height});

        d3.select("#" + key + " svg" + ' .lines1Wrap').moveToBack();
        d3.select("#" + key + " svg" + ' .lines2Wrap').moveToBack();

        d3.select('#' + key + " svg" + " .y1").moveToBack();
        d3.select('#' + key + " svg" + " .y2").moveToBack();
        d3.select('#' + key + " svg" + " .x").moveToBack();

        // <g class="nvd3 nv-wrap nv-axis"><g><g class="tick major" transform="translate(135.69538926681784,0)" style="opacity: 1;"><line y2="-170" x2="0"></line><text y="5" dy=".71em" transform="rotate(-45 0,0)" x="0" style="text-anchor: end;">11/24/16</text></g><g class="tick major" transform="translate(234.31122448979593,0)" style="opacity: 1;"><line y2="-170" x2="0"></line><text y="5" dy=".71em" transform="rotate(-45 0,0)" x="0" style="text-anchor: end;">01/21/17</text></g><path class="domain" d="M0,0V0H334V0"></path><text class="nv-axislabel" text-anchor="middle" y="63.024096390102976" x="167"></text></g><g class="nv-axisMaxMin" transform="translate(0,0)"><text dy=".71em" y="5" transform="rotate(-45 0,0)" style="text-anchor: end;">09/05/16</text></g><g class="nv-axisMaxMin" transform="translate(334,0)"><text dy=".71em" y="5" transform="rotate(-45 0,0)" style="text-anchor: end;">03/20/17</text></g></g>


        nv.utils.windowResize(chart.update);

        return chart;
    });
}