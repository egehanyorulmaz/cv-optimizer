class TemplateError(Exception):
    """Base class for template-related exceptions"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TemplateNotFoundError(TemplateError):
    """Raised when a template file is not found"""
    def __init__(self, template_name: str, search_paths: list[str] = None):
        self.template_name = template_name
        self.search_paths = search_paths
        message = f"Template '{template_name}' not found"
        if search_paths:
            message += f". Searched in: {', '.join(search_paths)}"
        super().__init__(message)


class TemplateRenderError(TemplateError):
    """Raised when template rendering fails"""
    def __init__(self, template_name: str, error: str, context: dict = None):
        self.template_name = template_name
        self.original_error = error
        self.context = context
        message = f"Failed to render template '{template_name}': {error}"
        if context:
            message += f"\nTemplate context: {context}"
        super().__init__(message)