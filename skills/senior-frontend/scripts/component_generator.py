import os
import sys
import argparse

def generate_component(component_path):
    component_name = os.path.basename(component_path)
    component_dir = os.path.dirname(component_path)
    target_dir = os.path.join(os.getcwd(), component_dir, component_name)

    os.makedirs(target_dir, exist_ok=True)

    component_code = f"""import React from 'react';
import PropTypes from 'prop-types';

/**
 * {component_name} Component
 */
export const {component_name} = ({{ title, children, className = '' }}) => {{
  return (
    <div className={{`${{className}}`}}>
      {{title && <h2>{{title}}</h2>}}
      {{children}}
    </div>
  );
}};

{component_name}.propTypes = {{
  title: PropTypes.string,
  children: PropTypes.node,
  className: PropTypes.string,
}};
"""

    test_code = f"""import {{ render, screen }} from '@testing-library/react';
import {{ {component_name} }} from './{component_name}';

describe('{component_name} Component', () => {{
  it('renders correctly', () => {{
    render(<{component_name} title="Test">Content</{component_name}>);
    expect(screen.getByText('Test')).toBeInTheDocument();
    expect(screen.getByText('Content')).toBeInTheDocument();
  }});
}});
"""

    story_code = f"""import {{ {component_name} }} from './{component_name}';

export default {{
  title: 'Components/{component_name}',
  component: {component_name},
  tags: ['autodocs'],
}};

export const Default = {{
  args: {{
    title: 'Default Title',
    children: 'Default Content',
  }},
}};
"""

    try:
        with open(os.path.join(target_dir, f"{component_name}.jsx"), "w") as f:
            f.write(component_code)
        with open(os.path.join(target_dir, f"{component_name}.test.jsx"), "w") as f:
            f.write(test_code)
        with open(os.path.join(target_dir, f"{component_name}.stories.jsx"), "w") as f:
            f.write(story_code)
        print(f"Successfully generated {component_name} (.jsx) in {target_dir}")
    except Exception as e:
        print(f"Error writing components: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a React JS component structure.')
    parser.add_argument('path', help='Path and name of the component (e.g. src/components/ui/Button)')
    args = parser.parse_args()
    
    generate_component(args.path)
