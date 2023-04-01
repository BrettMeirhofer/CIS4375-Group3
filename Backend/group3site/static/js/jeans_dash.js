$(document).ready(function () {
	var mychart = $('#chart1')
	var ctx1 = mychart.get(0)

	var border_colors = [
		'rgba(255, 99, 132, 1)',
		'rgba(54, 162, 235, 1)',
		'rgba(255, 171, 86, 1)',
		'rgba(75, 192, 192, 1)',
		'rgba(153, 102, 255, 1)',
	]

	var back_colors = border_colors
	var url = $("#Product_Perf").attr("data-url");
	console.log(url)
	$.ajax({
        url: url,
        success: function (data) {
			const myChart = new Chart(ctx1, {
				type: 'bar',
				data: {
					labels: data.label,
					datasets: [{
						label: 'Total $',
						data: data.y,
						backgroundColor: back_colors,
						borderColor: border_colors,
						borderWidth: 1
					}]
				},
				options: {
					responsive: false,
					scales: {
						y: {

							beginAtZero: true,
							title: {
								display: true,
								text: "Transaction Total"
							},
							ticks: {
								beginAtZero: true,
								callback: function(value) {return "$" + value;}
							  }


						}
					},
					plugins: {
						title: {
							display: true,
							text: "Top 5 Cashiers By Transaction Total - last 30 days"
						},
						legend: {
							display: false
						}
					}
				}
			});

        }
    })
})



window.onload = function() {

var url = $("#Product_Perf").attr("data-url");
	console.log(url)
	$.ajax({
        url: url,
        success: function (data) {

const ctx = document.getElementById('chart1');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
});
}