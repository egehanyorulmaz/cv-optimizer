import pytest
from src.infrastructure.template_service.exceptions import (
    TemplateError,
    TemplateNotFoundError,
    TemplateRenderError,
)


def test_template_error_basic():
    """Test basic TemplateError functionality."""
    error_message = "Test error message"
    error = TemplateError(error_message)
    assert str(error) == error_message
    assert error.message == error_message


def test_template_not_found_error():
    """Test TemplateNotFoundError with and without search paths."""
    # Test without search paths
    template_name = "nonexistent.j2"
    error = TemplateNotFoundError(template_name)
    assert error.template_name == template_name
    assert error.search_paths is None
    assert str(error) == f"Template '{template_name}' not found"

    # Test with search paths
    search_paths = ["/path/1", "/path/2"]
    error_with_paths = TemplateNotFoundError(template_name, search_paths)
    assert error_with_paths.template_name == template_name
    assert error_with_paths.search_paths == search_paths
    assert str(error_with_paths) == (
        f"Template '{template_name}' not found. "
        f"Searched in: {', '.join(search_paths)}"
    )


def test_template_render_error():
    """Test TemplateRenderError with various configurations."""
    template_name = "test.j2"
    error_msg = "Syntax error"
    context = {"var1": "value1"}

    # Test without context
    error = TemplateRenderError(template_name, error_msg)
    assert error.template_name == template_name
    assert error.original_error == error_msg
    assert error.context is None
    assert str(error) == f"Failed to render template '{template_name}': {error_msg}"

    # Test with context
    error_with_context = TemplateRenderError(template_name, error_msg, context)
    assert error_with_context.template_name == template_name
    assert error_with_context.original_error == error_msg
    assert error_with_context.context == context
    assert str(error_with_context) == (
        f"Failed to render template '{template_name}': {error_msg}\n"
        f"Template context: {context}"
    ) 
