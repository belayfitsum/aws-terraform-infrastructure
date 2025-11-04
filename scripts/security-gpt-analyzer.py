#!/usr/bin/env python3
"""
Security Auditor GPT Integration
Analyzes Trivy scan results and generates intelligent security reports
"""

import json
import requests
import os
from datetime import datetime

class SecurityAuditorGPT:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
    def analyze_trivy_results(self, trivy_json_file):
        """Analyze Trivy scan results using GPT"""
        with open(trivy_json_file, 'r') as f:
            scan_data = json.load(f)
        
        # Prepare vulnerability summary
        vuln_summary = self._extract_vulnerabilities(scan_data)
        
        # Send to GPT for analysis
        analysis = self._get_gpt_analysis(vuln_summary)
        
        # Generate report
        report = self._generate_report(analysis, vuln_summary)
        
        return report
    
    def _extract_vulnerabilities(self, scan_data):
        """Extract key vulnerability information"""
        vulnerabilities = []
        
        for result in scan_data.get('Results', []):
            for vuln in result.get('Vulnerabilities', []):
                vulnerabilities.append({
                    'id': vuln.get('VulnerabilityID'),
                    'severity': vuln.get('Severity'),
                    'package': vuln.get('PkgName'),
                    'version': vuln.get('InstalledVersion'),
                    'fixed_version': vuln.get('FixedVersion'),
                    'title': vuln.get('Title'),
                    'description': vuln.get('Description', '')[:200]
                })
        
        return vulnerabilities
    
    def _get_gpt_analysis(self, vulnerabilities):
        """Send vulnerabilities to GPT for analysis"""
        prompt = f"""
        Analyze these {len(vulnerabilities)} security vulnerabilities from a Trivy container scan:
        
        {json.dumps(vulnerabilities, indent=2)}
        
        Provide:
        1. Executive Summary
        2. Top 5 Critical Issues (prioritized by risk)
        3. Specific fix commands
        4. Prevention strategies
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an AWS DevOps Security Auditor."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.3
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    def _generate_report(self, gpt_analysis, vulnerabilities):
        """Generate comprehensive security report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# 🛡️ Security Audit Report
**Generated**: {timestamp}
**Total Vulnerabilities**: {len(vulnerabilities)}

## 🤖 AI Analysis
{gpt_analysis}

## 📊 Vulnerability Breakdown
"""
        
        # Count by severity
        severity_counts = {}
        for vuln in vulnerabilities:
            severity = vuln['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        for severity, count in severity_counts.items():
            report += f"- **{severity}**: {count}\n"
        
        return report

def main():
    """Main execution function"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    auditor = SecurityAuditorGPT(api_key)
    
    # Analyze latest Trivy results
    trivy_file = "trivy-results.json"
    if os.path.exists(trivy_file):
        report = auditor.analyze_trivy_results(trivy_file)
        
        # Save report
        with open("security-audit-report.md", "w") as f:
            f.write(report)
        
        print("✅ Security audit complete! Report saved to security-audit-report.md")
    else:
        print("❌ Trivy results file not found. Run Trivy scan first.")

if __name__ == "__main__":
    main()