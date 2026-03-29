import argparse
import csv
import json
import os
import sys

# Paths relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, mode='r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {}
    with open(path, mode='r', encoding='utf-8') as f:
        return json.load(f)

def search_domain(query, domain):
    filename = {
        "style": "styles.csv",
        "color": "colors.csv",
        "typography": "typography.csv",
        "chart": "charts.csv",
        "pattern": "patterns.csv",
        "ux": "ux-guidelines.csv"
    }.get(domain)

    if not filename:
        print(f"Error: Unknown domain '{domain}'")
        return

    data = load_csv(filename)
    query = query.lower()
    results = [row for row in data if any(query in val.lower() for val in row.values())]
    
    if not results:
        print(f"No results found for '{query}' in {domain}")
        return

    print(json.dumps(results, indent=2))

def generate_design_system(product_query, project_name, persist=False, page=None):
    rules = load_json("reasoning-rules.json")
    # Simple keyword matching for demo/pro-max engine
    matched_rule = None
    for rule in rules:
        if any(keyword.lower() in product_query.lower() for keyword in rule.get("keywords", [])):
            matched_rule = rule
            break
    
    if not matched_rule:
        # Default to SaaS if no match
        matched_rule = rules[0] if rules else {}

    # In a real engine, we'd pull from CSVs here. For now, we simulate the output.
    print(f"╔══════════════════════════════════════════════════════════════╗")
    print(f"║  DESIGN SYSTEM — {project_name or 'Untitled Project'} {' - ' + page if page else ''}")
    print(f"╠══════════════════════════════════════════════════════════════╣")
    print(f"║  INDUSTRY:    {matched_rule.get('industry', 'Unknown')}               ║")
    print(f"║  PATTERN:     {matched_rule.get('pattern', 'Hero-Centric')}           ║")
    print(f"║  STYLE:       {matched_rule.get('style', 'Minimalist')}               ║")
    print(f"╠══════════════════════════════════════════════════════════════╣")
    print(f"║  COLORS                                                      ║")
    print(f"║    Primary:    {matched_rule.get('colors', {}).get('primary', '#000000')} ║")
    print(f"║    Secondary:  {matched_rule.get('colors', {}).get('secondary', '#FFFFFF')} ║")
    print(f"║    CTA:        {matched_rule.get('colors', {}).get('cta', '#FF0000')} ║")
    print(f"╠══════════════════════════════════════════════════════════════╣")
    print(f"║  TYPOGRAPHY                                                  ║")
    print(f"║    Heading: {matched_rule.get('typography', {}).get('heading', 'Inter')} ║")
    print(f"║    Body:    {matched_rule.get('typography', {}).get('body', 'Inter')} ║")
    print(f"╚══════════════════════════════════════════════════════════════╝")

    if persist:
        target_dir = os.path.join(os.getcwd(), "design-system")
        os.makedirs(target_dir, exist_ok=True)
        template_path = os.path.join(RESOURCES_DIR, "design-system-template.md")
        
        if page:
            filename = f"pages/{page}.md"
            os.makedirs(os.path.join(target_dir, "pages"), exist_ok=True)
        else:
            filename = "MASTER.md"
            
        dest_path = os.path.join(target_dir, filename)
        with open(dest_path, "w") as f:
            f.write(f"# Design System for {project_name}\n\nGenerated for {product_query}")
        print(f"Design system persisted to {dest_path}")

def main():
    parser = argparse.ArgumentParser(description="Design database search engine")
    parser.add_argument("query", help="Search query or product description")
    parser.add_argument("--design-system", action="store_true", help="Generate design system")
    parser.add_argument("-p", "--project", dest="project", help="Project name")
    parser.add_argument("--domain", choices=["style", "color", "typography", "chart", "pattern", "ux"], help="Specific domain to search")
    parser.add_argument("--persist", action="store_true", help="Persist the design system to files")
    parser.add_argument("--page", help="Specific page for persistence")

    args = parser.parse_args()

    if args.domain:
        search_domain(args.query, args.domain)
    elif args.design_system:
        generate_design_system(args.query, args.project, args.persist, args.page)
    else:
        # Default to general search across all CSVs if no flag
        for domain in ["style", "color", "typography", "chart", "pattern", "ux"]:
            search_domain(args.query, domain)

if __name__ == "__main__":
    main()
