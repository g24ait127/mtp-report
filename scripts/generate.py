#!/usr/bin/env python3
"""
IITJ MTP Template Generator - Main Script

Generate professional LaTeX academic reports from user inputs.
Supports proposal reports and major project reports.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
    from jinja2 import Environment, FileSystemLoader
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("⚠️  Warning: Required dependencies not found.")
    print("Please install dependencies: pip install -r requirements.txt")
    print("Or use the zero-dependency version: python scripts/generate_simple.py")
    sys.exit(1)

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from validators import validate_config, validate_email
from template_engine import prepare_context


# Default values
DEFAULTS = {
    'university': 'Your University Name',
    'department': 'Department of Computer Science and Engineering',
    'degree': 'Bachelor of Technology',
    'session': '2024-25',
    'supervisor_designation': 'Professor',
}


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("🎓  IITJ MTP Template Generator")
    print("=" * 60)
    print()


def get_user_input(prompt: str, default: Optional[str] = None, required: bool = True) -> str:
    """Get user input with optional default value.
    
    Args:
        prompt: Prompt message
        default: Default value if user presses Enter
        required: Whether field is required
        
    Returns:
        User input or default value
    """
    if default:
        prompt_text = f"{prompt} [default: {default}]: "
    else:
        prompt_text = f"{prompt}: "
    
    while True:
        value = input(prompt_text).strip()
        
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("❌ This field is required. Please provide a value.")


def collect_interactive_inputs() -> Dict[str, Any]:
    """Collect inputs interactively from user.
    
    Returns:
        Configuration dictionary
    """
    print_banner()
    
    # Project type
    print("Report type:")
    print("  [1] Proposal (MTP1/Research Proposal)")
    print("  [2] Major Project Report (Full Thesis)")
    print("  [3] Presentation Slides (Beamer)")
    
    while True:
        choice = input("Choice [1-3]: ").strip()
        if choice == '1':
            project_type = 'proposal'
            break
        elif choice == '2':
            project_type = 'major-project'
            break
        elif choice == '3':
            project_type = 'presentation'
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    print()
    
    # Project details
    title = get_user_input("Project title")
    
    print("\n--- Author Information ---")
    author_name = get_user_input("Your name")
    roll_number = get_user_input("Roll number")
    
    # Email (optional)
    while True:
        email = get_user_input("Email", required=False)
        if not email or validate_email(email):
            break
        print("❌ Invalid email format. Please try again.")
    
    print("\n--- Academic Information ---")
    supervisor = get_user_input("Supervisor name (e.g., Dr. Jane Smith)")
    co_supervisor = get_user_input("Co-supervisor (optional, press Enter to skip)", required=False)
    
    department = get_user_input("Department", default=DEFAULTS['department'])
    university = get_user_input("University", default=DEFAULTS['university'])
    degree = get_user_input("Degree", default=DEFAULTS['degree'])
    session = get_user_input("Academic session", default=DEFAULTS['session'])
    
    # Supervisor details (for major project)
    if project_type == 'major-project':
        print("\n--- Supervisor Details (for certificate) ---")
        supervisor_designation = get_user_input("Supervisor designation", default=DEFAULTS['supervisor_designation'])
        supervisor_department = get_user_input("Supervisor department", default=department)
    else:
        supervisor_designation = DEFAULTS['supervisor_designation']
        supervisor_department = department
    
    print("\n--- Dates ---")
    submission_date = get_user_input("Submission date (e.g., November 2024)")
    
    # Build configuration
    config = {
        'project': {
            'title': title,
            'type': project_type,
        },
        'author': {
            'name': author_name,
            'roll_number': roll_number,
            'email': email,
        },
        'academic': {
            'supervisor': supervisor,
            'co_supervisor': co_supervisor,
            'supervisor_designation': supervisor_designation,
            'supervisor_department': supervisor_department,
            'department': department,
            'university': university,
            'degree': degree,
            'session': session,
        },
        'dates': {
            'submission_date': submission_date,
        },
    }
    
    return config


def load_config_file(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def copy_template_files(template_type: str, output_dir: str, script_dir: str):
    """Copy template files to output directory.
    
    Args:
        template_type: Type of template ('proposal' or 'major-project')
        output_dir: Output directory path
        script_dir: Script directory path
    """
    # Template directory
    template_dir = os.path.join(script_dir, '..', 'templates', template_type)
    
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    
    # Copy all files except .tex files (those will be rendered)
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, template_dir)
            dst_path = os.path.join(output_dir, rel_path)
            
            # Skip .tex files (will be rendered separately)
            if file.endswith('.tex'):
                continue
            
            # Create directory if needed
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            # Copy file
            shutil.copy2(src_path, dst_path)


def render_templates(template_type: str, context: Dict[str, Any], output_dir: str, script_dir: str):
    """Render all template files.
    
    Args:
        template_type: Type of template ('proposal' or 'major-project')
        context: Template context variables
        output_dir: Output directory path
        script_dir: Script directory path
    """
    template_dir = os.path.join(script_dir, '..', 'templates', template_type)
    
    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_dir),
        block_start_string='\\BLOCK{',
        block_end_string='}',
        variable_start_string='\\VAR{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        trim_blocks=True,
        lstrip_blocks=True,
    )
    
    # Find all .tex files
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.tex'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, template_dir)
                dst_path = os.path.join(output_dir, rel_path)
                
                # Load and render template
                template_rel_path = os.path.relpath(src_path, template_dir).replace('\\', '/')
                template = env.get_template(template_rel_path)
                rendered = template.render(**context)
                
                # Write rendered output
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                with open(dst_path, 'w', encoding='utf-8') as f:
                    f.write(rendered)


def generate_report(config: Dict[str, Any], output_dir: Optional[str] = None) -> str:
    """Generate report from configuration.
    
    Args:
        config: Configuration dictionary
        output_dir: Optional output directory path
        
    Returns:
        Path to generated report directory
    """
    # Validate configuration
    is_valid, errors = validate_config(config)
    if not is_valid:
        print("\n❌ Configuration validation failed:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)
    
    # Determine output directory
    if not output_dir:
        # Create output directory from project title
        title_slug = config['project']['title'].lower().replace(' ', '-')
        title_slug = ''.join(c for c in title_slug if c.isalnum() or c == '-')
        output_dir = os.path.join('output', title_slug)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Handle content extraction for presentations
    if config['project']['type'] == 'presentation':
        extract_config = config.get('presentation', {})
        if extract_config.get('extract_from_report', False):
            report_path = extract_config.get('report_path', '')
            
            # Resolve relative paths
            if report_path and not os.path.isabs(report_path):
                report_path = os.path.abspath(report_path)
            
            if report_path and os.path.exists(report_path):
                try:
                    print(f"\n📄 Extracting content from: {report_path}")
                    from utils.content_extractor import extract_content_from_report
                    extracted = extract_content_from_report(report_path)
                    
                    if extracted:
                        config['extracted_content'] = extracted
                        print("✅ Content extracted successfully")
                    else:
                        print("⚠️  Content extraction returned no data")
                        print("   Generating presentation with TODO placeholders")
                except Exception as e:
                    print(f"⚠️  Content extraction failed: {e}")
                    print("   Generating presentation with TODO placeholders")
            elif report_path:
                print(f"\n⚠️  Report file not found: {report_path}")
                print("   Generating presentation with TODO placeholders")
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get template type
    template_type = config['project']['type']
    
    print(f"\n📝 Generating {template_type} report...")
    
    # Prepare context
    context = prepare_context(config)
    
    # Copy non-template files
    print("   Copying template files...")
    copy_template_files(template_type, output_dir, script_dir)
    
    # Render templates
    print("   Rendering LaTeX templates...")
    render_templates(template_type, context, output_dir, script_dir)
    
    print(f"\n✅ Report generated successfully!")
    print(f"📁 Output directory: {os.path.abspath(output_dir)}")
    
    return output_dir


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate professional LaTeX academic reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python scripts/generate.py
  
  # Using config file
  python scripts/generate.py --config examples/sample-proposal/config.yaml
  
  # Specify output directory
  python scripts/generate.py --config config.yaml --output my-report
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to YAML configuration file',
        type=str,
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output directory path',
        type=str,
    )
    
    args = parser.parse_args()
    
    # Get configuration
    if args.config:
        # Load from config file
        if not os.path.exists(args.config):
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
        
        config = load_config_file(args.config)
        print(f"✅ Loaded configuration from: {args.config}")
    else:
        # Interactive mode
        config = collect_interactive_inputs()
        
        # Confirm generation
        print("\n" + "=" * 60)
        print("📋 Summary:")
        print(f"   Project: {config['project']['title']}")
        print(f"   Type: {config['project']['type']}")
        print(f"   Author: {config['author']['name']} ({config['author']['roll_number']})")
        print(f"   Supervisor: {config['academic']['supervisor']}")
        print("=" * 60)
        
        confirm = input("\nGenerate report with these details? [Y/n]: ").strip().lower()
        if confirm and confirm != 'y':
            print("❌ Generation cancelled.")
            sys.exit(0)
    
    # Generate report
    output_dir = generate_report(config, args.output)
    
    # Print next steps
    print("\n⚠️  Important:")
    print("   This is a starter LaTeX project with placeholders ([TODO] / % TODO in .tex files).")
    print("   A PDF compiled before you replace that text shows layout only—not your final report.")
    print("\n📚 Next steps:")
    print(f"   1. Edit the .tex files in {output_dir} to add your content")
    
    if config['project']['type'] == 'proposal':
        print(f"   2. Compile with: cd {output_dir} && pdflatex proposal.tex && bibtex proposal && pdflatex proposal.tex && pdflatex proposal.tex")
    elif config['project']['type'] == 'presentation':
        print(f"   2. Compile with: cd {output_dir} && pdflatex slides.tex && pdflatex slides.tex")
    else:
        print(f"   2. Compile with: cd {output_dir} && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex")
    
    print("\n")


if __name__ == '__main__':
    main()
