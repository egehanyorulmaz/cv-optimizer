from typing import Any
import logging
from jinja2 import Environment, FileSystemLoader
import jinja2

from src.core.ports.secondary.template_service import TemplateService
from src.core.domain.config import TemplateConfig
from src.infrastructure.template.exceptions import TemplateNotFoundError, TemplateRenderError

logger = logging.getLogger(__name__)

class JinjaTemplateService(TemplateService):
    """
    Jinja implementation of the template service.
    
    :param config: Configuration for the template service
    :type config: TemplateConfig
    """
    def __init__(self, config: TemplateConfig):
        """Initialize the Jinja template service.
        
        :param config: Template service configuration
        :type config: TemplateConfig
        :raises ValueError: If templates directory doesn't exist
        """
        if not config.templates_dir.exists():
            raise ValueError(f"Templates directory not found: {config.templates_dir}")

        self._env = Environment(
            loader=FileSystemLoader(
                searchpath=str(config.templates_dir),
                encoding=config.default_encoding
            ),
            enable_async=False,
            auto_reload=config.auto_reload
        )
        logger.info(f"Loaded templates: {self.get_template_names()}")

    def render_prompt(self, template_name: str, **kwargs: Any) -> str:
        """
        Render a template with the given context variables.
        
        Supports templates in subfolders using path notation, e.g.:
        'prompts/parsing/resume_parsing.j2'
        
        :param template_name: Template path relative to templates_dir
        :type template_name: str
        :param kwargs: Template context variables
        :type kwargs: Any
        :returns: Rendered template string
        :rtype: str
        :raises TemplateNotFoundError: If template doesn't exist
        :raises TemplateRenderError: If rendering fails
        """
        try:
            template = self._env.get_template(template_name)
            return template.render(**kwargs)
        except jinja2.exceptions.TemplateNotFound as e:
            search_paths = [str(path) for path in self._env.loader.searchpath]
            raise TemplateNotFoundError(template_name, search_paths) from e
        except Exception as e:
            raise TemplateRenderError(template_name, str(e), kwargs) from e

    def get_template_names(self) -> list[str]:
        """Get list of all available templates, including those in subfolders.
        
        :return: List of template paths relative to templates_dir
        :rtype: list[str]
        """
        return self._env.list_templates()

    def validate_template(self, template_name: str) -> bool:
        """
        Validate if a template exists and is well-formed.
        
        :param template_name: Template path relative to templates_dir
        :type template_name: str
        :return: True if template is valid, False otherwise
        """
        try:
            self._env.get_template(template_name)
            return True
        except Exception:
            logger.warning(f"Template {template_name} is not valid")
            return False

    def add_filter(self, name: str, filter_func: callable) -> None:
        """
        Add a custom filter to the template environment.
        
        :param name: Name of the filter
        :param filter_func: Filter function
        """
        self._env.filters[name] = filter_func

if __name__ == "__main__":
    jinja_template_service = JinjaTemplateService(config=TemplateConfig.default())
    print(jinja_template_service.get_template_names())
