// with common_top5 and similarity_top5 being defined already in JS as list of list pairs: [[game name: occurances], ..]

commonGames = common_top5.map(list_pair => list_pair[0]); // Not using {} for single expressions is equivalent to {return list_pair[0]}
commonOccurances = common_top5.map(list_pair => list_pair[1]);

similarityGames = similarity_top5.map(list_pair => list_pair[0]);
similarityOccurances = similarity_top5.map(list_pair => list_pair[1]);

// Function to create pie chart
function createPieChart(ctx, labels, data) {
    const chart_data = {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
            ],
            hoverOffset: 5,
        }]
    }

    const options = {
        responsive: true,
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart',
            animateScale: true,
            animateRotate: true,
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: context => ' ' + context.parsed + ' out of top 20 users love this game'
                },
            },
        },
    }

    const config = {
        type: 'doughnut',
        data: chart_data,
        options: options,
    };

    new Chart(ctx, config)
}

// Get canvas elements
const commonCanvas = document.getElementById("commonPieChart");
const similarityCanvas = document.getElementById("similarityPieChart");

// Create pie charts
createPieChart(commonCanvas, commonGames, commonOccurances);
createPieChart(similarityCanvas, similarityGames, similarityOccurances);