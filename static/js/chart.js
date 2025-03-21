// This file contains shared chart functions for the CodeCracker application
// It will be expanded as more visualization needs arise

/**
 * Creates a heatmap visualization for problem-solving activity
 * @param {string} elementId - The ID of the DOM element to render the chart in
 * @param {Object} data - The data for the heatmap
 */
function createActivityHeatmap(elementId, data) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Process data for heatmap format
    const processedData = processHeatmapData(data);

    // Create the heatmap using Plotly
    const layout = {
        title: 'Problem Solving Activity',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ffffff' },
        xaxis: {
            title: 'Day of Week',
            tickvals: [0, 1, 2, 3, 4, 5, 6],
            ticktext: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        },
        yaxis: {
            title: 'Week',
            autorange: 'reversed'
        }
    };

    Plotly.newPlot(elementId, [{
        z: processedData.values,
        x: processedData.x,
        y: processedData.y,
        type: 'heatmap',
        colorscale: 'Blues'
    }], layout);
}

/**
 * Creates a radar chart for showing strengths across problem categories
 * @param {string} elementId - The ID of the DOM element to render the chart in
 * @param {Object} data - The data for the radar chart
 */
function createStrengthsRadarChart(elementId, data) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, Math.max(...Object.values(data.values)) + 5]
            }
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ffffff' },
        showlegend: false
    };

    Plotly.newPlot(elementId, [{
        type: 'scatterpolar',
        r: Object.values(data.values),
        theta: Object.keys(data.values),
        fill: 'toself',
        name: 'Problem Categories',
        line: { color: 'rgb(31, 119, 180)' },
        fillcolor: 'rgba(31, 119, 180, 0.5)'
    }], layout);
}

/**
 * Creates a line chart for tracking progress over time
 * @param {string} elementId - The ID of the DOM element to render the chart in
 * @param {Object} data - The data for the line chart
 */
function createProgressLineChart(elementId, data) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const layout = {
        title: data.title || 'Progress Over Time',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ffffff' },
        xaxis: { title: 'Date' },
        yaxis: { title: data.yAxisTitle || 'Value' },
        legend: { orientation: 'h', y: -0.2 }
    };

    const traces = data.series.map(series => {
        return {
            x: series.dates,
            y: series.values,
            type: 'scatter',
            mode: 'lines+markers',
            name: series.name,
            line: { color: series.color, width: 3 },
            marker: { size: 8 }
        };
    });

    Plotly.newPlot(elementId, traces, layout);
}

/**
 * Process raw data into format needed for the heatmap
 * @param {Object} rawData - The raw data from the API
 * @returns {Object} Processed data for heatmap
 */
function processHeatmapData(rawData) {
    // This is a placeholder implementation
    // In a real app, you would process actual submission data

    // Create a 7x12 grid (days x weeks) with random values
    const weeks = 12;
    const values = [];

    for (let i = 0; i < weeks; i++) {
        const week = [];
        for (let j = 0; j < 7; j++) {
            // Generate random values between 0-5 with higher probability for 0
            const rand = Math.random();
            let val = 0;
            if (rand > 0.6) val = 1;
            if (rand > 0.75) val = 2;
            if (rand > 0.85) val = 3;
            if (rand > 0.92) val = 4;
            if (rand > 0.97) val = 5;
            week.push(val);
        }
        values.push(week);
    }

    // Create x and y labels
    const x = [0, 1, 2, 3, 4, 5, 6]; // Days of week
    const y = Array.from({length: weeks}, (_, i) => `Week ${i+1}`);

    return { values, x, y };
}