function renderChart(containerId, chartData) {
    console.log(chartData);
    try {
        // Map human-readable chart types to Chart.js types
        const chartTypeMap = {
            "bar chart": "bar",
            "line chart": "line",
            "pie chart": "pie",
            "doughnut": "doughnut",
            "single value": "single value"
        };

        // Normalize chart type
        const normalizedType = chartTypeMap[chartData.type];
        if (!normalizedType) {
            throw new Error(`Unsupported chart type: ${chartData.type}`);
        }

        // Validate data structure
        if (
            !chartData.data ||
            !Array.isArray(chartData.data.labels) ||
            !Array.isArray(chartData.data.datasets)
        ) {
            throw new Error("Invalid data structure: Ensure 'labels' and 'datasets' are arrays.");
        }

        // Handle heatmap or single value separately
        if (chartData.type === "heatmap" || chartData.type === "single value") {
            if (chartData.type === "heatmap") {
                console.error("Heatmap rendering not supported by Chart.js. Please use a heatmap library.");
            } else {
                const container = document.getElementById(containerId);
                if (!container) {
                    throw new Error(`Container with id '${containerId}' not found.`);
                }
                container.nextElementSibling.innerHTML = `<div class="pt-4" style="font-size: 48px; text-align: center; font-weight: bold">${chartData.data.datasets[0]?.data[0] ?? "N/A"}</
                div>`;
                container.nextElementSibling.style.display = 'block';
                container.style.display = 'none';
            }
            return;
        }

        // Color palette
        const colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", 
            "#FF9F40", "#FFCD56", "#C9CBCF", "#8DD1E1", "#D35D6E"
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
                        display: normalizedType !== "pie", // Hide legend for single-series pie charts
                    },
                },
            },
        });
    } catch (error) {
        console.log("Error rendering chart:", error);
    }
}

// Utility function to generate colors
function generateColors(count) {
    try {
        if (typeof count !== 'number' || count <= 0) {
            throw new Error('Invalid count for generating colors.');
        }
        const colors = [];
        for (let i = 0; i < count; i++) {
            colors.push(`rgba(${randomColor()}, ${randomColor()}, ${randomColor()}, 0.5)`);
        }
        return colors;
    } catch (error) {
        console.error(`Error generating colors: ${error.message}`);
        throw error;
    }
}

function randomColor() {
    return Math.floor(Math.random() * 256);
}

// Utility function for heatmap colors
function generateHeatmapColors(values) {
    try {
        if (!Array.isArray(values) || values.length === 0) {
            throw new Error('Values must be a non-empty array for heatmap.');
        }

        const max = Math.max(...values);
        const min = Math.min(...values);

        if (max === min) {
            throw new Error('All values are the same. Heatmap requires varying data.');
        }

        return values.map(value => {
            const intensity = (value - min) / (max - min); // Normalize
            return `rgba(255, ${255 - Math.round(255 * intensity)}, ${255 - Math.round(255 * intensity)}, 0.5)`;
        });
    } catch (error) {
        console.error(`Error generating heatmap colors: ${error.message}`);
        throw error;
    }
}
