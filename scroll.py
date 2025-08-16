# Function to scroll to column configuration section
def scroll_to_column_config(components):
    """Scroll to the column configuration section in the sidebar"""
    scroll_script = """
    <script>
    setTimeout(function() {
        // Try multiple selectors to find the column configuration section
        const selectors = [
            '[data-testid="stSidebar"] #column-config-anchor',
            '[data-testid="stSidebar"] h3:contains("⚙️ Column Configuration")',
            '[data-testid="stSidebar"] h3:contains("Column Configuration")',
            '[data-testid="stSidebar"] .element-container:has(h3:contains("Column Configuration"))'
        ];
        
        let element = null;
        for (let selector of selectors) {
            try {
                if (selector.includes(':contains')) {
                    // Handle :contains selector manually
                    const h3Elements = parent.document.querySelectorAll('[data-testid="stSidebar"] h3');
                    for (let h3 of h3Elements) {
                        if (h3.textContent.includes('Column Configuration')) {
                            element = h3;
                            break;
                        }
                    }
                } else {
                    element = parent.document.querySelector(selector);
                }
                if (element) break;
            } catch(e) {
                continue;
            }
        }
        
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }, 500);
    </script>
    """
    components.html(scroll_script, height=0)