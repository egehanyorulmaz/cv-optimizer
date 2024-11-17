from typing import Any, Dict
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound

from cv_optimizer.core.ports.template_service import TemplateService
from cv_optimizer.core.domain.config import TemplateConfig
from cv_optimizer.infrastructure.template_service.exceptions import TemplateNotFoundError, TemplateRenderError

logger = logging.getLogger(__name__)

class JinjaTemplateService(TemplateService):
    """
    Jinja2 implementation of the template service.
    
    :param config: Template configuration
    :type config: TemplateConfig
    """
    
    def __init__(self, config: TemplateConfig):
        """Initialize the Jinja2 template service."""
        self.config = config
        self.env = Environment(
            loader=FileSystemLoader(
                str(config.templates_dir),
                encoding=config.default_encoding
            ),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            auto_reload=config.auto_reload,
            cache_size=200 if config.cache_enabled else 0
        )
        
        # Add custom filters if needed
        self.env.filters['clean_whitespace'] = lambda x: ' '.join(x.split())

    def render_prompt(self, template_name: str, **kwargs: Dict[str, Any]) -> str:
        """
        Render a prompt template with the given context.
        
        :raises TemplateNotFoundError: If template doesn't exist
        :raises TemplateRenderError: If rendering fails
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except TemplateNotFound:
            logger.error(f"Template not found: {template_name}")
            raise TemplateNotFoundError(template_name)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {str(e)}")
            raise TemplateRenderError(template_name, str(e))

    def get_template_names(self) -> list[str]:
        """Get list of available template names."""
        return self.env.list_templates()

    def validate_template(self, template_name: str) -> bool:
        """
        Validate if a template exists and is well-formed.
        
        :param template_name: Name of the template to validate
        :return: True if template is valid, False otherwise
        """
        try:
            self.env.get_template(template_name)
            return True
        except Exception as e:
            logger.warning(f"Template validation failed for {template_name}: {str(e)}")
            return False

    def add_filter(self, name: str, filter_func: callable) -> None:
        """
        Add a custom filter to the template environment.
        
        :param name: Name of the filter
        :param filter_func: Filter function
        """
        self.env.filters[name] = filter_func

if __name__ == "__main__":
    jinja_template_service = JinjaTemplateService(config=TemplateConfig.default())
    print(jinja_template_service.get_template_names())
