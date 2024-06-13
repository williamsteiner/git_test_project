document.getElementById('stockForm').addEventListener('submit', fetchStockPrices);

async function fetchStockPrices(event) {
    event.preventDefault();

    const stockSymbol = document.getElementById('stockSymbol').value;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading...';

    try {
        const response = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${stockSymbol}?range=1y&interval=1mo`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        displayStockPrices(data, resultsDiv);
    } catch (error) {
        resultsDiv.innerHTML = `Failed to fetch data: ${error.message}`;
    }
}

function displayStockPrices(data, resultsDiv) {
    if (!data.chart.result || data.chart.result.length === 0) {
        resultsDiv.innerHTML = 'No data available.';
        return;
    }

    const timestamps = data.chart.result[0].timestamp;
    const prices = data.chart.result[0].indicators.quote[0].close;

    let html = '<h2>Monthly Prices (in USD)</h2><ul>';
    for (let i = 0; i < timestamps.length; i++) {
        const date = new Date(timestamps[i] * 1000);
        const year = date.getFullYear();
        const month = date.getMonth() + 1; // getMonth() returns 0-indexed month
        const price = prices[i];
        html += `<li>${year}-${month.toString().padStart(2, '0')}: ${price.toFixed(2)}</li>`;
    }
    html += '</ul>';

    resultsDiv.innerHTML = html;
}
