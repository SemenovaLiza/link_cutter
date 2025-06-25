// this file is to be updated
function submitForm(event) {
    event.preventDefault();
    const form = document.getElementById('link_form');
    const formData = new FormData(form);

    fetch('/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const linkContainer = document.getElementById('new_link');
            if (linkContainer) {
                linkContainer.href = `${window.location.origin}/${data.custom_id}`;
                linkContainer.textContent = `${window.location.origin}/${data.custom_id}`;
                linkContainer.parentElement.style.display = 'block';
            }
            form.reset();
        } else {
            console.error('Form submission failed:', data.errors || data.message);
            
            const errorDiv = document.createElement('div');
            errorDiv.style.color = 'red';
            errorDiv.style.textAlign = 'center';
            errorDiv.textContent = data.message || 'Form submission failed';
            
            form.parentNode.insertBefore(errorDiv, form);
            
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
    })
    .catch(error => {
        console.error('Error during form submission:', error);
        
        const errorDiv = document.createElement('div');
        errorDiv.style.color = 'red';
        errorDiv.style.textAlign = 'center';
        errorDiv.textContent = error.message;
        
        form.parentNode.insertBefore(errorDiv, form);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    });
}

class FallingLinks {
    constructor() {
      this.container = document.getElementById('fallingLinks');
      this.linkTexts = [];
      this.isRunning = false;
      this.animationInterval = null;
      
      // Fallback texts in case API fails
      this.fallbackTexts = [
        'JavaScript', 'HTML', 'CSS', 'React', 'Node.js',
        'Python', 'Web Dev', 'Frontend', 'Backend', 'API',
        'Database', 'Framework', 'Library', 'Code', 'Debug'
      ];
      
      this.colors = [
        '#ff6b6b', '#4ecdc4', '#45b7d1', '#f7dc6f',
        '#bb6bd9', '#fd79a8', '#fdcb6e', '#6c5ce7',
        '#a29bfe', '#fd79a8', '#55a3ff', '#26de81',
        '#ffeaa7', '#fab1a0', '#ff7675'
      ];
      
      this.loadLinksFromDatabase();
    }
  
    async loadLinksFromDatabase() {
      try {
        const response = await fetch('/api/links');
        const data = await response.json();
        
        if (data.links && data.links.length > 0) {
          this.linkTexts = data.links;
        }
      } catch (error) {
        console.error('Error occurred while loading data from database:', error);
        this.linkTexts = [...this.fallbackTexts];
      }
      if (this.linkTexts.length === 0) {
        this.linkTexts = [...this.fallbackTexts];
      }
  
      this.init();
    }
  
    init() {
      if (this.isRunning) {
        return;
      }
      if (!this.container) {
        console.error('Container with id "fallingLinks" not found');
        return;
      }
      if (this.linkTexts.length === 0) {
        console.error('No link texts available to display');
        return;
      }
  
      this.isRunning = true;
  
      for (let i = 0; i < Math.min(this.colors.length, 10); i++) {
        setTimeout(() => {
          this.createFallingLink();
        }, i * 800);
      }
  
      this.animationInterval = setInterval(() => {
        this.createFallingLink();
      }, 2000);
    }
  
    createFallingLink() {
      if (!this.container) {
        this.stop();
        return;
      }
  
      const link = document.createElement('div');
      const animationDuration = 8 + Math.random() * 4;
      
      link.className = 'falling-link';
      link.textContent = this.linkTexts[Math.floor(Math.random() * this.linkTexts.length)];
      link.style.background = this.colors[Math.floor(Math.random() * this.colors.length)];
      link.style.color = 'white';
      
      link.style.left = Math.random() * 100 + '%';
      link.style.fontSize = (10 + Math.random() * 6) + 'px';
      link.style.animationDuration = animationDuration + 's';
      link.style.animationDelay = Math.random() * 2 + 's';
      
      link.style.position = 'absolute';
      link.style.padding = '8px 12px';
      link.style.borderRadius = '20px';
      link.style.fontWeight = 'bold';
      link.style.textShadow = '0 1px 2px rgba(0,0,0,0.3)';
      link.style.userSelect = 'none';
      link.style.pointerEvents = 'none';
  
      this.container.appendChild(link);
  
      setTimeout(() => {
        if (link && link.parentNode) {
          link.parentNode.removeChild(link);
        }
      }, (animationDuration + 2) * 1000);
    }
  
    stop() {
      this.isRunning = false;
      if (this.animationInterval) {
        clearInterval(this.animationInterval);
        this.animationInterval = null;
      }
    }
  
    restart() {
      this.stop();
      setTimeout(() => {
        this.init();
      }, 100);
    }
  
    updateLinkTexts(newTexts) {
      if (Array.isArray(newTexts) && newTexts.length > 0) {
        this.linkTexts = [...newTexts];
      }
    }
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    window.fallingLinksInstance = new FallingLinks();
  });
  
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.form-control').forEach(input => {
      input.addEventListener('focus', function() {
        this.style.transform = 'translateY(-2px)';
        this.style.transition = 'all 0.2s ease';
        this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
      });
      
      input.addEventListener('blur', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'none';
      });
    });
  });