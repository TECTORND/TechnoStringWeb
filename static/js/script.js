window.addEventListener('DOMContentLoaded', (event) => {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const darkModeLabel = document.querySelector('.dark-mode-label');

    // Function to toggle the sidebar open/close
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        menuToggle.classList.toggle('active');
    }

    // Function to set the dark mode preference in localStorage
    function setDarkModePreference(isDarkMode) {
        localStorage.setItem('darkMode', isDarkMode);
    }

    // Function to load the dark mode preference from localStorage
    function loadDarkModePreference() {
        return JSON.parse(localStorage.getItem('darkMode'));
    }

    // Function to toggle dark mode based on user interaction
    function toggleDarkMode() {
        const isDarkMode = loadDarkModePreference();

        if (isDarkMode) {
            document.documentElement.classList.add('dark-mode');
            darkModeToggle.checked = true;
            darkModeLabel.innerHTML = '<i class="bx bx-moon"></i> Light Mode';
        } else {
            document.documentElement.classList.remove('dark-mode');
            darkModeToggle.checked = false;
            darkModeLabel.innerHTML = '<i class="bx bx-sun"></i> Dark Mode';
        }
    }

    // Event listener for sidebar toggle
    menuToggle.addEventListener('click', function() {
        toggleSidebar();
        document.body.classList.toggle('menu-active');
        document.querySelector('.menu').classList.toggle('active');
    });

    // Event listener for dark mode toggle
    darkModeToggle.addEventListener('change', function() {
        const isDarkMode = this.checked;
        setDarkModePreference(isDarkMode);
        toggleDarkMode();
    });

    // Initialize menu state based on the saved preference
    toggleDarkMode();
});