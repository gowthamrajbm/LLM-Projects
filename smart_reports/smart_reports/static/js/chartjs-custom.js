function renderChart(containerId, chartData) {
    try {
        console.log(chartData)
        // Map human-readable chart types to Chart.js types and custom rendering
        const chartTypeMap = {
            "bar chart": "bar",
            "line chart": "line",
            "pie chart": "pie",
            "doughnut": "doughnut",
            "single value": "single value",
            "table": "table", // New table chart type
        };

        // Normalize chart type
        const normalizedType = chartTypeMap[chartData.type];
        if (!normalizedType) {
            throw new Error(`Unsupported chart type: ${chartData.type}`);
        }
        
        const container = chartData.type === "table" ? document.getElementById(containerId+"-nc") : document.getElementById(containerId);
        // Handle specific types of charts
        if (chartData.type === "heatmap" || chartData.type === "single value") {
            if (chartData.type === "heatmap") {
                console.error("Heatmap rendering not supported by Chart.js. Please use a heatmap library.");
            } else {
                if (!container) {
                    throw new Error(`Container with id '${containerId}' not found.`);
                }
                container.nextElementSibling.innerHTML = `<div class="pt-4" style="font-size: 48px; text-align: center; font-weight: bold">${chartData.data.datasets[0]?.data[0] ?? "N/A"}</div>`;
                container.nextElementSibling.style.display = 'block';
                container.style.display = 'none';
            }
            return;
        }

        // Handle table chart rendering
        if (chartData.type === "table") {
            document.getElementById(containerId).style.display = "none";
            if (!container) {
                throw new Error(`Container with id '${containerId}' not found.`);
            }

            // Create table dynamically
            let tableHTML = `<table class="min-w-full border-collapse border border-gray-200 text-sm text-left">
                                <thead>
                                    <tr>`;

            // Add headers from labels
            chartData.data.labels.forEach(label => {
                tableHTML += `<th class="border border-gray-200 px-4 py-2">${label}</th>`;
            });
            tableHTML += `</tr></thead><tbody>`;

            // Add rows from dataset data
            //console.log(chartData.data.datasets[0].data)
            chartData.data.datasets[0].data.forEach(dataset => {
                tableHTML += `<tr>`;
                if(!!dataset && dataset.constructor === Array)                    
                    dataset.forEach(value => {
                        tableHTML += `<td class="border border-gray-200 px-4 py-2">${value}</td>`;
                    });
                else
                    tableHTML += `<td class="border border-gray-200 px-4 py-2">${dataset}</td>`;
                
                tableHTML += `</tr>`;
            });

            tableHTML += `</tbody></table>`;

            // Insert table into the container
            container.innerHTML = tableHTML;
            return;
        }

        // Color palette
        const colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
            "#FF9F40", "#FFCD56", "#C9CBCF", "#8DD1E1", "#D35D6E",
        ];

        // Dynamically assign colors
        chartData.data.datasets = chartData.data.datasets.map((dataset, index) => {
            const colorIndex = index % colors.length;
            return {
                ...dataset,
                backgroundColor: Array.isArray(dataset.data)
                    ? dataset.data.map((_, i) => colors[i % colors.length]) // Assign color for each data point
                    : colors[colorIndex],
                borderColor: Array.isArray(dataset.data)
                    ? dataset.data.map((_, i) => colors[i % colors.length])
                    : colors[colorIndex],
                borderWidth: 1,
            };
        });

        // Render the chart
        const ctx = document.getElementById(containerId)?.getContext("2d");
        if (!ctx) {
            throw new Error(`Canvas with id '${containerId}' not found or invalid.`);
        }

        new Chart(ctx, {
            type: normalizedType,
            data: {
                labels: chartData.data.labels,
                datasets: chartData.data.datasets,
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true, // Ensure the legend is visible
                        position: 'top', // Adjust the legend position
                        labels: {
                            font: {
                                size: 12, // Adjust font size for readability
                            },
                            color: "#000", // Legend label color
                        },
                    },
                },
                scales: normalizedType === 'bar' || normalizedType === 'line'
                    ? {
                          x: {
                              beginAtZero: true,
                          },
                          y: {
                              beginAtZero: true,
                          },
                      }
                    : {}, // Scales only for bar/line charts
            },
        });
    } catch (error) {
        console.log("Error rendering chart:", error);
    }
}
