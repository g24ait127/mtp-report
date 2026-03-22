# Input Schema Reference

Complete reference for all configuration options in the IITJ MTP Template Generator.

## Configuration File Format

The generator uses YAML format for configuration files. Here's the complete schema:

## Required Fields

### Project Information

```yaml
project:
  title: "Your Project Title"
  type: "proposal"  # or "major-project"
```

- **title** (string, required): Full title of your project
- **type** (string, required): Type of report
  - `"proposal"` - Research proposal or MTP1 report
  - `"major-project"` - Full thesis or major project report
  - `"presentation"` - Beamer slides

### Author Information

```yaml
author:
  name: "Full Name"
  roll_number: "Student ID"
  email: "email@example.com"  # Optional
```

- **name** (string, required): Your full name as it should appear on the report
- **roll_number** (string, required): Your student ID or roll number
- **email** (string, optional): Your email address (validated if provided)

### Academic Information

```yaml
academic:
  supervisor: "Dr. Supervisor Name"
  co_supervisor: "Dr. Co-Supervisor Name"  # Optional
  supervisor_designation: "Professor"  # Required for major-project
  supervisor_department: "Department Name"  # Required for major-project
  department: "Department of Computer Science"
  university: "University Name"
  degree: "Bachelor of Technology"
  session: "2024-25"
```

- **supervisor** (string, required): Name of your supervisor with title (e.g., "Dr. Jane Smith")
- **co_supervisor** (string, optional): Name of co-supervisor if applicable
- **supervisor_designation** (string, required for major-project): Supervisor's designation (e.g., "Professor", "Associate Professor")
- **supervisor_department** (string, required for major-project): Supervisor's department (defaults to student's department if not specified)
- **department** (string, required): Your department name
- **university** (string, required): Full university name
- **degree** (string, required): Degree name (e.g., "Bachelor of Technology", "Master of Science")
- **session** (string, required): Academic year or session (e.g., "2024-25")

### Dates

```yaml
dates:
  submission_date: "November 2024"
```

- **submission_date** (string, required): Submission date in "Month Year" format

## Optional Fields

### Formatting Options

```yaml
formatting:
  color_scheme: "blue"           # blue, red, green, custom
  font_size: 12                  # 10, 11, 12
  line_spacing: 1.5              # 1.0, 1.5, 2.0
  bibliography_style: "IEEE"     # IEEE, APA, ACM
```

- **color_scheme** (string, default: "blue"): Color scheme for the document
  - `"blue"` - Blue theme (default)
  - `"red"` - Red theme
  - `"green"` - Green theme
  - `"custom"` - Custom colors (requires template modification)

- **font_size** (integer, default: 12): Base font size in points
  - `10` - Small
  - `11` - Medium
  - `12` - Large (recommended)

- **line_spacing** (float, default: 1.5): Line spacing multiplier
  - `1.0` - Single spacing
  - `1.5` - 1.5 spacing (recommended for academic reports)
  - `2.0` - Double spacing

- **bibliography_style** (string, default: "IEEE"): Citation style
  - `"IEEE"` - IEEE style (default)
  - `"APA"` - APA style (requires APA .bst file)
  - `"ACM"` - ACM style (requires ACM .bst file)

### Content Options

```yaml
content:
  include_declaration: true
  include_certificate: true
  include_acknowledgments: true
  include_abstract: true
```

All content options are boolean (true/false) and default to `true`.

- **include_declaration** (boolean, default: true): Include declaration page (major-project only)
- **include_certificate** (boolean, default: true): Include certificate page (major-project only)
- **include_acknowledgments** (boolean, default: true): Include acknowledgments page
- **include_abstract** (boolean, default: true): Include abstract page

### Assets

```yaml
assets:
  logo_path: "./assets/university-logo.png"
```

- **logo_path** (string, optional): Path to custom university logo
  - Supported formats: PNG, JPG, PDF
  - Recommended size: 300x300 pixels minimum
  - If not specified, a default placeholder will be used

## Complete Example

### Proposal Report

```yaml
project:
  title: "Machine Learning for Climate Change Prediction"
  type: "proposal"

author:
  name: "Alice Johnson"
  roll_number: "2021CS042"
  email: "alice.johnson@university.edu"

academic:
  supervisor: "Dr. Robert Brown"
  co_supervisor: "Dr. Emily White"
  department: "Department of Computer Science and Engineering"
  university: "Institute of Technology"
  degree: "Bachelor of Technology"
  session: "2024-25"

dates:
  submission_date: "December 2024"

formatting:
  color_scheme: "blue"
  font_size: 12
  line_spacing: 1.5
  bibliography_style: "IEEE"

content:
  include_acknowledgments: true
  include_abstract: true

assets:
  logo_path: "./my-university-logo.png"
```

### Major Project Report

```yaml
project:
  title: "Machine Learning for Climate Change Prediction"
  type: "major-project"

author:
  name: "Alice Johnson"
  roll_number: "2021CS042"
  email: "alice.johnson@university.edu"

academic:
  supervisor: "Dr. Robert Brown"
  co_supervisor: ""
  supervisor_designation: "Professor"
  supervisor_department: "Department of Computer Science and Engineering"
  department: "Department of Computer Science and Engineering"
  university: "Institute of Technology"
  degree: "Bachelor of Technology"
  session: "2024-25"

dates:
  submission_date: "May 2025"

formatting:
  font_size: 12
  line_spacing: 1.5
  bibliography_style: "IEEE"

content:
  include_declaration: true
  include_certificate: true
  include_acknowledgments: true
  include_abstract: true
```

## Validation Rules

The generator validates your configuration:

1. **Required fields**: All required fields must be present and non-empty
2. **Email format**: If provided, email must be valid (e.g., `user@domain.com`)
3. **Project type**: Must be one of: `proposal`, `major-project`, `presentation`
4. **Logo path**: If specified, file must exist
5. **Font size**: Must be 10, 11, or 12
6. **Line spacing**: Must be 1.0, 1.5, or 2.0

## Tips

1. **Use quotes**: Always quote string values in YAML to avoid parsing issues
2. **Leave empty for optional**: Use `""` or omit the field entirely for optional fields
3. **Comments**: Use `#` for comments in your config file
4. **Validation**: Run the generator to validate your config before editing templates
5. **Reusability**: Save your config file for future use or sharing with peers

## See Also

- [Quick Start Guide](quickstart)
- [Customization Guide](customization)
- [FAQ](faq)
