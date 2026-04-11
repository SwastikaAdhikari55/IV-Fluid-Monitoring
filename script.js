// IV Monitoring System - Frontend Script
// Handles all frontend interactions and API communication

// ============================================================
// CONFIGURATION
// ============================================================
const CONFIG = {
    API_URL: 'http://localhost:8000',
    DEVICE_ID: 'device_001',
    REFRESH_INTERVAL: 5000 // 5 seconds
};

// ============================================================
// STATE MANAGEMENT
// ============================================================
let STATE = {
    isMonitoring: false,
    refreshInterval: null,
    currentData: null,
    alerts: []
};

// ============================================================
// NOTIFICATION FUNCTIONS
// ============================================================
function toggleNotificationDropdown() {
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) {
        dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const bellContainer = document.getElementById('notificationBellContainer');
    const dropdown = document.getElementById('notificationDropdown');
    if (bellContainer && dropdown && !bellContainer.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});

// ============================================================
// API FUNCTIONS
// ============================================================
async function fetchAlerts() {
    try {
        const response = await fetch(`${CONFIG.API_URL}/alerts?device_id=${CONFIG.DEVICE_ID}`);
        if (!response.ok) return [];
        const data = await response.json();
        return data.map(alert => ({
            id: alert.id,
            message: alert.message,
            alert_type: alert.alert_type,
            timestamp: alert.triggered_at
        }));
    } catch (error) {
        console.error('Error fetching alerts:', error);
        return [];
    }
}

async function fetchDashboard() {
    try {
        const response = await fetch(`${CONFIG.API_URL}/dashboard?device_id=${CONFIG.DEVICE_ID}`);
        if (!response.ok) return null;
        const data = await response.json();
        return data[0] || null;
    } catch (error) {
        console.error('Error fetching dashboard:', error);
        return null;
    }
}

// ============================================================
// UPDATE FUNCTIONS
// ============================================================
async function updateNotifications() {
    const alerts = await fetchAlerts();
    const notificationCount = document.getElementById('notificationCount');
    const dropdownAlertCount = document.getElementById('dropdownAlertCount');
    const notificationItems = document.getElementById('notificationItems');

    // Update counts
    if (notificationCount) notificationCount.textContent = alerts.length;
    if (dropdownAlertCount) dropdownAlertCount.textContent = alerts.length;

    // Update notification items
    if (notificationItems) {
        if (alerts.length === 0) {
            notificationItems.innerHTML = `
                <div style="padding: 40px 16px; text-align: center; color: #999;">
                    <div style="font-size: 28px; margin-bottom: 8px;">✓</div>
                    <p style="font-size: 13px;">No active alerts</p>
                </div>
            `;
        } else {
            notificationItems.innerHTML = alerts.map(alert => {
                const timestamp = new Date(alert.timestamp).toLocaleTimeString();
                const iconMap = {
                    'critical': '🔴',
                    'warning': '⚠️',
                    'info': 'ℹ️'
                };
                const typeMap = {
                    'critical': 'critical',
                    'warning': 'warning',
                    'info': 'info'
                };
                const icon = iconMap[alert.alert_type] || 'ℹ️';
                const typeClass = typeMap[alert.alert_type] || 'info';
                const title = alert.alert_type === 'critical' ? 'CRITICAL ALERT' : alert.alert_type === 'warning' ? 'WARNING' : 'INFO';

                return `
                    <div style="padding: 14px 16px; border-bottom: 1px solid #f5f5f5; display: flex; gap: 12px; align-items: flex-start; transition: background 0.2s ease;">
                        <div style="font-size: 18px; min-width: 28px; display: flex; align-items: center; justify-content: center;">${icon}</div>
                        <div style="flex: 1; min-width: 0;">
                            <div style="font-size: 13px; font-weight: 600; color: #333; margin-bottom: 4px;">${title}</div>
                            <div style="font-size: 12px; color: #666; margin-bottom: 6px; line-height: 1.4;">${alert.message}</div>
                            <div style="font-size: 11px; color: #999;">${timestamp}</div>
                        </div>
                    </div>
                `;
            }).join('');
        }
    }

    STATE.alerts = alerts;
}

async function updateDashboard() {
    const data = await fetchDashboard();
    if (!data) return;

    STATE.currentData = data;

    // Update dashboard elements if they exist
    if (document.getElementById('ivLevel')) {
        document.getElementById('ivLevel').textContent = Math.round(data.current_iv_level || 0);
    }
    if (document.getElementById('dripRate')) {
        document.getElementById('dripRate').textContent = Math.round(data.current_drip_rate || 0);
    }
    if (document.getElementById('status')) {
        const statusText = data.status_color === 'green' ? 'Normal' : data.status_color === 'yellow' ? 'Warning' : 'Critical';
        document.getElementById('status').textContent = statusText;
    }
}

// ============================================================
// MONITORING FUNCTIONS
// ============================================================
function startMonitoring() {
    STATE.isMonitoring = true;
    
    // Update immediately
    updateNotifications();
    updateDashboard();
    
    // Then set interval
    STATE.refreshInterval = setInterval(() => {
        updateNotifications();
        updateDashboard();
    }, CONFIG.REFRESH_INTERVAL);

    console.log('Monitoring started');
}

function stopMonitoring() {
    STATE.isMonitoring = false;
    if (STATE.refreshInterval) {
        clearInterval(STATE.refreshInterval);
        STATE.refreshInterval = null;
    }
    console.log('Monitoring stopped');
}

async function resetAlerts() {
    try {
        // Refresh alerts from server
        await updateNotifications();
        console.log('Alerts refreshed');
    } catch (error) {
        console.error('Error resetting alerts:', error);
    }
}

// ============================================================
// PAGE NAVIGATION
// ============================================================
function switchTab(tabName, event) {
    if (event) {
        event.preventDefault();
    }

    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Update menu links
    const menuLinks = document.querySelectorAll('.menu-link');
    menuLinks.forEach(link => {
        link.parentElement.classList.remove('active');
    });
    event.target.closest('.menu-item').classList.add('active');
}

// ============================================================
// SETTINGS FUNCTIONS
// ============================================================
function saveSettings() {
    alert('Settings saved successfully!');
}

function resetSettings() {
    alert('Settings reset to default!');
}

// ============================================================
// INITIALIZATION
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('IV Monitoring System loaded');
    
    // Initial notification update
    updateNotifications();
    updateDashboard();
    
    // Optional: Auto-start monitoring
    // startMonitoring();
});

// Auto-update notifications periodically
setInterval(updateNotifications, 10000); // Update notifications every 10 seconds
