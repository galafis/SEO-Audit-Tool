#!/usr/bin/env python3
"""
SEO Audit Tool
Comprehensive SEO analysis and audit tool for websites.
"""

from flask import Flask, render_template_string, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime

app = Flask(__name__)

class SEOAuditor:
    """Comprehensive SEO audit functionality."""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def audit_website(self, url):
        """Perform comprehensive SEO audit."""
        try:
            # Fetch webpage
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            audit_results = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'page_size': len(response.content),
                'load_time': response.elapsed.total_seconds(),
                'title_analysis': self._analyze_title(soup),
                'meta_analysis': self._analyze_meta_tags(soup),
                'heading_analysis': self._analyze_headings(soup),
                'content_analysis': self._analyze_content(soup),
                'image_analysis': self._analyze_images(soup),
                'link_analysis': self._analyze_links(soup, url),
                'technical_analysis': self._analyze_technical(soup, response),
                'performance_score': 0,
                'seo_score': 0
            }
            
            # Calculate scores
            audit_results['seo_score'] = self._calculate_seo_score(audit_results)
            audit_results['performance_score'] = self._calculate_performance_score(audit_results)
            
            return audit_results
            
        except Exception as e:
            return {'error': str(e), 'url': url}
    
    def _analyze_title(self, soup):
        """Analyze page title."""
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ''
        
        return {
            'title': title,
            'length': len(title),
            'has_title': bool(title),
            'optimal_length': 30 <= len(title) <= 60,
            'issues': self._get_title_issues(title)
        }
    
    def _analyze_meta_tags(self, soup):
        """Analyze meta tags."""
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        
        description = meta_description.get('content', '') if meta_description else ''
        
        return {
            'description': description,
            'description_length': len(description),
            'has_description': bool(description),
            'optimal_description_length': 120 <= len(description) <= 160,
            'has_keywords': bool(meta_keywords),
            'has_robots': bool(meta_robots),
            'robots_content': meta_robots.get('content', '') if meta_robots else '',
            'issues': self._get_meta_issues(description)
        }
    
    def _analyze_headings(self, soup):
        """Analyze heading structure."""
        headings = {}
        heading_structure = []
        
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = {
                'count': len(h_tags),
                'texts': [h.get_text().strip() for h in h_tags]
            }
            
            for h in h_tags:
                heading_structure.append({
                    'level': i,
                    'text': h.get_text().strip(),
                    'length': len(h.get_text().strip())
                })
        
        return {
            'headings': headings,
            'structure': heading_structure,
            'has_h1': headings['h1']['count'] > 0,
            'h1_count': headings['h1']['count'],
            'proper_hierarchy': self._check_heading_hierarchy(heading_structure),
            'issues': self._get_heading_issues(headings)
        }
    
    def _analyze_content(self, soup):
        """Analyze page content."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = text.split()
        
        return {
            'word_count': len(words),
            'character_count': len(text),
            'paragraph_count': len(soup.find_all('p')),
            'has_sufficient_content': len(words) >= 300,
            'readability_score': self._calculate_readability(text),
            'issues': self._get_content_issues(words)
        }
    
    def _analyze_images(self, soup):
        """Analyze images for SEO."""
        images = soup.find_all('img')
        
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        images_without_alt = total_images - images_with_alt
        
        return {
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'images_without_alt': images_without_alt,
            'alt_text_coverage': (images_with_alt / total_images * 100) if total_images > 0 else 100,
            'issues': self._get_image_issues(images_without_alt)
        }
    
    def _analyze_links(self, soup, base_url):
        """Analyze internal and external links."""
        links = soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)
        
        return {
            'total_links': len(links),
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'internal_ratio': (len(internal_links) / len(links) * 100) if links else 0,
            'issues': self._get_link_issues(links)
        }
    
    def _analyze_technical(self, soup, response):
        """Analyze technical SEO factors."""
        # Check for canonical tag
        canonical = soup.find('link', rel='canonical')
        
        # Check for viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        # Check for SSL
        is_https = response.url.startswith('https://')
        
        return {
            'has_canonical': bool(canonical),
            'canonical_url': canonical.get('href') if canonical else '',
            'has_viewport': bool(viewport),
            'is_https': is_https,
            'response_time': response.elapsed.total_seconds(),
            'content_type': response.headers.get('content-type', ''),
            'issues': self._get_technical_issues(canonical, viewport, is_https, response)
        }
    
    def _calculate_seo_score(self, audit):
        """Calculate overall SEO score."""
        score = 0
        max_score = 100
        
        # Title (20 points)
        if audit['title_analysis']['has_title']:
            score += 10
        if audit['title_analysis']['optimal_length']:
            score += 10
        
        # Meta description (15 points)
        if audit['meta_analysis']['has_description']:
            score += 8
        if audit['meta_analysis']['optimal_description_length']:
            score += 7
        
        # Headings (15 points)
        if audit['heading_analysis']['has_h1']:
            score += 8
        if audit['heading_analysis']['h1_count'] == 1:
            score += 7
        
        # Content (20 points)
        if audit['content_analysis']['has_sufficient_content']:
            score += 20
        
        # Images (10 points)
        if audit['image_analysis']['alt_text_coverage'] >= 80:
            score += 10
        elif audit['image_analysis']['alt_text_coverage'] >= 50:
            score += 5
        
        # Technical (20 points)
        if audit['technical_analysis']['is_https']:
            score += 5
        if audit['technical_analysis']['has_canonical']:
            score += 5
        if audit['technical_analysis']['has_viewport']:
            score += 5
        if audit['technical_analysis']['response_time'] < 3:
            score += 5
        
        return min(score, max_score)
    
    def _calculate_performance_score(self, audit):
        """Calculate performance score."""
        score = 100
        
        # Page size penalty
        if audit['page_size'] > 1000000:  # 1MB
            score -= 20
        elif audit['page_size'] > 500000:  # 500KB
            score -= 10
        
        # Load time penalty
        if audit['load_time'] > 5:
            score -= 30
        elif audit['load_time'] > 3:
            score -= 15
        elif audit['load_time'] > 1:
            score -= 5
        
        return max(score, 0)
    
    def _get_title_issues(self, title):
        """Get title-related issues."""
        issues = []
        if not title:
            issues.append("Missing page title")
        elif len(title) < 30:
            issues.append("Title too short (less than 30 characters)")
        elif len(title) > 60:
            issues.append("Title too long (more than 60 characters)")
        return issues
    
    def _get_meta_issues(self, description):
        """Get meta description issues."""
        issues = []
        if not description:
            issues.append("Missing meta description")
        elif len(description) < 120:
            issues.append("Meta description too short")
        elif len(description) > 160:
            issues.append("Meta description too long")
        return issues
    
    def _get_heading_issues(self, headings):
        """Get heading structure issues."""
        issues = []
        if headings['h1']['count'] == 0:
            issues.append("Missing H1 tag")
        elif headings['h1']['count'] > 1:
            issues.append("Multiple H1 tags found")
        return issues
    
    def _get_content_issues(self, words):
        """Get content-related issues."""
        issues = []
        if len(words) < 300:
            issues.append("Insufficient content (less than 300 words)")
        return issues
    
    def _get_image_issues(self, images_without_alt):
        """Get image-related issues."""
        issues = []
        if images_without_alt > 0:
            issues.append(f"{images_without_alt} images missing alt text")
        return issues
    
    def _get_link_issues(self, links):
        """Get link-related issues."""
        issues = []
        broken_links = [link for link in links if not link.get('href') or link['href'].strip() == '']
        if broken_links:
            issues.append(f"{len(broken_links)} empty or broken links found")
        return issues
    
    def _get_technical_issues(self, canonical, viewport, is_https, response):
        """Get technical SEO issues."""
        issues = []
        if not is_https:
            issues.append("Website not using HTTPS")
        if not canonical:
            issues.append("Missing canonical URL")
        if not viewport:
            issues.append("Missing viewport meta tag")
        if response.elapsed.total_seconds() > 3:
            issues.append("Slow page load time")
        return issues
    
    def _check_heading_hierarchy(self, structure):
        """Check if heading hierarchy is proper."""
        if not structure:
            return False
        
        current_level = 0
        for heading in structure:
            if heading['level'] > current_level + 1:
                return False
            current_level = max(current_level, heading['level'])
        
        return True
    
    def _calculate_readability(self, text):
        """Simple readability score calculation."""
        sentences = len(re.split(r'[.!?]+', text))
        words = len(text.split())
        
        if sentences == 0 or words == 0:
            return 0
        
        avg_sentence_length = words / sentences
        
        # Simple readability score (higher is better)
        if avg_sentence_length <= 15:
            return 90
        elif avg_sentence_length <= 20:
            return 70
        elif avg_sentence_length <= 25:
            return 50
        else:
            return 30

auditor = SEOAuditor()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .audit-form {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        input[type="url"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        input[type="url"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .results {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            display: none;
        }
        
        .score-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .score-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }
        
        .score-value {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .score-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .analysis-section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .metric {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.2rem;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .issues {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .issues h4 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        .issue-item {
            color: #856404;
            margin-bottom: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 SEO Audit Tool</h1>
            <p>Comprehensive SEO analysis for your website</p>
        </div>
        
        <div class="audit-form">
            <form id="auditForm">
                <div class="form-group">
                    <label for="url">Website URL:</label>
                    <input type="url" id="url" name="url" placeholder="https://example.com" required>
                </div>
                <button type="submit" class="btn">🚀 Start SEO Audit</button>
            </form>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing your website... This may take a few moments.</p>
        </div>
        
        <div class="results" id="results">
            <!-- Results will be populated here -->
        </div>
    </div>

    <script>
        document.getElementById('auditForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const url = document.getElementById('url').value;
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Show loading
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const response = await fetch('/audit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    alert('Error: ' + data.error);
                    return;
                }
                
                displayResults(data);
                
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                loading.style.display = 'none';
            }
        });
        
        function displayResults(audit) {
            const results = document.getElementById('results');
            
            results.innerHTML = `
                <div class="score-section">
                    <div class="score-card">
                        <div class="score-value">${audit.seo_score}</div>
                        <div class="score-label">SEO Score</div>
                    </div>
                    <div class="score-card">
                        <div class="score-value">${audit.performance_score}</div>
                        <div class="score-label">Performance Score</div>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h3 class="section-title">📝 Title & Meta Analysis</h3>
                    <div class="metric-grid">
                        <div class="metric">
                            <div class="metric-label">Page Title</div>
                            <div class="metric-value">${audit.title_analysis.title || 'Not found'}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Title Length</div>
                            <div class="metric-value">${audit.title_analysis.length} characters</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Meta Description</div>
                            <div class="metric-value">${audit.meta_analysis.description || 'Not found'}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Description Length</div>
                            <div class="metric-value">${audit.meta_analysis.description_length} characters</div>
                        </div>
                    </div>
                    ${generateIssues([...audit.title_analysis.issues, ...audit.meta_analysis.issues])}
                </div>
                
                <div class="analysis-section">
                    <h3 class="section-title">📊 Content Analysis</h3>
                    <div class="metric-grid">
                        <div class="metric">
                            <div class="metric-label">Word Count</div>
                            <div class="metric-value">${audit.content_analysis.word_count}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">H1 Tags</div>
                            <div class="metric-value">${audit.heading_analysis.h1_count}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Images</div>
                            <div class="metric-value">${audit.image_analysis.total_images}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Alt Text Coverage</div>
                            <div class="metric-value">${audit.image_analysis.alt_text_coverage.toFixed(1)}%</div>
                        </div>
                    </div>
                    ${generateIssues([...audit.content_analysis.issues, ...audit.heading_analysis.issues, ...audit.image_analysis.issues])}
                </div>
                
                <div class="analysis-section">
                    <h3 class="section-title">🔧 Technical Analysis</h3>
                    <div class="metric-grid">
                        <div class="metric">
                            <div class="metric-label">HTTPS</div>
                            <div class="metric-value">${audit.technical_analysis.is_https ? 'Yes' : 'No'}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Load Time</div>
                            <div class="metric-value">${audit.load_time.toFixed(2)}s</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Page Size</div>
                            <div class="metric-value">${(audit.page_size / 1024).toFixed(1)} KB</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Status Code</div>
                            <div class="metric-value">${audit.status_code}</div>
                        </div>
                    </div>
                    ${generateIssues(audit.technical_analysis.issues)}
                </div>
            `;
            
            results.style.display = 'block';
        }
        
        function generateIssues(issues) {
            if (issues.length === 0) {
                return '<div style="color: #27ae60; font-weight: 600;">✅ No issues found in this section</div>';
            }
            
            return `
                <div class="issues">
                    <h4>⚠️ Issues Found:</h4>
                    ${issues.map(issue => `<div class="issue-item">• ${issue}</div>`).join('')}
                </div>
            `;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main audit tool page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/audit', methods=['POST'])
def audit_website():
    """Perform SEO audit on submitted URL."""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Perform audit
    results = auditor.audit_website(url)
    
    return jsonify(results)

def main():
    """Main execution function."""
    print("SEO Audit Tool")
    print("=" * 20)
    
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

