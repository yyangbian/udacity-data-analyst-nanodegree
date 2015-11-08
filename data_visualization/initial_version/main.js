var normalized = document.getElementById("normalized").checked;
var margin = {top: 40, right: 20, bottom: 40, left: 80},
    width = 900, height = 600;

var svg = dimple.newSvg("#chartContainer", width, height);
var myChart;
var titanicData;
d3.csv("titanic_modified.csv", function (data) {
  titanicData = data;
  createBarPlot();
});

function switchData() {
  createBarPlot();
}

function createBarPlot() {
  var e = document.getElementById('metric');
  var categoryVal = e.options[e.selectedIndex].value;
  var categoryText = e.options[e.selectedIndex].text;
  svg.selectAll('g').remove();
  myChart = new dimple.chart(svg, titanicData);
  myChart.setBounds(margin.left, margin.top,
                    width - margin.left - margin.right,
                    height - margin.top - margin.bottom)
  var x = myChart.addCategoryAxis("x", categoryVal);
  if (categoryVal === "AgeGroup") {
    x.addOrderRule(['Younger than 6', '6 to 15', '15 to 30', '30 to 40',
                    '40 to 50', '50 to 60', 'Older than 60']);
  } else {
    x.addOrderRule(categoryVal);
  }
  if (normalized) {
    myChart.addPctAxis("y", "Count");
  } else {
    myChart.addMeasureAxis("y", "Count");
  }
  myChart.addSeries("SurvivalStatus", dimple.plot.bar);
  myChart.assignColor("Survived", "#80b1d3", "#80b1d3", 0.8);
  myChart.assignColor("Died", "#fb8072", "#fb8072", 0.8);
  legend = myChart.addLegend(margin.left, margin.top / 2,
                    width - margin.left - margin.right, 20, "right");
  legend.fontSize = "16px";
  myChart.draw(1000);
  svg.select('text.dimple-axis-x').text(categoryText);
  if (normalized) {
    svg.select('text.dimple-axis-y').text("Percentage");
  }
  svg.selectAll('text.dimple-custom-axis-title').style('font-size', '20px');
  svg.selectAll('text.dimple-custom-axis-label').style('font-size', '16px');

  svg.append("text")
          .attr("class", "chart-title")
          .attr("x", (width / 2))
          .attr("y", (margin.top / 2))
          .attr("text-anchor", "middle")
          .style("font-size", '24px')
          .text("Titanic Passenger Data");
}

function normalizeYAxis(element) {
  console.log('normalize');
  normalized = element.checked;
  createBarPlot();
}
