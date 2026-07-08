import os
from jinja2 import Environment, FileSystemLoader
from app.core.logger import logger

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates", "emails"))

class EmailTemplates:
    @staticmethod
    def render_template(template_name: str, context: dict) -> str:
        """
        Renders a Jinja2 HTML email template.
        """
        try:
            os.makedirs(TEMPLATES_DIR, exist_ok=True)
            env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
            template = env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering Jinja2 template {template_name}: {e}")
            # Fallback inline layout if loading fails
            return f"<h3>Traffic Alert</h3><p>{str(context)}</p>"
