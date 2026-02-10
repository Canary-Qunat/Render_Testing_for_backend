// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API Helper Functions
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        throw error;
    }
}

// API Functions
async function fetchProfile() {
    return await fetchAPI('/api/profile');
}

async function fetchHoldings() {
    return await fetchAPI('/api/holdings');
}

async function fetchPositions() {
    return await fetchAPI('/api/positions');
}

async function fetchSummary() {
    return await fetchAPI('/api/summary');
}
