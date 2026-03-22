#!/usr/bin/env python3
"""
IITJ MTP Template Generator - Simple Version (Zero Dependencies)

This is a simplified version that uses only Python standard library.
No external dependencies required (no Jinja2, no PyYAML).
Uses JSON for configuration and simple string replacement for templating.
"""

import os
import sys
import shutil
import json


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("IITJ MTP Template Generator (Simple Mode)")
    print("=" * 60)
    print("Note: This is the zero-dependency version with basic features.")
    print("For full features, install dependencies and use generate.py")
    print("=" * 60)
    print()


def get_user_input(prompt, default=None, required=True):
    """Get user input with optional default value."""
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
            print("[ERROR] This field is required. Please provide a value.")


def collect_inputs():
    """Collect inputs interactively from user."""
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
            print("[ERROR] Invalid choice. Please enter 1, 2, or 3.")
    
    print()
    
    # Collect basic information
    config = {
        'project': {
            'title': get_user_input("Project title"),
            'type': project_type,
        },
        'author': {
            'name': get_user_input("Your name"),
            'roll_number': get_user_input("Roll number"),
            'email': get_user_input("Email (optional)", required=False),
        },
        'academic': {
            'supervisor': get_user_input("Supervisor name (e.g., Dr. Jane Smith)"),
            'co_supervisor': get_user_input("Co-supervisor (optional)", required=False),
            'department': get_user_input("Department", default="Department of Computer Science"),
            'university': get_user_input("University", default="Your University Name"),
            'degree': get_user_input("Degree", default="Bachelor of Technology"),
            'session': get_user_input("Academic session", default="2024-25"),
        },
        'dates': {
            'submission_date': get_user_input("Submission date (e.g., November 2024)"),
        },
    }
    
    if project_type == 'major-project':
        config['academic']['supervisor_designation'] = get_user_input(
            "Supervisor designation", default="Professor"
        )
        config['academic']['supervisor_department'] = get_user_input(
            "Supervisor department", default=config['academic']['department']
        )
    
    return config


def simple_replace(text, replacements):
    """Simple string replacement."""
    result = text
    for key, value in replacements.items():
        # Handle both Jinja2-style and simple placeholders
        result = result.replace(f'\\VAR{{{key}}}', str(value))
        result = result.replace(f'{{{{{key}}}}}', str(value))
    return result


def copy_and_process_files(template_type, config, output_dir, script_dir):
    """Copy and process template files."""
    template_dir = os.path.join(script_dir, '..', 'templates', template_type)
    
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    
    # Create replacements dictionary
    replacements = {
        'TITLE': config['project']['title'],
        'AUTHOR_NAME': config['author']['name'],
        'ROLL_NUMBER': config['author']['roll_number'],
        'EMAIL': config['author'].get('email', ''),
        'SUPERVISOR': config['academic']['supervisor'],
        'CO_SUPERVISOR': config['academic'].get('co_supervisor', ''),
        'SUPERVISOR_DESIGNATION': config['academic'].get('supervisor_designation', 'Professor'),
        'SUPERVISOR_DEPARTMENT': config['academic'].get('supervisor_department', config['academic']['department']),
        'DEPARTMENT': config['academic']['department'],
        'UNIVERSITY': config['academic']['university'],
        'DEGREE': config['academic']['degree'],
        'SESSION': config['academic']['session'],
        'SUBMISSION_DATE': config['dates']['submission_date'],
        'INCLUDE_DECLARATION': 'true',
        'INCLUDE_CERTIFICATE': 'true',
        'INCLUDE_ACKNOWLEDGMENTS': 'true',
        'INCLUDE_ABSTRACT': 'true',
        # Presentation-specific
        'THEME': config.get('presentation', {}).get('theme', 'Madrid'),
        'COLOR_SCHEME': config.get('presentation', {}).get('color_scheme', 'default'),
        'ASPECT_RATIO': config.get('presentation', {}).get('aspect_ratio', '16:9'),
        'ASPECT_RATIO_VALUE': '169' if config.get('presentation', {}).get('aspect_ratio', '16:9') == '16:9' else '43',
        'PRESENTATION_DATE': config.get('presentation', {}).get('presentation_date', config['dates']['submission_date']),
    }
    
    # Process all files
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, template_dir)
            dst_path = os.path.join(output_dir, rel_path)
            
            # Create directory if needed
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            # Process .tex files with replacements
            if file.endswith('.tex'):
                with open(src_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple replacement (won't handle Jinja2 blocks perfectly)
                processed = simple_replace(content, replacements)
                
                # Remove Jinja2 block statements (basic cleanup)
                processed = processed.replace('\\BLOCK{if INCLUDE_DECLARATION}', '')
                processed = processed.replace('\\BLOCK{if INCLUDE_CERTIFICATE}', '')
                processed = processed.replace('\\BLOCK{if INCLUDE_ACKNOWLEDGMENTS}', '')
                processed = processed.replace('\\BLOCK{if INCLUDE_ABSTRACT}', '')
                processed = processed.replace('\\BLOCK{endif}', '')
                
                with open(dst_path, 'w', encoding='utf-8') as f:
                    f.write(processed)
            else:
                # Copy non-.tex files as-is
                shutil.copy2(src_path, dst_path)


def generate_report(config, output_dir=None):
    """Generate report from configuration."""
    # Determine output directory
    if not output_dir:
        title_slug = config['project']['title'].lower().replace(' ', '-')
        title_slug = ''.join(c for c in title_slug if c.isalnum() or c == '-')
        output_dir = os.path.join('output', title_slug)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get template type
    template_type = config['project']['type']
    
    print(f"\n[INFO] Generating {template_type} report...")
    print("   Processing template files...")
    
    # Copy and process files
    copy_and_process_files(template_type, config, output_dir, script_dir)
    
    print(f"\n[OK] Report generated successfully!")
    print(f"[INFO] Output directory: {os.path.abspath(output_dir)}")
    
    return output_dir


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate academic reports (Simple version - no dependencies)',
        epilog='Note: This version has limited features. For full functionality, use generate.py'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to JSON configuration file',
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
        if not os.path.exists(args.config):
            print(f"[ERROR] Config file not found: {args.config}")
            sys.exit(1)
        
        with open(args.config, 'r') as f:
            config = json.load(f)
        print(f"[OK] Loaded configuration from: {args.config}")
    else:
        # Interactive mode
        config = collect_inputs()
        
        # Confirm generation
        print("\n" + "=" * 60)
        print("[Outcome] Summary:")
        print(f"   Project: {config['project']['title']}")
        print(f"   Type: {config['project']['type']}")
        print(f"   Author: {config['author']['name']} ({config['author']['roll_number']})")
        print(f"   Supervisor: {config['academic']['supervisor']}")
        print("=" * 60)
        
        confirm = input("\nGenerate report with these details? [Y/n]: ").strip().lower()
        if confirm and confirm != 'y':
            print("[ERROR] Generation cancelled.")
            sys.exit(0)
    
    # Generate report
    output_dir = generate_report(config, args.output)
    
    # Print next steps
    print("\n[INFO] Important:")
    print("   This is a starter LaTeX project with placeholders ([TODO] / % TODO in .tex files).")
    print("   A PDF compiled before you replace that text shows layout only—not your final report.")
    print("\n[INFO] Next steps:")
    print(f"   1. Edit the .tex files in {output_dir} to add your content")
    
    if config['project']['type'] == 'proposal':
        print(f"   2. Compile with: cd {output_dir} && pdflatex proposal.tex && bibtex proposal && pdflatex proposal.tex && pdflatex proposal.tex")
    elif config['project']['type'] == 'presentation':
        print(f"   2. Compile with: cd {output_dir} && pdflatex slides.tex && pdflatex slides.tex")
    else:
        print(f"   2. Compile with: cd {output_dir} && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex")
    
    print("\n[INFO] Note: For advanced features (YAML config, better templating), use generate.py")
    print("   Install dependencies: pip install -r scripts/requirements.txt")
    print("\n")


if __name__ == '__main__':
    main()
