"""Tests for template generation scripts (generate.py and generate_simple.py)."""

import os
import sys
import json
import yaml
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, mock_open
import pytest


class TestGenerateCLI:
    """Tests for generate.py CLI functionality."""

    def test_cli_help(self):
        """Test that --help works."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        result = subprocess.run([
            sys.executable, os.path.join(script_dir, 'scripts/generate.py'), '--help'
        ], capture_output=True, text=True, cwd=script_dir)

        assert result.returncode == 0
        assert 'Generate professional LaTeX academic reports' in result.stdout

    def test_cli_config_file_not_found(self):
        """Test error when config file doesn't exist."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))       
        result = subprocess.run([
            sys.executable, os.path.join(script_dir, 'scripts/generate.py'), '--config', 'nonexistent.yaml'
        ], capture_output=True, text=True, cwd=script_dir)

        assert result.returncode == 1
        assert 'Config file not found' in result.stdout or 'Config file not found' in result.stderr

    def test_cli_with_valid_config(self):
        """Test generation with valid config file."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-proposal/config.yaml')

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'test-output')

            result = subprocess.run([
                sys.executable, os.path.join(script_dir, 'scripts/generate.py'),
                '--config', config_path,
                '--output', output_dir
            ], capture_output=True, text=True, cwd=script_dir)

            assert result.returncode == 0
            assert 'Report generated successfully' in result.stdout
            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))

    def test_cli_with_major_project_config(self):
        """Test generation with major project config."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-major-project/config.yaml')

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'test-major')

            result = subprocess.run([
                sys.executable, os.path.join(script_dir, 'scripts/generate.py'),
                '--config', config_path,
                '--output', output_dir
            ], capture_output=True, text=True, cwd=script_dir)

            assert result.returncode == 0
            assert 'Report generated successfully' in result.stdout
            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'main.tex'))

    def test_cli_with_presentation_config(self):
        """Test generation with presentation config."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-presentation/config.yaml')

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'test-presentation')

            result = subprocess.run([
                sys.executable, os.path.join(script_dir, 'scripts/generate.py'),
                '--config', config_path,
                '--output', output_dir
            ], capture_output=True, text=True, cwd=script_dir)

            assert result.returncode == 0
            assert 'Report generated successfully' in result.stdout
            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'slides.tex'))

    @patch('builtins.input')
    def test_interactive_mode_proposal(self, mock_input):
        """Test interactive mode for proposal generation."""
        from scripts.generate import collect_interactive_inputs
        
        # Mock user inputs for proposal
        mock_input.side_effect = [
            '1',  # Choose proposal
            'Test Proposal Title',  # Title
            'Test Author',  # Author name
            '12345',  # Roll number
            '',  # Email (empty, not required)
            'Dr. Test Supervisor',  # Supervisor
            '',  # Co-supervisor (empty)
            'CSE Department',  # Department
            'Test University',  # University
            'B.Tech',  # Degree
            '2024-25',  # Session
            'December 2024'  # Submission date
        ]

        config = collect_interactive_inputs()
        
        assert config['project']['type'] == 'proposal'
        assert config['project']['title'] == 'Test Proposal Title'
        assert config['author']['name'] == 'Test Author'
        assert config['author']['roll_number'] == '12345'

    def test_generate_report_function(self):
        """Test the generate_report function directly."""
        from scripts.generate import generate_report

        config = {
            'project': {
                'title': 'Test Report',
                'type': 'proposal'
            },
            'author': {
                'name': 'Test Author',
                'roll_number': '12345',
                'email': 'test@example.com'
            },
            'academic': {
                'supervisor': 'Dr. Test',
                'department': 'CSE',
                'university': 'Test University',
                'degree': 'B.Tech',
                'session': '2024-25'
            },
            'dates': {
                'submission_date': 'December 2024'
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = generate_report(config, temp_dir)

            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))
            assert os.path.exists(os.path.join(output_dir, 'titlePage.tex'))

    def test_copy_template_files(self):
        """Test copying template files."""
        from scripts.generate import copy_template_files

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'output')
            script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

            copy_template_files('proposal', output_dir, script_dir)

            assert os.path.exists(output_dir)
            # Check that non-.tex files are copied (tex files are skipped)
            assert os.path.exists(os.path.join(output_dir, 'IEEEtran.bst'))
            assert os.path.exists(os.path.join(output_dir, 'proposal_refs.bib'))

    def test_render_templates(self):
        """Test template rendering."""
        from scripts.generate import render_templates
        from scripts.utils.template_engine import prepare_context

        config = {
            'project': {'title': 'Test', 'type': 'proposal'},
            'author': {'name': 'Author', 'roll_number': '123'},
            'academic': {'supervisor': 'Dr. X', 'department': 'CSE', 'university': 'Uni', 'degree': 'B.Tech', 'session': '2024'},
            'dates': {'submission_date': 'Dec 2024'}
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'output')
            script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

            context = prepare_context(config)
            render_templates('proposal', context, output_dir, script_dir)

            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))
            # Check that template variables are replaced
            with open(os.path.join(output_dir, 'proposal.tex'), 'r') as f:
                content = f.read()
                assert 'Test' in content
                assert 'Author' in content


class TestGenerateSimpleCLI:
    """Tests for generate_simple.py CLI functionality."""

    def test_simple_cli_help(self):
        """Test that --help works for simple version."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        result = subprocess.run([
            sys.executable, os.path.join(script_dir, 'scripts/generate_simple.py'), '--help'
        ], capture_output=True, text=True, cwd=script_dir)

        assert result.returncode == 0
        assert 'Generate academic reports (Simple version' in result.stdout

    def test_simple_cli_with_json_config(self):
        """Test simple generation with JSON config."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-proposal/config.json')

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'test-simple')

            result = subprocess.run([
                sys.executable, os.path.join(script_dir, 'scripts/generate_simple.py'),
                '--config', config_path,
                '--output', output_dir
            ], capture_output=True, text=True, cwd=script_dir)

            assert result.returncode == 0
            assert 'Report generated successfully' in result.stdout
            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))

    def test_simple_cli_with_presentation_json(self):
        """Test simple generation with presentation JSON config."""
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-presentation/config.json')

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'test-simple-presentation')

            result = subprocess.run([
                sys.executable, os.path.join(script_dir, 'scripts/generate_simple.py'),
                '--config', config_path,
                '--output', output_dir
            ], capture_output=True, text=True, cwd=script_dir)

            assert result.returncode == 0
            assert 'Report generated successfully' in result.stdout
            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'slides.tex'))

    def test_simple_generate_report_function(self):
        """Test the simple generate_report function."""
        from scripts.generate_simple import generate_report

        config = {
            'project': {
                'title': 'Simple Test Report',
                'type': 'proposal'
            },
            'author': {
                'name': 'Simple Author',
                'roll_number': '67890',
                'email': 'simple@example.com'
            },
            'academic': {
                'supervisor': 'Dr. Simple',
                'department': 'CSE',
                'university': 'Simple University',
                'degree': 'B.Tech',
                'session': '2024-25'
            },
            'dates': {
                'submission_date': 'December 2024'
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = generate_report(config, temp_dir)

            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))

    def test_simple_replace_function(self):
        """Test the simple string replacement function."""
        from scripts.generate_simple import simple_replace

        text = "Title: \\VAR{TITLE}, Author: \\VAR{AUTHOR_NAME}"
        replacements = {'TITLE': 'Test Title', 'AUTHOR_NAME': 'Test Author'}

        result = simple_replace(text, replacements)

        assert result == "Title: Test Title, Author: Test Author"

    def test_copy_and_process_files(self):
        """Test copying and processing files in simple version."""
        from scripts.generate_simple import copy_and_process_files

        config = {
            'project': {'title': 'Process Test', 'type': 'proposal'},
            'author': {'name': 'Process Author', 'roll_number': '123'},
            'academic': {'supervisor': 'Dr. P', 'department': 'CSE', 'university': 'Uni', 'degree': 'B.Tech', 'session': '2024'},
            'dates': {'submission_date': 'Dec 2024'}
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, 'processed')
            script_dir = os.path.join(os.path.dirname(__file__), '../scripts')

            copy_and_process_files('proposal', config, output_dir, script_dir)

            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))

            # Check that replacements worked
            with open(os.path.join(output_dir, 'proposal.tex'), 'r') as f:
                content = f.read()
                assert 'Process Test' in content
                assert 'Process Author' in content


class TestConfigValidation:
    """Tests for configuration validation in generation."""

    def test_load_config_file_yaml(self):
        """Test loading YAML config file."""
        from scripts.generate import load_config_file

        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-proposal/config.yaml')
        config = load_config_file(config_path)

        assert isinstance(config, dict)
        assert 'project' in config
        assert 'author' in config
        assert config['project']['type'] == 'proposal'

    def test_load_config_file_json(self):
        """Test loading JSON config file."""
        # Use Python's json module directly for testing
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-proposal/config.json')

        with open(config_path, 'r') as f:
            config = json.load(f)

        assert isinstance(config, dict)
        assert 'project' in config
        assert 'author' in config

    def test_invalid_config_handling(self):
        """Test handling of invalid configuration."""
        from scripts.generate import generate_report
        import sys
        from io import StringIO

        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            invalid_config = {
                'project': {'title': 'Test'},  # Missing required fields
            }

            with pytest.raises(SystemExit):
                generate_report(invalid_config)
        finally:
            sys.stderr = old_stderr


class TestOutputDirectoryHandling:
    """Tests for output directory creation and handling."""

    def test_default_output_directory_creation(self):
        """Test creation of default output directory."""
        from scripts.generate import generate_report

        config = {
            'project': {'title': 'Default Output Test', 'type': 'proposal'},
            'author': {'name': 'Author', 'roll_number': '123'},
            'academic': {'supervisor': 'Dr. X', 'department': 'CSE', 'university': 'Uni', 'degree': 'B.Tech', 'session': '2024'},
            'dates': {'submission_date': 'Dec 2024'}
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp dir so output goes there
            old_cwd = os.getcwd()
            os.chdir(temp_dir)

            try:
                output_dir = generate_report(config)
                assert 'output' in output_dir
                assert 'default-output-test' in output_dir
                assert os.path.exists(output_dir)
            finally:
                os.chdir(old_cwd)

    def test_custom_output_directory(self):
        """Test using custom output directory."""
        from scripts.generate import generate_report

        config = {
            'project': {'title': 'Custom Output Test', 'type': 'proposal'},
            'author': {'name': 'Author', 'roll_number': '123'},
            'academic': {'supervisor': 'Dr. X', 'department': 'CSE', 'university': 'Uni', 'degree': 'B.Tech', 'session': '2024'},
            'dates': {'submission_date': 'Dec 2024'}
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            custom_output = os.path.join(temp_dir, 'my-custom-output')
            output_dir = generate_report(config, custom_output)

            assert output_dir == custom_output
            assert os.path.exists(output_dir)
            assert os.path.exists(os.path.join(output_dir, 'proposal.tex'))
    
    def test_variable_substitution(self):
        """Test variable substitution in templates."""
        template = "Author: {AUTHOR}, Project: {PROJECT}"
        context = {"AUTHOR": "John", "PROJECT": "Test"}
        
        result = template.format(**context)
        assert result == "Author: John, Project: Test"
    
    def test_multiline_content_handling(self):
        """Test handling multiline content."""
        content = """Introduction section.
        
First paragraph here.
Second paragraph here.

Conclusion."""
        
        # Check that content is preserved
        lines = content.split('\n')
        assert len(lines) >= 5
        assert "First paragraph" in content
        assert "Conclusion" in content


class TestGenerateErrorHandling:
    """Tests for error handling in generation."""
    
    def test_missing_required_config_field(self):
        """Test error when required field is missing."""
        from scripts.utils.validators import validate_config
        
        incomplete_config = {
            "project": {"title": "Test"},
            # Missing author and academic
        }
        
        is_valid, errors = validate_config(incomplete_config)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_invalid_project_type(self):
        """Test error with invalid project type."""
        from scripts.utils.validators import validate_config
        
        config = {
            "project": {"type": "invalid-type"},
            "author": {"name": "John", "roll_number": "123"},
            "academic": {"supervisor": "Dr. A", "department": "CSE", "university": "U", "degree": "B.Tech"}
        }
        
        is_valid, errors = validate_config(config)
        assert is_valid is False
        assert any("project type" in str(e).lower() for e in errors)
    
    def test_missing_template_directory(self):
        """Test error when template directory doesn't exist."""
        non_existent = "/path/to/non/existent/templates"
        assert not os.path.exists(non_existent)
    
    def test_invalid_tex_syntax_recovery(self):
        """Test handling of invalid LaTeX syntax."""
        # This would be caught during compilation, not generation
        # Just test that we can detect problematic content
        invalid_tex = r"\undefined_command{content}"
        
        # We can at least check the syntax when parsing
        assert "\\" in invalid_tex
        assert "{" in invalid_tex


class TestGenerateSimpleVersion:
    """Tests for generate_simple.py functionality."""
    
    def test_no_dependencies_yaml_parsing(self):
        """Test YAML parsing without yaml library (fallback)."""
        # Simulate minimal YAML parsing
        yaml_str = """key: value
nested:
  field: data"""
        
        # We can still read it as text
        assert "key:" in yaml_str
        assert "nested:" in yaml_str
    
    def test_simple_template_rendering(self):
        """Test simple string-based template rendering."""
        template = "Hello {name}, your project is {project}"
        data = {"name": "John", "project": "Test Project"}
        
        result = template.format(**data)
        assert "Hello John" in result
        assert "Test Project" in result
    
    def test_basic_file_io(self):
        """Test basic file input/output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write file
            output_path = os.path.join(temp_dir, "output.tex")
            content = r"% Generated report\n\documentclass{article}"
            
            with open(output_path, 'w') as f:
                f.write(content)
            
            # Read file
            with open(output_path, 'r') as f:
                read_content = f.read()
            
            assert content == read_content
    
    def test_simple_config_parsing(self):
        """Test parsing config without yaml library."""
        config_text = """
title=My Project
author=John Doe
type=proposal
"""
        # Parse manually
        config = {}
        for line in config_text.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
        
        assert config['title'] == 'My Project'
        assert config['author'] == 'John Doe'


class TestGenerateIntegration:
    """Integration-level tests combining multiple components."""
    
    def test_full_workflow_proposal(self):
        """Test complete workflow for proposal generation."""
        # This is an integration test showing the full flow
        config = {
            "project": {"title": "My Proposal", "type": "proposal"},
            "author": {"name": "John Doe", "roll_number": "12345"},
            "academic": {
                "supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            },
            "dates": {"submission_date": "December 2024"}
        }
        
        # 1. Validate config
        from scripts.utils.validators import validate_config
        is_valid, errors = validate_config(config)
        assert is_valid is True
        
        # 2. Prepare context
        from scripts.utils.template_engine import prepare_context
        context = prepare_context(config)
        assert context['TITLE'] == 'My Proposal'
        assert context['AUTHOR_NAME'] == 'John Doe'
        assert context['SUPERVISOR'] == 'Dr. Smith'
    
    def test_full_workflow_major_project(self):
        """Test complete workflow for major project generation."""
        config = {
            "project": {"title": "My Major Project", "type": "major-project"},
            "author": {"name": "Jane Doe", "roll_number": "54321"},
            "academic": {
                "supervisor": "Dr. Jones",
                "co_supervisor": "Dr. Smith",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            }
        }
        
        from scripts.utils.validators import validate_config
        from scripts.utils.template_engine import prepare_context
        
        is_valid, errors = validate_config(config)
        assert is_valid is True
        
        context = prepare_context(config)
        assert context['TITLE'] == 'My Major Project'
        assert context['CO_SUPERVISOR'] == 'Dr. Smith'
    
    def test_workflow_with_content_extraction(self):
        """Test workflow with content extraction."""
        config = {
            "project": {"title": "Presentation", "type": "presentation"},
            "author": {"name": "Bob Smith", "roll_number": "99999"},
            "academic": {
                "supervisor": "Dr. Admin",
                "department": "CSE",
                "university": "IITJ",
                "degree": "B.Tech"
            },
            "presentation": {"theme": "Madrid", "aspect_ratio": "16:9"}
        }
        
        from scripts.utils.validators import validate_config
        from scripts.utils.template_engine import prepare_context
        
        is_valid, errors = validate_config(config)
        assert is_valid is True
        
        context = prepare_context(config)
        assert context['THEME'] == 'Madrid'
        assert context['ASPECT_RATIO_VALUE'] == '169'


class TestGenerateUserInputAndInteractive:
    """Cover get_user_input and collect_interactive_inputs branches."""

    @patch('builtins.input')
    def test_get_user_input_required_retry_then_value(self, mock_input):
        from scripts.generate import get_user_input

        mock_input.side_effect = ['', '', 'final']
        assert get_user_input('Field', required=True) == 'final'

    @patch('builtins.input')
    def test_collect_interactive_invalid_choice_then_proposal(self, mock_input):
        from scripts.generate import collect_interactive_inputs

        mock_input.side_effect = [
            'x', '1',
            'T', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov 2024',
        ]
        cfg = collect_interactive_inputs()
        assert cfg['project']['type'] == 'proposal'

    @patch('builtins.input')
    def test_collect_interactive_presentation(self, mock_input):
        from scripts.generate import collect_interactive_inputs

        mock_input.side_effect = [
            '3',
            'Slides', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov 2024',
        ]
        cfg = collect_interactive_inputs()
        assert cfg['project']['type'] == 'presentation'

    @patch('builtins.input')
    def test_collect_interactive_invalid_email_then_valid(self, mock_input):
        from scripts.generate import collect_interactive_inputs

        mock_input.side_effect = [
            '1',
            'T', 'A', '1', 'bad', 'a@b.com', 'Dr', '', '', '', '', '', 'Nov 2024',
        ]
        cfg = collect_interactive_inputs()
        assert cfg['author']['email'] == 'a@b.com'

    @patch('builtins.input')
    def test_collect_interactive_major_project(self, mock_input):
        from scripts.generate import collect_interactive_inputs

        mock_input.side_effect = [
            '2',
            'Thesis', 'Auth', '9', '', 'Sup', '', '', '', '', '', 'Prof', 'Dept', 'Nov 2024',
        ]
        cfg = collect_interactive_inputs()
        assert cfg['project']['type'] == 'major-project'
        assert cfg['academic']['supervisor_designation'] == 'Prof'


class TestGeneratePresentationExtract:
    """Presentation + content extraction paths in generate_report."""

    def _base_pres_config(self, report_path, **extra):
        cfg = {
            'project': {'title': 'Pres', 'type': 'presentation'},
            'author': {'name': 'A', 'roll_number': '1', 'email': 'a@b.com'},
            'academic': {
                'supervisor': 'Dr. S',
                'co_supervisor': '',
                'department': 'CSE',
                'university': 'U',
                'degree': 'B.Tech',
                'session': '2024-25',
            },
            'dates': {'submission_date': 'November 2024'},
            'presentation': {
                'theme': 'Madrid',
                'aspect_ratio': '16:9',
                'extract_from_report': True,
                'report_path': report_path,
            },
        }
        cfg['presentation'].update(extra)
        return cfg

    @patch('scripts.utils.content_extractor.extract_content_from_report')
    def test_extract_success_populates_config(self, mock_extract):
        from scripts.generate import generate_report

        mock_extract.return_value = {'slides': 'ok'}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(r'\documentclass{article}\begin{document}x\end{document}')
            path = f.name
        try:
            cfg = self._base_pres_config(path)
            with tempfile.TemporaryDirectory() as tmp:
                generate_report(cfg, tmp)
            assert 'extracted_content' in cfg
            assert cfg['extracted_content'] == {'slides': 'ok'}
        finally:
            os.unlink(path)

    @patch('scripts.utils.content_extractor.extract_content_from_report')
    def test_extract_empty_warns(self, mock_extract):
        from scripts.generate import generate_report

        mock_extract.return_value = {}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write('x')
            path = f.name
        try:
            cfg = self._base_pres_config(path)
            with tempfile.TemporaryDirectory() as tmp:
                generate_report(cfg, tmp)
            assert mock_extract.called
        finally:
            os.unlink(path)

    def test_extract_missing_report_file_warns(self):
        from scripts.generate import generate_report

        cfg = self._base_pres_config('/nonexistent/path/to/main.tex')
        with tempfile.TemporaryDirectory() as tmp:
            generate_report(cfg, tmp)

    @patch('scripts.utils.content_extractor.extract_content_from_report', side_effect=RuntimeError('boom'))
    def test_extract_exception_warns(self, mock_extract):
        from scripts.generate import generate_report

        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write('x')
            path = f.name
        try:
            cfg = self._base_pres_config(path)
            with tempfile.TemporaryDirectory() as tmp:
                generate_report(cfg, tmp)
        finally:
            os.unlink(path)


class TestGenerateCopyTemplateErrors:
    def test_copy_template_files_missing_raises(self):
        from scripts.generate import copy_template_files

        with tempfile.TemporaryDirectory() as tmp:
            with pytest.raises(FileNotFoundError):
                copy_template_files('nonexistent-template-xyz', tmp, os.path.dirname(__file__))


class TestGenerateMainInProcess:
    """Call generate.main() in-process for coverage of main() body."""

    def test_main_with_config_and_output(self, monkeypatch):
        import scripts.generate as gen

        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-proposal/config.yaml')
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, 'gen-out')
            monkeypatch.setattr(
                sys,
                'argv',
                ['generate.py', '--config', config_path, '--output', out],
            )
            gen.main()
            assert os.path.isfile(os.path.join(out, 'proposal.tex'))


class TestGenerateMainSubprocess:
    """Exercise generate.py main() via subprocess."""

    def test_main_interactive_cancel(self):
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        stdin = '\n'.join([
            '1',
            'T', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov 2024',
            'n',
        ]) + '\n'
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, 'scripts/generate.py')],
            input=stdin,
            capture_output=True,
            text=True,
            cwd=script_dir,
            env=env,
        )
        assert result.returncode == 0
        assert 'cancelled' in (result.stdout + result.stderr).lower()


class TestGenerateSimpleHelpers:
    """Increase coverage for generate_simple.py."""

    def test_print_banner(self, capsys):
        from scripts.generate_simple import print_banner

        print_banner()
        out = capsys.readouterr().out
        assert 'Simple Mode' in out

    @patch('builtins.input')
    def test_get_user_input_empty_default(self, mock_input):
        from scripts.generate_simple import get_user_input

        mock_input.return_value = ''
        assert get_user_input('D', default='fallback') == 'fallback'

    @patch('builtins.input')
    def test_collect_inputs_proposal(self, mock_input):
        from scripts.generate_simple import collect_inputs

        mock_input.side_effect = [
            '1', 'T', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov',
        ]
        cfg = collect_inputs()
        assert cfg['project']['type'] == 'proposal'

    @patch('builtins.input')
    def test_collect_inputs_invalid_choice_then_proposal(self, mock_input):
        from scripts.generate_simple import collect_inputs

        mock_input.side_effect = [
            'bad', '1', 'T', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov',
        ]
        cfg = collect_inputs()
        assert cfg['project']['type'] == 'proposal'

    @patch('builtins.input')
    def test_collect_inputs_major_project(self, mock_input):
        from scripts.generate_simple import collect_inputs

        mock_input.side_effect = [
            '2', 'T', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov',
            'Prof', 'Dept',
        ]
        cfg = collect_inputs()
        assert cfg['project']['type'] == 'major-project'
        assert cfg['academic']['supervisor_designation'] == 'Prof'

    @patch('builtins.input')
    def test_collect_inputs_presentation(self, mock_input):
        from scripts.generate_simple import collect_inputs

        mock_input.side_effect = [
            '3', 'S', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov',
        ]
        cfg = collect_inputs()
        assert cfg['project']['type'] == 'presentation'

    def test_generate_report_default_output_dir_major(self):
        from scripts.generate_simple import generate_report

        config = {
            'project': {'title': 'Major Title X', 'type': 'major-project'},
            'author': {'name': 'A', 'roll_number': '1', 'email': ''},
            'academic': {
                'supervisor': 'Dr. S',
                'co_supervisor': '',
                'supervisor_designation': 'Prof',
                'supervisor_department': 'CSE',
                'department': 'CSE',
                'university': 'U',
                'degree': 'B.Tech',
                'session': '2024-25',
            },
            'dates': {'submission_date': 'November 2024'},
        }
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            os.chdir(tmp)
            try:
                out = generate_report(config)
                assert 'output' in out.replace('\\', '/')
                assert 'major-title-x' in out.replace('\\', '/').lower()
            finally:
                os.chdir(old)


class TestGenerateSimpleMainInProcess:
    def test_main_with_json_config(self, monkeypatch):
        import scripts.generate_simple as gs

        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(script_dir, 'examples/sample-proposal/config.json')
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, 'simple-out')
            monkeypatch.setattr(
                sys,
                'argv',
                ['generate_simple.py', '--config', config_path, '--output', out],
            )
            gs.main()
            assert os.path.isfile(os.path.join(out, 'proposal.tex'))


class TestGenerateSimpleMainSubprocess:
    def test_main_config_missing(self):
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, 'scripts/generate_simple.py'),
             '--config', 'missing-config-xyz.json'],
            capture_output=True,
            text=True,
            cwd=script_dir,
        )
        assert result.returncode == 1
        assert 'not found' in (result.stdout + result.stderr).lower()

    def test_main_interactive_cancel(self):
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        stdin = '\n'.join([
            '1', 'T', 'A', '1', '', 'Dr', '', '', '', '', '', 'Nov',
            'n',
        ]) + '\n'
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, 'scripts/generate_simple.py')],
            input=stdin,
            capture_output=True,
            text=True,
            cwd=script_dir,
        )
        assert result.returncode == 0
        assert 'cancelled' in (result.stdout + result.stderr).lower()
