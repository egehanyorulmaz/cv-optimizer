import pytest
from pathlib import Path
from cv_optimizer.core.domain.constants import PROJECT_ROOT
from cv_optimizer.core.domain.config import TemplateConfig
from cv_optimizer.infrastructure.template_service.jinja_template_service import JinjaTemplateService
from cv_optimizer.infrastructure.template_service.exceptions import (
    TemplateNotFoundError,
    TemplateRenderError,
)


@pytest.fixture
def template_dir(tmp_path):
    """
    Create a temporary directory with test templates.
    
    :param tmp_path: Pytest temporary path fixture
    :type tmp_path: Path
    :returns: Path to template directory
    :rtype: Path
    """
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    
    # Create a valid template
    valid_template = template_dir / "valid_template.j2"
    valid_template.write_text("Hello {{ name }}!")
    
    # Create an invalid template (Missing closing brace)
    invalid_template = template_dir / "invalid_template.j2"
    invalid_template.write_text("Hello {{ name }!") 
    
    return template_dir


@pytest.fixture
def template_service(template_dir):
    """
    Create a JinjaTemplateService instance with test templates.
    
    :param template_dir: Path to template directory
    :type template_dir: Path
    :returns: Configured template service
    :rtype: JinjaTemplateService
    """
    config = TemplateConfig.testing(templates_dir=template_dir)
    return JinjaTemplateService(config)


def test_template_not_found(template_service):
    """
    Test handling of non-existent templates.
    
    :param template_service: Template service instance
    :type template_service: JinjaTemplateService
    :raises TemplateNotFoundError: Expected to be raised
    """
    with pytest.raises(TemplateNotFoundError) as exc_info:
        # Pass kwargs correctly using unpacking
        template_service.render_prompt("nonexistent.j2", **{"dummy": "value"})
    
    assert exc_info.value.template_name == "nonexistent.j2"
    assert isinstance(exc_info.value.search_paths, list)


def test_successful_template_rendering(template_service):
    """
    Test successful template rendering.
    
    :param template_service: Template service instance
    :type template_service: JinjaTemplateService
    """
    result = template_service.render_prompt(
        "valid_template.j2",
        **{"name": "World"}  # Use kwargs unpacking
    )
    assert result == "Hello World!"


def test_with_real_templates():
    """Test using actual project templates."""
    config = TemplateConfig.default()
    service = JinjaTemplateService(config)
    
    # Test with actual resume parsing template
    result = service.render_prompt(
        "prompts/parsing/resume_extraction.j2",
        text="Sample Resume",
        schema={"type": "object"}
    )
    assert "Sample Resume" in result