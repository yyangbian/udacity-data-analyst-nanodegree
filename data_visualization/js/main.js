var normalized = document.getElementById("normalized").checked;
var margin = {top: 40, right: 20, bottom: 40, left: 80},
    width = 750, height = 400;

var svg = dimple.newSvg("#chartContainer", width, height);
var myChart;
var titanicData;
d3.csv("data/titanic_modified.csv", function (data) {
  titanicData = data;
  createBarPlot();
});

var categories = ['Gender', 'Passenger Class', 'Age Group',
                  'Number of Siblings/Spouses Abroad',
                  'Number of Parents/Children Abroad',
                  'Ticket Fare',
                  'Port of Embarkation'];

function createBarPlot() {
  var categoryVal, categoryText;
  radios = document.forms['inputs'].categories
  for (var i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      categoryVal = radios[i].value;
      categoryText = categories[i];
    }
  }
  svg.selectAll('g').remove();
  myChart = new dimple.chart(svg, titanicData);
  myChart.setBounds(margin.left, margin.top,
                    width - margin.left - margin.right,
                    height - margin.top - margin.bottom)
  var x = myChart.addCategoryAxis("x", categoryVal);
  if (categoryVal === "AgeGroup") {
    x.addOrderRule(['Younger than 6', '6 to 15', '15 to 30', '30 to 40',
                    '40 to 50', '50 to 60', 'Older than 60']);
  } else if (categoryVal === 'FareGroup') {
    x.addOrderRule(['Less than 10', '10 to 20', '20 to 40', '40 to 100',
                    'More than 100']);
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
  svg.selectAll('text.dimple-custom-axis-title').style('font-size', '18px');
  svg.selectAll('text.dimple-custom-axis-label').style('font-size', '14px');
}

function normalizeYAxis(element) {
  normalized = element.checked;
  createBarPlot();
}
