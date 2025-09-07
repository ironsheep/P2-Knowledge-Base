#!/usr/bin/env python3
"""
Quality Audit Dashboard Generator for P2 Knowledge Base
Generates comprehensive quality reports from audit YAML files
Version: 1.0.0
"""

import yaml
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import statistics

class AuditDashboardGenerator:
    """Generates quality dashboards from audit data"""
    
    def __init__(self, audit_dir: str, output_dir: str):
        self.audit_dir = Path(audit_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audit_data = {}
        self.metrics = {}
        
    def load_audits(self) -> None:
        """Load all audit YAML files"""
        for audit_file in self.audit_dir.glob("*.yaml"):
            with open(audit_file, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    category = data.get('category_id', audit_file.stem)
                    self.audit_data[category] = data
                    
    def calculate_metrics(self) -> None:
        """Calculate aggregate metrics across all audits"""
        self.metrics = {
            'total_entries': 0,
            'average_score': 0,
            'production_ready': 0,
            'needs_work': 0,
            'score_distribution': {i: 0 for i in range(9)},
            'coverage_by_source': {},
            'categories': {}
        }
        
        scores = []
        for category, data in self.audit_data.items():
            # Aggregate totals
            total = data.get('total_entries', 0)
            self.metrics['total_entries'] += total
            
            # Production readiness
            ready = data.get('production_ready', 0)
            needs_work = data.get('needs_work', 0)
            self.metrics['production_ready'] += ready
            self.metrics['needs_work'] += needs_work
            
            # Score distribution
            if 'score_distribution' in data:
                for score_level, count in data['score_distribution'].items():
                    score_num = int(score_level.split('_')[1])
                    self.metrics['score_distribution'][score_num] += count
                    scores.extend([score_num] * count)
            
            # Category-specific metrics
            self.metrics['categories'][category] = {
                'total': total,
                'average_score': data.get('average_score', 0),
                'production_ready': ready,
                'coverage': data.get('extraction_coverage', {})
            }
        
        # Calculate overall average
        if scores:
            self.metrics['average_score'] = statistics.mean(scores)
            
    def generate_html_dashboard(self) -> str:
        """Generate HTML dashboard"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P2 Knowledge Base Quality Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .score-bar {{
            display: flex;
            height: 40px;
            border-radius: 4px;
            overflow: hidden;
            margin: 20px 0;
        }}
        .score-segment {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        .score-0 {{ background: #e74c3c; }}
        .score-1 {{ background: #e67e22; }}
        .score-2 {{ background: #f39c12; }}
        .score-3 {{ background: #f1c40f; }}
        .score-4 {{ background: #2ecc71; }}
        .score-5 {{ background: #27ae60; }}
        .score-6 {{ background: #16a085; }}
        .score-7 {{ background: #2980b9; }}
        .score-8 {{ background: #8e44ad; }}
        .category-table {{
            width: 100%;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        .progress-bar {{
            background: #ecf0f1;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
        }}
        .progress-fill {{
            background: #3498db;
            height: 100%;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-size: 0.8em;
        }}
        .timestamp {{
            color: #7f8c8d;
            margin-top: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>P2 Knowledge Base Quality Dashboard</h1>
        <p>Repository Health and Completeness Metrics</p>
    </div>
    
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{self.metrics['total_entries']}</div>
            <div class="metric-label">Total Entries</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{self.metrics['average_score']:.1f}/8</div>
            <div class="metric-label">Average Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{self.metrics['production_ready']}</div>
            <div class="metric-label">Production Ready (≥6)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{self.metrics['needs_work']}</div>
            <div class="metric-label">Needs Work (<6)</div>
        </div>
    </div>
    
    <h2>Score Distribution</h2>
    <div class="score-bar">
"""
        
        # Add score distribution bars
        total = sum(self.metrics['score_distribution'].values())
        if total > 0:
            for score, count in self.metrics['score_distribution'].items():
                if count > 0:
                    percentage = (count / total) * 100
                    html += f'''
        <div class="score-segment score-{score}" style="width: {percentage}%">
            {count}
        </div>
'''
        
        html += """
    </div>
    
    <h2>Category Breakdown</h2>
    <div class="category-table">
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Total Entries</th>
                    <th>Average Score</th>
                    <th>Production Ready</th>
                    <th>Progress</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add category rows
        for category, data in self.metrics['categories'].items():
            ready_pct = (data['production_ready'] / data['total'] * 100) if data['total'] > 0 else 0
            html += f"""
                <tr>
                    <td><strong>{category}</strong></td>
                    <td>{data['total']}</td>
                    <td>{data['average_score']:.1f}</td>
                    <td>{data['production_ready']}</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {ready_pct}%">
                                {ready_pct:.0f}%
                            </div>
                        </div>
                    </td>
                </tr>
"""
        
        html += f"""
            </tbody>
        </table>
    </div>
    
    <div class="timestamp">
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
"""
        return html
        
    def generate_markdown_report(self) -> str:
        """Generate Markdown report"""
        md = f"""# P2 Knowledge Base Quality Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Metrics

| Metric | Value |
|--------|-------|
| **Total Entries** | {self.metrics['total_entries']} |
| **Average Score** | {self.metrics['average_score']:.1f}/8 |
| **Production Ready** | {self.metrics['production_ready']} (≥6) |
| **Needs Work** | {self.metrics['needs_work']} (<6) |

## Score Distribution

| Score | Count | Percentage |
|-------|-------|------------|
"""
        
        total = sum(self.metrics['score_distribution'].values())
        for score in range(9):
            count = self.metrics['score_distribution'][score]
            pct = (count / total * 100) if total > 0 else 0
            bar = '█' * int(pct / 2)
            md += f"| {score} | {count} | {bar} {pct:.1f}% |\n"
            
        md += """
## Category Breakdown

| Category | Total | Avg Score | Production Ready | Progress |
|----------|-------|-----------|------------------|----------|
"""
        
        for category, data in self.metrics['categories'].items():
            ready_pct = (data['production_ready'] / data['total'] * 100) if data['total'] > 0 else 0
            md += f"| {category} | {data['total']} | {data['average_score']:.1f} | {data['production_ready']} | {ready_pct:.0f}% |\n"
            
        md += """
## Improvement Priorities

### Critical (Score 0-2)
Focus on basic extraction from CSV and datasheet

### High Priority (Score 3-5)  
Add descriptions, examples, and timing data

### Enhancement (Score 6-7)
Add cross-references and meta-knowledge

### Complete (Score 8)
Maintain and verify accuracy
"""
        
        return md
        
    def generate_json_metrics(self) -> str:
        """Generate JSON metrics for programmatic access"""
        output = {
            'generated': datetime.now().isoformat(),
            'metrics': self.metrics,
            'audit_data': self.audit_data
        }
        return json.dumps(output, indent=2, default=str)
        
    def save_dashboard(self) -> None:
        """Save all dashboard formats"""
        # HTML Dashboard
        html_path = self.output_dir / "dashboard.html"
        with open(html_path, 'w') as f:
            f.write(self.generate_html_dashboard())
            
        # Markdown Report
        md_path = self.output_dir / "quality-report.md"
        with open(md_path, 'w') as f:
            f.write(self.generate_markdown_report())
            
        # JSON Metrics
        json_path = self.output_dir / "metrics.json"
        with open(json_path, 'w') as f:
            f.write(self.generate_json_metrics())
            
        print(f"Dashboard generated:")
        print(f"  HTML: {html_path}")
        print(f"  Markdown: {md_path}")
        print(f"  JSON: {json_path}")
        
    def run(self) -> None:
        """Execute dashboard generation"""
        print("Loading audit data...")
        self.load_audits()
        
        print("Calculating metrics...")
        self.calculate_metrics()
        
        print("Generating dashboards...")
        self.save_dashboard()
        
        print(f"\nSummary:")
        print(f"  Total Entries: {self.metrics['total_entries']}")
        print(f"  Average Score: {self.metrics['average_score']:.1f}/8")
        print(f"  Production Ready: {self.metrics['production_ready']}")
        

if __name__ == "__main__":
    # Configure paths
    audit_dir = "quality-audits"
    output_dir = "quality-audits/dashboard"
    
    # Generate dashboard
    generator = AuditDashboardGenerator(audit_dir, output_dir)
    generator.run()