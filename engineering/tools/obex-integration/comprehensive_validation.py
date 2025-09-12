#!/usr/bin/env python3
"""
Comprehensive OBEX integration validation before production trust
"""

import os
import yaml
import re
import requests
from pathlib import Path
from datetime import datetime
import random
import time

class OBEXValidator:
    def __init__(self, objects_dir, manifests_dir):
        self.objects_dir = Path(objects_dir)
        self.manifests_dir = Path(manifests_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.issues = []
        
    def log_issue(self, category, message):
        """Log validation issue"""
        self.issues.append(f"[{category}] {message}")
        print(f"⚠️  {category}: {message}")
    
    def validate_download_links(self, sample_size=3):
        """Test download links work"""
        print(f"\n🔗 DOWNLOAD LINK VALIDATION ({sample_size} samples)")
        print("-" * 50)
        
        # Get random sample of objects
        yaml_files = list(self.objects_dir.glob("*.yaml"))
        if "_template.yaml" in [f.name for f in yaml_files]:
            yaml_files = [f for f in yaml_files if f.name != "_template.yaml"]
        
        sample_files = random.sample(yaml_files, min(sample_size, len(yaml_files)))
        
        for yaml_file in sample_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                download_url = data['object_metadata']['urls'].get('download_direct', '')
                
                print(f"Testing {obj_id}: {title}")
                
                if not download_url:
                    self.log_issue("DOWNLOAD", f"Object {obj_id} missing download URL")
                    continue
                
                # Test download URL (HEAD request only)
                try:
                    response = self.session.head(download_url, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        print(f"  ✅ Download URL works (status {response.status_code})")
                    else:
                        self.log_issue("DOWNLOAD", f"Object {obj_id} download URL returns {response.status_code}")
                except requests.RequestException as e:
                    self.log_issue("DOWNLOAD", f"Object {obj_id} download failed: {e}")
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                self.log_issue("DOWNLOAD", f"Error testing {yaml_file}: {e}")
    
    def validate_random_sample_metadata(self, sample_size=3):
        """Compare random objects with live OBEX pages"""
        print(f"\n🎯 RANDOM SAMPLE VALIDATION ({sample_size} samples)")
        print("-" * 50)
        
        yaml_files = list(self.objects_dir.glob("*.yaml"))
        if "_template.yaml" in [f.name for f in yaml_files]:
            yaml_files = [f for f in yaml_files if f.name != "_template.yaml"]
        
        sample_files = random.sample(yaml_files, min(sample_size, len(yaml_files)))
        
        for yaml_file in sample_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                
                print(f"Validating {obj_id}: {title}")
                
                if not obex_url:
                    self.log_issue("METADATA", f"Object {obj_id} missing OBEX page URL")
                    continue
                
                # Fetch live page
                try:
                    response = self.session.get(obex_url, timeout=15)
                    if response.status_code == 200:
                        page_text = response.text
                        # Check if title appears on page
                        if title.lower() in page_text.lower():
                            print(f"  ✅ Title matches live page")
                        else:
                            self.log_issue("METADATA", f"Object {obj_id} title mismatch with live page")
                    else:
                        self.log_issue("METADATA", f"Object {obj_id} OBEX page returns {response.status_code}")
                except requests.RequestException as e:
                    self.log_issue("METADATA", f"Object {obj_id} page fetch failed: {e}")
                
                time.sleep(1.0)  # Rate limiting
                
            except Exception as e:
                self.log_issue("METADATA", f"Error validating {yaml_file}: {e}")
    
    def validate_manifest_connectivity(self, sample_size=3):
        """Check manifest references work"""
        print(f"\n🔗 MANIFEST CONNECTIVITY ({sample_size} samples)")
        print("-" * 50)
        
        # Test author manifests
        author_manifests = list((self.manifests_dir / "authors").glob("*.yaml"))
        sample_manifests = random.sample(author_manifests, min(sample_size, len(author_manifests)))
        
        for manifest_file in sample_manifests:
            try:
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                author = data['manifest_metadata']['author']
                print(f"Checking {author} manifest")
                
                if 'objects' in data:
                    for obj in data['objects']:
                        obj_id = obj.get('object_id', '')
                        yaml_path = obj.get('yaml_path', '')
                        
                        if yaml_path:
                            # Convert relative path to absolute
                            full_path = (self.manifests_dir / "authors" / yaml_path).resolve()
                            if full_path.exists():
                                print(f"  ✅ Object {obj_id} file exists")
                            else:
                                self.log_issue("CONNECTIVITY", f"Object {obj_id} file missing: {full_path}")
                        else:
                            self.log_issue("CONNECTIVITY", f"Object {obj_id} missing yaml_path")
                
            except Exception as e:
                self.log_issue("CONNECTIVITY", f"Error checking {manifest_file}: {e}")
    
    def scan_html_artifacts(self):
        """Final scan for HTML corruption"""
        print(f"\n🔍 HTML ARTIFACT SCAN")
        print("-" * 50)
        
        html_patterns = [
            r'<[A-Za-z]+\\s+ID\\s*:',
            r'Author\\s*:\\s*[^<]+Content\\s*:',
            r'Downloads\\\\_\\\\_',
            r'Select\\s+all\\\\nDeselect',
            r'To\\s+view\\s+this\\s+content,\\s+you\\s+need',
            r'Name\\s+Size\\s+Modified\\s+Date'
        ]
        
        artifacts_found = 0
        
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                obj_id = data['object_metadata']['object_id']
                desc_short = data['object_metadata']['functionality'].get('description_short', '')
                desc_full = data['object_metadata']['functionality'].get('description_full', '')
                
                combined_desc = desc_short + ' ' + desc_full
                
                for pattern in html_patterns:
                    if re.search(pattern, combined_desc, re.IGNORECASE):
                        self.log_issue("HTML_ARTIFACTS", f"Object {obj_id} contains HTML artifacts")
                        artifacts_found += 1
                        break
                        
            except Exception as e:
                self.log_issue("HTML_ARTIFACTS", f"Error scanning {yaml_file}: {e}")
        
        if artifacts_found == 0:
            print("✅ No HTML artifacts found!")
        else:
            print(f"⚠️  Found {artifacts_found} objects with potential HTML artifacts")
    
    def spot_check_github_references(self, sample_size=2):
        """Verify GitHub references in archiver imports"""
        print(f"\n🐙 GITHUB REFERENCE SPOT CHECK ({sample_size} samples)")
        print("-" * 50)
        
        github_objects = []
        
        # Find objects with GitHub archiver metadata
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                import_source = data['object_metadata']['metadata'].get('import_source', '')
                if import_source == 'github_archiver':
                    github_objects.append(yaml_file)
                    
            except Exception as e:
                continue
        
        if not github_objects:
            print("No GitHub archiver objects found")
            return
        
        sample_objects = random.sample(github_objects, min(sample_size, len(github_objects)))
        
        for yaml_file in sample_objects:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                obj_id = data['object_metadata']['object_id']
                original_platform = data['object_metadata']['metadata'].get('original_platform', '')
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                
                print(f"Checking GitHub reference for {obj_id}")
                
                if original_platform == 'github':
                    print(f"  ✅ Marked as GitHub import")
                else:
                    self.log_issue("GITHUB", f"Object {obj_id} missing GitHub platform marker")
                
                # We can't easily verify the actual GitHub repo exists without the URL
                # But we can verify the OBEX page mentions GitHub
                if obex_url:
                    try:
                        response = self.session.get(obex_url, timeout=10)
                        if 'github' in response.text.lower() or 'archiver' in response.text.lower():
                            print(f"  ✅ OBEX page mentions GitHub/archiver")
                        else:
                            print(f"  ⚠️  OBEX page doesn't mention GitHub import")
                    except:
                        print(f"  ⚠️  Couldn't verify OBEX page")
                
                time.sleep(1.0)
                
            except Exception as e:
                self.log_issue("GITHUB", f"Error checking {yaml_file}: {e}")
    
    def validate_date_consistency(self):
        """Check date formats and reasonable ranges"""
        print(f"\n📅 DATE CONSISTENCY CHECK")
        print("-" * 50)
        
        date_issues = 0
        date_formats = {}
        earliest_date = None
        latest_date = None
        
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                obj_id = data['object_metadata']['object_id']
                created_date = data['object_metadata']['metadata'].get('created_date', '')
                
                if not created_date:
                    self.log_issue("DATES", f"Object {obj_id} missing created_date")
                    date_issues += 1
                    continue
                
                # Parse date to check format and reasonableness
                try:
                    # Handle both formats: "YYYY-MM-DD HH:MM:SS" and "YYYY-MM-DD"
                    if ' ' in created_date:
                        date_part = created_date.split(' ')[0]
                        format_type = 'datetime'
                    else:
                        date_part = created_date
                        format_type = 'date'
                    
                    parsed_date = datetime.strptime(date_part, '%Y-%m-%d')
                    
                    # Track format usage
                    date_formats[format_type] = date_formats.get(format_type, 0) + 1
                    
                    # Check reasonableness (P2 released ~2019)
                    if parsed_date.year < 2019:
                        self.log_issue("DATES", f"Object {obj_id} date too early: {created_date}")
                        date_issues += 1
                    elif parsed_date.year > 2026:  # Future limit
                        self.log_issue("DATES", f"Object {obj_id} date too future: {created_date}")
                        date_issues += 1
                    
                    # Track date range
                    if earliest_date is None or parsed_date < earliest_date:
                        earliest_date = parsed_date
                    if latest_date is None or parsed_date > latest_date:
                        latest_date = parsed_date
                        
                except ValueError:
                    self.log_issue("DATES", f"Object {obj_id} invalid date format: {created_date}")
                    date_issues += 1
                
            except Exception as e:
                self.log_issue("DATES", f"Error checking {yaml_file}: {e}")
        
        print(f"Date format distribution: {date_formats}")
        if earliest_date and latest_date:
            print(f"Date range: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
        
        if date_issues == 0:
            print("✅ All dates consistent and reasonable!")
        else:
            print(f"⚠️  Found {date_issues} date issues")
    
    def generate_quality_metrics_report(self):
        """Generate final quality metrics report"""
        print(f"\n📊 QUALITY METRICS REPORT")
        print("=" * 50)
        
        total_objects = len([f for f in self.objects_dir.glob("*.yaml") if f.name != "_template.yaml"])
        total_issues = len(self.issues)
        
        print(f"Total objects analyzed: {total_objects}")
        print(f"Total validation issues: {total_issues}")
        
        if total_issues == 0:
            print("🎉 EXCELLENT: No validation issues found!")
            print("✅ Data ready for production use")
        else:
            print(f"⚠️  Quality Score: {((total_objects - total_issues) / total_objects * 100):.1f}%")
            
            # Categorize issues
            issue_categories = {}
            for issue in self.issues:
                category = issue.split(']')[0][1:]
                issue_categories[category] = issue_categories.get(category, 0) + 1
            
            print("\nIssue breakdown:")
            for category, count in sorted(issue_categories.items()):
                print(f"  {category}: {count} issues")
        
        print(f"\nRecommendation:")
        if total_issues == 0:
            print("✅ READY FOR PRODUCTION - No issues found")
        elif total_issues < 5:
            print("⚠️  MINOR ISSUES - Review and fix, then ready for production")
        elif total_issues < 15:
            print("🔶 MODERATE ISSUES - Address issues before production use")
        else:
            print("❌ MAJOR ISSUES - Significant cleanup needed before production")
        
        return total_issues

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    manifests_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/manifests"
    
    validator = OBEXValidator(objects_dir, manifests_dir)
    
    print("COMPREHENSIVE OBEX VALIDATION")
    print("=" * 50)
    print("Validating OBEX integration data before production deployment...")
    
    # Run all validations
    validator.validate_download_links(sample_size=3)
    validator.validate_random_sample_metadata(sample_size=3)
    validator.validate_manifest_connectivity(sample_size=3)
    validator.scan_html_artifacts()
    validator.spot_check_github_references(sample_size=2)
    validator.validate_date_consistency()
    
    # Final report
    issues_found = validator.generate_quality_metrics_report()
    
    return 0 if issues_found == 0 else 1

if __name__ == "__main__":
    exit(main())