from typing import Protocol, Any, Dict
from abc import abstractmethod

class TemplateService(Protocol):
    """
    Port interface for template rendering services.
    
    This port defines the contract for template services that handle
    prompt templates and other templated content in the application.
    """
    
    @abstractmethod
    def render_prompt(self, template_name: str, **kwargs: Dict[str, Any]) -> str:
        """
        Render a template with the given context variables.
        
        :param template_name: Name or path of the template to render
        :type template_name: str
        :param kwargs: Variables to pass to the template
        :type kwargs: Dict[str, Any]
        :return: Rendered template string
        :rtype: str
        :raises TemplateNotFoundError: If template doesn't exist
        :raises TemplateRenderError: If rendering fails
        """
        pass

    @abstractmethod
    def get_template_names(self) -> list[str]:
        """
        Get list of available template names.
        
        :return: List of template names
        :rtype: list[str]
        """
        pass

    @abstractmethod
    def validate_template(self, template_name: str) -> bool:
        """
        Validate if a template exists and is well-formed.
        
        :param template_name: Name of the template to validate
        :type template_name: str
        :return: True if template is valid, False otherwise
        :rtype: bool
        """
        pass 