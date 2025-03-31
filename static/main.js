import { socialLinks } from './config.js';

const socialContainer = document.getElementById('social-buttons');

socialLinks.forEach(({ name, url, icon, username }) => {
    const link = document.createElement('a');
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.className = "social-link";
    
    const tooltip = document.createElement('div');
    tooltip.className = "username-tooltip";
    tooltip.textContent = username;
    
    const iconContainer = document.createElement('div');
    iconContainer.className = "social-icon";
    iconContainer.innerHTML = icon;
    
    link.appendChild(tooltip);
    link.appendChild(iconContainer);
    socialContainer.appendChild(link);
});

