// False: plot the number of people died or survived within each category
// True: plot the percentage of people died or survived within each category
var normalized = document.getElementById("normalized").checked;

// specify margin and size of the chart
var margin = {top: 40, right: 20, bottom: 40, left: 80},
    width = 900, height = 600;

var svg = dimple.newSvg("#chartContainer", width, height);

// load the data file and initialize the bar chart
var titanicData;
d3.csv("/data/titanic_modified.csv", function (data) {
  titanicData = data;
  createBarPlot();
});

// store proper text to label x axis of the bar chart
var categories = ['Gender', 'Passenger Class', 'Age Group',
                  'Number of Siblings/Spouses Abroad',
                  'Number of Parents/Children Abroad',
                  'Ticket Fare',
                  'Port of Embarkation'];

// create the bar chart when the page loads or when user selection changes
function createBarPlot() {
  // Find the checked radio button; store column name of the data file in
  // categoryVal; store the x axis label in categoryText
  var categoryVal, categoryText;
  var radios = document.forms['inputs'].categories
  for (var i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      categoryVal = radios[i].value;
      categoryText = categories[i];
    }
  }

  // clear the chart area to prepare for creating a new chart
  svg.selectAll('g').remove();

  // create a new bar chart
  var myChart = new dimple.chart(svg, titanicData);
  myChart.setBounds(margin.left, margin.top,
                    width - margin.left - margin.right,
                    height - margin.top - margin.bottom)

  // create x axis displaying categorical variables in the column categoryVal
  // loaded from the data file
  var x = myChart.addCategoryAxis("x", categoryVal);

  // show the categorical variable in proper order on x axis
  if (categoryVal === "AgeGroup") {
    x.addOrderRule(['Younger than 6', '6 to 15', '15 to 30', '30 to 40',
                    '40 to 50', '50 to 60', 'Older than 60']);
  } else if (categoryVal === 'FareGroup') {
    x.addOrderRule(['Less than 10', '10 to 20', '20 to 40', '40 to 100',
                    'More than 100']);
  } else {
    x.addOrderRule(categoryVal);
  }

  // Plot absolute count or percentage on y axis based on variable "normalized"
  if (normalized) {
    myChart.addPctAxis("y", "Count");
  } else {
    myChart.addMeasureAxis("y", "Count");
  }

  // display survived and died people count/percentage within each category
  myChart.addSeries("SurvivalStatus", dimple.plot.bar);
  myChart.assignColor("Survived", "#80b1d3", "#80b1d3", 0.8);
  myChart.assignColor("Died", "#fb8072", "#fb8072", 0.8);

  // format the legend properly
  legend = myChart.addLegend(margin.left, margin.top / 2,
                    width - margin.left - margin.right, 20, "right");
  legend.fontSize = "16px";

  // create the chart and make x/y axis display the correct labels
  // with proper font size
  myChart.draw(1000);
  svg.select('text.dimple-axis-x').text(categoryText);
  if (normalized) {
    svg.select('text.dimple-axis-y').text("Percentage");
  }
  svg.selectAll('text.dimple-custom-axis-title').style('font-size', '20px');
  svg.selectAll('text.dimple-custom-axis-label').style('font-size', '16px');
}

// When "Normalized" check box changed, re-create the chart based on its value
function normalizeYAxis(element) {
  normalized = element.checked;
  createBarPlot();
}
