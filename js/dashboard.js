// Dashboard Logic

// Format currency
function formatCurrency(value) {
    return `₹${parseFloat(value).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Format number
function formatNumber(value) {
    return parseFloat(value).toLocaleString('en-IN');
}

// Show/Hide elements
function showElement(id) {
    document.getElementById(id).style.display = 'block';
}

function hideElement(id) {
    document.getElementById(id).style.display = 'none';
}

// Display error
function displayError(message) {
    hideElement('loading');
    hideElement('main-content');
    document.getElementById('error-text').textContent = message;
    showElement('error');
}

// Load all dashboard data
async function loadDashboard() {
    try {
        showElement('loading');
        hideElement('error');
        hideElement('main-content');

        // Fetch all data
        const [profile, holdings, positions, summary] = await Promise.all([
            fetchProfile(),
            fetchHoldings(),
            fetchPositions(),
            fetchSummary()
        ]);

        // Display profile
        if (profile && profile.user_name) {
            document.getElementById('user-name').textContent = profile.user_name;
        }

        // Display summary
        displaySummary(summary);

        // Display holdings
        displayHoldings(holdings);

        // Display positions
        displayPositions(positions);

        // Show main content
        hideElement('loading');
        showElement('main-content');

    } catch (error) {
        console.error('Error loading dashboard:', error);
        displayError('Failed to load dashboard data. Please try logging in again.');
    }
}

// Display summary cards
function displaySummary(summary) {
    if (!summary) return;

    document.getElementById('total-value').textContent = formatCurrency(summary.total_value || 0);

    const totalPnl = summary.total_pnl || 0;
    const pnlElement = document.getElementById('total-pnl');
    pnlElement.textContent = formatCurrency(totalPnl);
    pnlElement.className = `value ${totalPnl >= 0 ? 'positive' : 'negative'}`;

    document.getElementById('holdings-count').textContent = summary.holdings_count || 0;
    document.getElementById('positions-count').textContent = summary.positions_count || 0;
}

// Display holdings table
function displayHoldings(holdings) {
    const tbody = document.getElementById('holdings-body');

    if (!holdings || holdings.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="no-data">No holdings found</td></tr>';
        return;
    }

    tbody.innerHTML = holdings.map(holding => {
        const quantity = holding.quantity || 0;
        const avgPrice = holding.average_price || 0;
        const lastPrice = holding.last_price || 0;
        const currentValue = lastPrice * quantity;
        const investedValue = avgPrice * quantity;
        const pnl = currentValue - investedValue;

        return `
            <tr>
                <td><strong>${holding.tradingsymbol || 'N/A'}</strong></td>
                <td>${formatNumber(quantity)}</td>
                <td>${formatCurrency(avgPrice)}</td>
                <td>${formatCurrency(lastPrice)}</td>
                <td>${formatCurrency(currentValue)}</td>
                <td class="${pnl >= 0 ? 'positive' : 'negative'}">${formatCurrency(pnl)}</td>
            </tr>
        `;
    }).join('');
}

// Display positions table
function displayPositions(positions) {
    const tbody = document.getElementById('positions-body');

    // Get net positions
    const netPositions = positions?.net || [];

    if (netPositions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="no-data">No positions found</td></tr>';
        return;
    }

    tbody.innerHTML = netPositions.map(position => {
        const pnl = position.pnl || 0;

        return `
            <tr>
                <td><strong>${position.tradingsymbol || 'N/A'}</strong></td>
                <td>${formatNumber(position.quantity || 0)}</td>
                <td>${formatCurrency(position.average_price || 0)}</td>
                <td>${formatCurrency(position.last_price || 0)}</td>
                <td class="${pnl >= 0 ? 'positive' : 'negative'}">${formatCurrency(pnl)}</td>
            </tr>
        `;
    }).join('');
}

// Refresh data
async function refreshData() {
    await loadDashboard();
}

// Logout
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = 'index.html';
    }
}

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', loadDashboard);
