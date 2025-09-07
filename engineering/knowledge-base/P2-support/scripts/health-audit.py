#!/usr/bin/env python3
"""
P2 Knowledge Base Health Audit System
Comprehensive health check for the P2 knowledge base
"""

from pathlib import Path
from datetime import datetime
import re

class P2HealthAudit:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent / "P2"
        self.issues = []
        self.warnings = []
        self.stats = {}
        
    def audit_structure(self):
        """Check directory structure is correct"""
        print("📁 Checking Directory Structure...")
        
        required_dirs = [
            "instructions/pasm2",
            "language/spin2/methods",
            "language/spin2/operators",
            "hardware",
            "architecture",
            "documentation",
            "examples"
        ]
        
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            if not full_path.exists():
                self.issues.append(f"Missing directory: {dir_path}")
            else:
                print(f"  ✅ {dir_path}")
    
    def audit_instruction_files(self):
        """Check PASM2 instruction files"""
        print("\n📋 Checking PASM2 Instructions...")
        
        pasm2_dir = self.base_dir / "instructions/pasm2"
        if not pasm2_dir.exists():
            self.issues.append("PASM2 directory missing!")
            return
            
        yaml_files = list(pasm2_dir.glob("*.yaml"))
        self.stats['pasm2_count'] = len(yaml_files)
        
        # Check for expected count
        if len(yaml_files) != 357:
            self.warnings.append(f"Expected 357 PASM2 files, found {len(yaml_files)}")
        
        # Check for invalid files (conditionals, pseudo)
        bad_patterns = ['if_', 'c_and', 'nc_or', 'empty', 'clr']
        bad_files = []
        
        for file in yaml_files:
            if any(pattern in file.stem for pattern in bad_patterns):
                bad_files.append(file.name)
        
        if bad_files:
            self.issues.append(f"Found {len(bad_files)} conditional/pseudo files")
            for bf in bad_files[:5]:
                self.issues.append(f"  - {bf}")
        
        # Check file structure
        sample_file = pasm2_dir / "add.yaml"
        if sample_file.exists():
            with open(sample_file, 'r') as f:
                content = f.read()
                required_fields = ['instruction:', 'syntax:', 'encoding:', 'description:', 'timing:']
                for field in required_fields:
                    if field not in content:
                        self.warnings.append(f"ADD.yaml missing field: {field}")
        
        print(f"  Found {len(yaml_files)} instruction files")
        
    def audit_language_files(self):
        """Check Spin2 language files"""
        print("\n🔤 Checking Spin2 Language...")
        
        methods_dir = self.base_dir / "language/spin2/methods"
        operators_dir = self.base_dir / "language/spin2/operators"
        
        if methods_dir.exists():
            methods = list(methods_dir.glob("*.yaml"))
            self.stats['spin2_methods'] = len(methods)
            print(f"  Methods: {len(methods)} files")
            if len(methods) != 73:
                self.warnings.append(f"Expected 73 methods, found {len(methods)}")
        else:
            self.issues.append("Spin2 methods directory missing!")
            
        if operators_dir.exists():
            operators = list(operators_dir.glob("*.yaml"))
            self.stats['spin2_operators'] = len(operators)
            print(f"  Operators: {len(operators)} files")
            if len(operators) != 46:
                self.warnings.append(f"Expected 46 operators, found {len(operators)}")
        else:
            self.issues.append("Spin2 operators directory missing!")
    
    def audit_completeness(self):
        """Check overall completeness"""
        print("\n✅ Checking Completeness...")
        
        # Check timing coverage
        pasm2_dir = self.base_dir / "instructions/pasm2"
        if pasm2_dir.exists():
            files_with_timing = 0
            for file in pasm2_dir.glob("*.yaml"):
                with open(file, 'r') as f:
                    if 'timing:' in f.read():
                        files_with_timing += 1
            
            timing_coverage = (files_with_timing / self.stats.get('pasm2_count', 1)) * 100
            self.stats['timing_coverage'] = timing_coverage
            print(f"  Timing coverage: {timing_coverage:.1f}%")
            
            if timing_coverage < 100:
                self.warnings.append(f"Timing coverage only {timing_coverage:.1f}%")
    
    def audit_no_maintenance_files(self):
        """Ensure no maintenance files in P2"""
        print("\n🚫 Checking for Maintenance Files...")
        
        # Should NOT find these in P2
        bad_patterns = [
            "*.py",  # Python scripts
            "*extractor*", 
            "*validator*",
            "*converter*",
            "_sources",
            "*.sh"  # Shell scripts
        ]
        
        maintenance_files = []
        for pattern in bad_patterns:
            found = list(self.base_dir.rglob(pattern))
            maintenance_files.extend(found)
        
        if maintenance_files:
            self.issues.append(f"Found {len(maintenance_files)} maintenance files in P2!")
            for mf in maintenance_files[:5]:
                self.issues.append(f"  - {mf.relative_to(self.base_dir)}")
        else:
            print("  ✅ No maintenance files found (correct)")
    
    def generate_report(self):
        """Generate health report"""
        print("\n" + "="*60)
        print("P2 KNOWLEDGE BASE HEALTH REPORT")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Base: {self.base_dir}")
        
        print("\n📊 Statistics:")
        print(f"  PASM2 Instructions: {self.stats.get('pasm2_count', 0)}")
        print(f"  Spin2 Methods: {self.stats.get('spin2_methods', 0)}")
        print(f"  Spin2 Operators: {self.stats.get('spin2_operators', 0)}")
        print(f"  Timing Coverage: {self.stats.get('timing_coverage', 0):.1f}%")
        
        if not self.issues and not self.warnings:
            print("\n✅ HEALTH CHECK PASSED")
            print("   Knowledge base is in excellent condition!")
        else:
            if self.issues:
                print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
                for issue in self.issues:
                    print(f"  • {issue}")
            
            if self.warnings:
                print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
                for warning in self.warnings:
                    print(f"  • {warning}")
        
        # Calculate health score
        score = 100
        score -= len(self.issues) * 10
        score -= len(self.warnings) * 3
        score = max(0, score)
        
        print(f"\n🏥 Health Score: {score}/100")
        
        if score >= 95:
            print("   Status: EXCELLENT")
        elif score >= 80:
            print("   Status: GOOD")
        elif score >= 60:
            print("   Status: NEEDS ATTENTION")
        else:
            print("   Status: CRITICAL")
        
        # Write report to file
        report_path = self.base_dir / "HEALTH-REPORT.md"
        with open(report_path, 'w') as f:
            f.write(f"# P2 Knowledge Base Health Report\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            f.write(f"## Health Score: {score}/100\n\n")
            f.write(f"## Statistics\n")
            f.write(f"- PASM2 Instructions: {self.stats.get('pasm2_count', 0)}\n")
            f.write(f"- Spin2 Methods: {self.stats.get('spin2_methods', 0)}\n")
            f.write(f"- Spin2 Operators: {self.stats.get('spin2_operators', 0)}\n")
            f.write(f"- Timing Coverage: {self.stats.get('timing_coverage', 0):.1f}%\n\n")
            
            if self.issues:
                f.write(f"## Issues\n")
                for issue in self.issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            if self.warnings:
                f.write(f"## Warnings\n")
                for warning in self.warnings:
                    f.write(f"- {warning}\n")
        
        print(f"\n📄 Report saved to: {report_path}")
    
    def run(self):
        """Run complete health audit"""
        print("🏥 P2 Knowledge Base Health Audit v1.0")
        print("="*60)
        
        self.audit_structure()
        self.audit_instruction_files()
        self.audit_language_files()
        self.audit_completeness()
        self.audit_no_maintenance_files()
        self.generate_report()

if __name__ == "__main__":
    audit = P2HealthAudit()
    audit.run()