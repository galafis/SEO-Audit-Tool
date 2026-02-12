"""
Unit tests for SEO-Audit-Tool
Auto-generated test scaffold — extend with project-specific tests
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import seo_audit
    HAS_SEO_AUDIT = True
except ImportError:
    HAS_SEO_AUDIT = False


class TestProjectStructure:
    """Test project structure and configuration."""
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        readme = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
        assert os.path.isfile(readme), "README.md should exist"
    
    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        req = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")
        assert os.path.isfile(req), "requirements.txt should exist"
    
    def test_license_exists(self):
        """Test that LICENSE exists."""
        lic = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LICENSE")
        assert os.path.isfile(lic), "LICENSE should exist"

class TestSeoAudit:
    """Tests for seo_audit module."""
    
    def test_module_imports(self):
        """Test that the module can be imported."""
        assert HAS_SEO_AUDIT, "Module seo_audit should be importable"
    
    def test_module_has_attributes(self):
        """Test that the module has expected attributes."""
        if HAS_SEO_AUDIT:
            assert hasattr(seo_audit, '__name__')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
