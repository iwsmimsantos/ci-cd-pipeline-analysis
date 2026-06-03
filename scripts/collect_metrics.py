#!/usr/bin/env python3
"""
GitHub Actions Workflow Metrics Collector

Collects comprehensive metrics from GitHub Actions workflow runs:
- Workflow duration
- Job durations
- Step durations
- Workflow status
- Commit information (SHA, message)
- Timestamps
- Workflow IDs
- Artifact sizes

Outputs to CSV and JSON files.
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
import sys

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = 'iwsmimsantos/ci-cd-pipeline-analysis'
GITHUB_API_BASE = 'https://api.github.com'

# Output files
OUTPUT_CSV = 'workflow_metrics.csv'
OUTPUT_JSON = 'workflow_metrics.json'

class GitHubActionsCollector:
    """Collects metrics from GitHub Actions API"""
    
    def __init__(self, repo: str, token: str = None):
        self.repo = repo
        self.token = token
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'
        self.metrics = []
    
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make authenticated request to GitHub API"""
        url = f'{GITHUB_API_BASE}{endpoint}'
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'❌ API Request failed: {e}', file=sys.stderr)
            return {}
    
    def _get_artifact_sizes(self, run_id: int) -> int:
        """Get total artifact size for a workflow run"""
        endpoint = f'/repos/{self.repo}/actions/runs/{run_id}/artifacts'
        data = self._make_request(endpoint)
        
        total_size = 0
        if 'artifacts' in data:
            for artifact in data['artifacts']:
                total_size += artifact.get('size_in_bytes', 0)
        
        return total_size
    
    def _parse_duration(self, start_time: str, end_time: str) -> float:
        """Calculate duration in seconds between two ISO timestamps"""
        try:
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            return (end - start).total_seconds()
        except (ValueError, TypeError):
            return 0.0
    
    def _get_job_details(self, run_id: int) -> List[Dict[str, Any]]:
        """Get detailed job and step information for a workflow run"""
        endpoint = f'/repos/{self.repo}/actions/runs/{run_id}/jobs'
        data = self._make_request(endpoint)
        
        jobs_info = []
        if 'jobs' in data:
            for job in data['jobs']:
                job_info = {
                    'job_name': job.get('name', 'N/A'),
                    'job_id': job.get('id'),
                    'job_status': job.get('status', 'unknown'),
                    'job_conclusion': job.get('conclusion'),
                    'job_duration': self._parse_duration(
                        job.get('started_at', ''),
                        job.get('completed_at', '')
                    ),
                    'steps_count': len(job.get('steps', [])),
                    'steps': []
                }
                
                # Collect step information
                for step in job.get('steps', []):
                    step_info = {
                        'step_name': step.get('name', 'N/A'),
                        'step_status': step.get('status', 'unknown'),
                        'step_conclusion': step.get('conclusion'),
                        'step_duration': self._parse_duration(
                            step.get('started_at', ''),
                            step.get('completed_at', '')
                        )
                    }
                    job_info['steps'].append(step_info)
                
                jobs_info.append(job_info)
        
        return jobs_info
    
    def collect_workflows(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Collect metrics from recent workflow runs"""
        endpoint = f'/repos/{self.repo}/actions/runs?per_page={limit}'
        data = self._make_request(endpoint)
        
        if 'workflow_runs' not in data:
            print('❌ No workflow runs found or API error', file=sys.stderr)
            return []
        
        print(f'📊 Found {len(data["workflow_runs"])} workflow runs')
        
        for idx, run in enumerate(data['workflow_runs'], 1):
            print(f'  [{idx}/{len(data["workflow_runs"])}] Processing {run.get("name")}...', end=' ')
            
            # Get job and step details
            jobs_data = self._get_job_details(run['id'])
            
            # Get artifact sizes
            artifact_size = self._get_artifact_sizes(run['id'])
            
            # Calculate total workflow duration
            workflow_duration = self._parse_duration(
                run.get('created_at', ''),
                run.get('updated_at', '')
            )
            
            # Flatten jobs and steps for CSV
            if jobs_data:
                for job in jobs_data:
                    job_steps = job.pop('steps', [])
                    
                    if job_steps:
                        for step in job_steps:
                            metric_record = {
                                'workflow_id': run['id'],
                                'workflow_name': run.get('name', 'N/A'),
                                'workflow_status': run.get('status', 'unknown'),
                                'workflow_conclusion': run.get('conclusion'),
                                'workflow_duration_seconds': workflow_duration,
                                'workflow_created_at': run.get('created_at'),
                                'workflow_updated_at': run.get('updated_at'),
                                'commit_sha': run.get('head_commit', {}).get('id', 'N/A')[:8],
                                'commit_message': run.get('head_commit', {}).get('message', 'N/A')[:100],
                                'job_name': job['job_name'],
                                'job_id': job['job_id'],
                                'job_status': job['job_status'],
                                'job_conclusion': job['job_conclusion'],
                                'job_duration_seconds': job['job_duration'],
                                'step_name': step['step_name'],
                                'step_status': step['step_status'],
                                'step_conclusion': step['step_conclusion'],
                                'step_duration_seconds': step['step_duration'],
                                'artifact_size_bytes': artifact_size,
                                'timestamp': datetime.now().isoformat()
                            }
                            self.metrics.append(metric_record)
                    else:
                        # No steps - record job level
                        metric_record = {
                            'workflow_id': run['id'],
                            'workflow_name': run.get('name', 'N/A'),
                            'workflow_status': run.get('status', 'unknown'),
                            'workflow_conclusion': run.get('conclusion'),
                            'workflow_duration_seconds': workflow_duration,
                            'workflow_created_at': run.get('created_at'),
                            'workflow_updated_at': run.get('updated_at'),
                            'commit_sha': run.get('head_commit', {}).get('id', 'N/A')[:8],
                            'commit_message': run.get('head_commit', {}).get('message', 'N/A')[:100],
                            'job_name': job['job_name'],
                            'job_id': job['job_id'],
                            'job_status': job['job_status'],
                            'job_conclusion': job['job_conclusion'],
                            'job_duration_seconds': job['job_duration'],
                            'step_name': 'N/A',
                            'step_status': 'N/A',
                            'step_conclusion': 'N/A',
                            'step_duration_seconds': 0,
                            'artifact_size_bytes': artifact_size,
                            'timestamp': datetime.now().isoformat()
                        }
                        self.metrics.append(metric_record)
            else:
                # No jobs - record workflow level
                metric_record = {
                    'workflow_id': run['id'],
                    'workflow_name': run.get('name', 'N/A'),
                    'workflow_status': run.get('status', 'unknown'),
                    'workflow_conclusion': run.get('conclusion'),
                    'workflow_duration_seconds': workflow_duration,
                    'workflow_created_at': run.get('created_at'),
                    'workflow_updated_at': run.get('updated_at'),
                    'commit_sha': run.get('head_commit', {}).get('id', 'N/A')[:8],
                    'commit_message': run.get('head_commit', {}).get('message', 'N/A')[:100],
                    'job_name': 'N/A',
                    'job_id': 'N/A',
                    'job_status': 'N/A',
                    'job_conclusion': 'N/A',
                    'job_duration_seconds': 0,
                    'step_name': 'N/A',
                    'step_status': 'N/A',
                    'step_conclusion': 'N/A',
                    'step_duration_seconds': 0,
                    'artifact_size_bytes': artifact_size,
                    'timestamp': datetime.now().isoformat()
                }
                self.metrics.append(metric_record)
            
            print('✅')
        
        return self.metrics
    
    def save_csv(self, filename: str) -> None:
        """Save metrics to CSV file"""
        if not self.metrics:
            print('⚠️  No metrics to save', file=sys.stderr)
            return
        
        df = pd.DataFrame(self.metrics)
        df.to_csv(filename, index=False)
        print(f'💾 Metrics saved to {filename}')
        print(f'   Rows: {len(df)}')
        print(f'   Columns: {len(df.columns)}')
    
    def save_json(self, filename: str) -> None:
        """Save metrics to JSON file"""
        if not self.metrics:
            print('⚠️  No metrics to save', file=sys.stderr)
            return
        
        with open(filename, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f'💾 Metrics saved to {filename}')
        print(f'   Records: {len(self.metrics)}')


def main():
    """Main entry point"""
    print('🔄 GitHub Actions Metrics Collector')
    print('=' * 50)
    
    # Check for token
    if not GITHUB_TOKEN:
        print('⚠️  GITHUB_TOKEN not found in environment variables')
        print('   Set it: export GITHUB_TOKEN=your_github_token')
        print('   Proceeding with unauthenticated requests (limited rate)...')
    else:
        print(f'✅ GitHub token found (authenticated)')
    
    print(f'📦 Repository: {GITHUB_REPO}')
    print()
    
    # Create collector and gather metrics
    collector = GitHubActionsCollector(GITHUB_REPO, GITHUB_TOKEN)
    
    print('📊 Collecting workflow metrics...')
    collector.collect_workflows(limit=50)
    
    if not collector.metrics:
        print('❌ Failed to collect metrics', file=sys.stderr)
        return 1
    
    print()
    print('💾 Saving metrics...')
    collector.save_csv(OUTPUT_CSV)
    collector.save_json(OUTPUT_JSON)
    
    print()
    print('✅ Collection complete!')
    print(f'   CSV: {OUTPUT_CSV}')
    print(f'   JSON: {OUTPUT_JSON}')
    
    # Show summary statistics
    df = pd.DataFrame(collector.metrics)
    print()
    print('📈 Summary Statistics:')
    print(f'   Total records: {len(df)}')
    print(f'   Unique workflows: {df["workflow_id"].nunique()}')
    print(f'   Avg workflow duration: {df["workflow_duration_seconds"].mean():.2f}s')
    print(f'   Avg job duration: {df["job_duration_seconds"].mean():.2f}s')
    print(f'   Total artifact size: {df["artifact_size_bytes"].sum() / (1024*1024):.2f} MB')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
