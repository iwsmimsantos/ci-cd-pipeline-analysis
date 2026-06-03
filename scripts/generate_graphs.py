#!/usr/bin/env python3
"""
GitHub Actions Workflow Metrics Visualization

Generates comprehensive visualizations from collected workflow metrics:
1. Total pipeline time distribution
2. Time per job
3. Success vs Failure rates
4. Tests count vs Duration
5. Cache effect on performance
6. Parallel vs Sequential job execution
7. Step execution heatmap
8. Lead time trend
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
import numpy as np
from pathlib import Path

# Configuration
METRICS_CSV = 'workflow_metrics.csv'
METRICS_JSON = 'workflow_metrics.json'
GRAPHS_DIR = 'graphs'
FIGURE_DPI = 300
FIGURE_FORMAT = 'png'

# Create graphs directory
Path(GRAPHS_DIR).mkdir(exist_ok=True)

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class WorkflowMetricsVisualizer:
    """Generate visualizations from workflow metrics."""
    
    def __init__(self, csv_file: str, json_file: str):
        """Load metrics data."""
        self.df = pd.read_csv(csv_file)
        with open(json_file, 'r') as f:
            self.json_data = json.load(f)
        
        # Parse timestamps
        self.df['workflow_created_at'] = pd.to_datetime(self.df['workflow_created_at'])
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
        print(f"✅ Loaded {len(self.df)} records from {csv_file}")
    
    def graph_1_pipeline_time_distribution(self):
        """Graph 1: Total pipeline time distribution."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        workflow_times = self.df.groupby('workflow_id')['workflow_duration_seconds'].first()
        
        ax.hist(workflow_times, bins=15, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Pipeline Duration (seconds)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Pipeline Execution Time Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        stats_text = f"Mean: {workflow_times.mean():.1f}s\nMedian: {workflow_times.median():.1f}s\nMax: {workflow_times.max():.1f}s"
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, 
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/01_pipeline_time_distribution.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 1: Pipeline time distribution")
    
    def graph_2_time_per_job(self):
        """Graph 2: Average time per job."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        job_times = self.df.groupby('job_name')['job_duration_seconds'].agg(['mean', 'count'])
        job_times = job_times.sort_values('mean', ascending=False).head(10)
        
        bars = ax.barh(range(len(job_times)), job_times['mean'], color='coral', edgecolor='black')
        ax.set_yticks(range(len(job_times)))
        ax.set_yticklabels(job_times.index)
        ax.set_xlabel('Average Duration (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Longest Running Jobs (Average Duration)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (idx, row) in enumerate(job_times.iterrows()):
            ax.text(row['mean'], i, f" {row['mean']:.1f}s (n={int(row['count'])})", 
                   va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/02_time_per_job.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 2: Time per job")
    
    def graph_3_success_vs_failure(self):
        """Graph 3: Success vs Failure rates."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # By workflow
        workflow_status = self.df.groupby(['workflow_id', 'workflow_conclusion']).size().unstack(fill_value=0)
        if 'success' in workflow_status.columns and 'failure' in workflow_status.columns:
            success_count = (workflow_status['success'] > 0).sum()
            failure_count = (workflow_status['failure'] > 0).sum()
        else:
            success_count = len(self.df[self.df['workflow_conclusion'] == 'success'].drop_duplicates('workflow_id'))
            failure_count = len(self.df[self.df['workflow_conclusion'] == 'failure'].drop_duplicates('workflow_id'))
        
        # Pie chart
        labels = ['Success', 'Failure']
        sizes = [success_count, failure_count]
        colors = ['#2ecc71', '#e74c3c']
        explode = (0.05, 0.05)
        
        axes[0].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        axes[0].set_title('Workflow Success Rate', fontsize=13, fontweight='bold')
        
        # By job status
        job_success = (self.df['job_conclusion'] == 'success').sum()
        job_failure = (self.df['job_conclusion'] == 'failure').sum()
        
        job_labels = ['Success', 'Failure']
        job_sizes = [job_success, job_failure]
        
        axes[1].pie(job_sizes, explode=explode, labels=job_labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        axes[1].set_title('Job Success Rate', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/03_success_vs_failure.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 3: Success vs Failure")
    
    def graph_4_tests_vs_duration(self):
        """Graph 4: Test count vs Pipeline duration (correlation)."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Aggregate by workflow
        workflow_agg = self.df.groupby('workflow_id').agg({
            'workflow_duration_seconds': 'first',
            'step_name': 'count'
        }).rename(columns={'step_name': 'step_count'})
        
        scatter = ax.scatter(workflow_agg['step_count'], workflow_agg['workflow_duration_seconds'],
                           alpha=0.6, s=100, c=workflow_agg['workflow_duration_seconds'],
                           cmap='viridis', edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel('Number of Steps', fontsize=12, fontweight='bold')
        ax.set_ylabel('Pipeline Duration (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Pipeline Duration vs Number of Steps', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(workflow_agg['step_count'], workflow_agg['workflow_duration_seconds'], 1)
        p = np.poly1d(z)
        ax.plot(workflow_agg['step_count'].sort_values(), 
               p(workflow_agg['step_count'].sort_values()),
               "r--", alpha=0.8, linewidth=2, label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
        ax.legend(fontsize=10)
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Duration (s)', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/04_tests_vs_duration.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 4: Tests vs Duration")
    
    def graph_5_cache_effect(self):
        """Graph 5: Cache effect on performance."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Identify cache-related workflows
        with_cache = self.json_data[::2] if len(self.json_data) > 1 else self.json_data
        without_cache = self.json_data[1::2] if len(self.json_data) > 1 else []
        
        # Use commit messages to identify cache runs
        cache_enabled = self.df[self.df['commit_message'].str.contains('cache|enable', case=False, na=False)].copy()
        cache_disabled = self.df[self.df['commit_message'].str.contains('disable', case=False, na=False)].copy()
        
        if len(cache_enabled) > 0 and len(cache_disabled) > 0:
            cache_e_times = cache_enabled.groupby('workflow_id')['workflow_duration_seconds'].first().mean()
            cache_d_times = cache_disabled.groupby('workflow_id')['workflow_duration_seconds'].first().mean()
            
            conditions = ['Cache Enabled', 'Cache Disabled']
            times = [cache_e_times, cache_d_times]
            improvement = ((cache_d_times - cache_e_times) / cache_d_times * 100)
        else:
            # Fallback: compare early vs late runs
            mid_point = len(self.df) // 2
            times = [
                self.df.iloc[:mid_point].groupby('workflow_id')['workflow_duration_seconds'].first().mean(),
                self.df.iloc[mid_point:].groupby('workflow_id')['workflow_duration_seconds'].first().mean()
            ]
            conditions = ['Early Runs', 'Late Runs']
            improvement = ((times[1] - times[0]) / times[1] * 100)
        
        colors = ['#3498db', '#e74c3c']
        bars = ax.bar(conditions, times, color=colors, edgecolor='black', linewidth=2, alpha=0.8)
        
        ax.set_ylabel('Average Duration (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Cache Effect on Pipeline Performance', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, (bar, time) in enumerate(zip(bars, times)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{time:.1f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add improvement text
        improvement_text = f"{'Improvement' if improvement > 0 else 'Increase'}: {abs(improvement):.1f}%"
        ax.text(0.5, 0.95, improvement_text, transform=ax.transAxes,
               ha='center', va='top', fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/05_cache_effect.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 5: Cache effect")
    
    def graph_6_parallel_vs_sequential(self):
        """Graph 6: Parallel vs Sequential job execution."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Identify parallel vs sequential runs from commit messages
        parallel = self.df[self.df['commit_message'].str.contains('parallel', case=False, na=False)].copy()
        sequential = self.df[self.df['commit_message'].str.contains('sequential', case=False, na=False)].copy()
        
        if len(parallel) > 0 and len(sequential) > 0:
            parallel_times = parallel.groupby('workflow_id')['workflow_duration_seconds'].first().values
            sequential_times = sequential.groupby('workflow_id')['workflow_duration_seconds'].first().values
            
            data_to_plot = [parallel_times, sequential_times]
            labels = ['Parallel Jobs', 'Sequential Jobs']
        else:
            # Fallback
            all_times = self.df.groupby('workflow_id')['workflow_duration_seconds'].first().values
            mid = len(all_times) // 2
            data_to_plot = [all_times[:mid], all_times[mid:]]
            labels = ['Set A', 'Set B']
        
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True, 
                        medianprops=dict(color='red', linewidth=2),
                        boxprops=dict(facecolor='lightblue', alpha=0.7))
        
        ax.set_ylabel('Pipeline Duration (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Parallel vs Sequential Job Execution Performance', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add mean values
        for i, data in enumerate(data_to_plot):
            mean_val = np.mean(data)
            ax.plot(i+1, mean_val, 'D', color='orange', markersize=8, markeredgecolor='black')
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/06_parallel_vs_sequential.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 6: Parallel vs Sequential")
    
    def graph_7_step_execution_heatmap(self):
        """Graph 7: Step execution heatmap."""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Create step execution matrix
        step_job = self.df[['job_name', 'step_name', 'step_duration_seconds']].copy()
        step_job = step_job.dropna()
        
        # Aggregate by job and step
        heatmap_data = step_job.pivot_table(
            values='step_duration_seconds',
            index='step_name',
            columns='job_name',
            aggfunc='mean',
            fill_value=0
        )
        
        # Limit to top steps for readability
        heatmap_data = heatmap_data.head(15)
        
        sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Duration (seconds)'}, ax=ax, linewidths=0.5)
        
        ax.set_title('Step Execution Heatmap: Duration by Job and Step', fontsize=14, fontweight='bold')
        ax.set_xlabel('Job Name', fontsize=12, fontweight='bold')
        ax.set_ylabel('Step Name', fontsize=12, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/07_step_execution_heatmap.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 7: Step execution heatmap")
    
    def graph_8_lead_time_trend(self):
        """Graph 8: Lead time trend over time."""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Group by workflow and get first timestamp
        lead_times = self.df.groupby('workflow_id').agg({
            'workflow_created_at': 'first',
            'workflow_duration_seconds': 'first'
        }).reset_index()
        
        lead_times = lead_times.sort_values('workflow_created_at')
        
        ax.plot(lead_times['workflow_created_at'], lead_times['workflow_duration_seconds'],
               marker='o', linestyle='-', linewidth=2, markersize=6, color='steelblue', label='Pipeline Duration')
        
        # Add trend line
        lead_times['numeric_date'] = (lead_times['workflow_created_at'] - lead_times['workflow_created_at'].min()).dt.total_seconds()
        z = np.polyfit(lead_times['numeric_date'], lead_times['workflow_duration_seconds'], 2)
        p = np.poly1d(z)
        ax.plot(lead_times['workflow_created_at'], 
               p(lead_times['numeric_date']),
               "r--", alpha=0.8, linewidth=2, label='Trend (polynomial)')
        
        ax.set_xlabel('Timestamp', fontsize=12, fontweight='bold')
        ax.set_ylabel('Pipeline Duration (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Pipeline Lead Time Trend Over Time', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{GRAPHS_DIR}/08_lead_time_trend.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
        print("✅ Graph 8: Lead time trend")
    
    def generate_all(self):
        """Generate all graphs."""
        print("\n📊 Generating workflow metrics visualizations...\n")
        
        try:
            self.graph_1_pipeline_time_distribution()
            self.graph_2_time_per_job()
            self.graph_3_success_vs_failure()
            self.graph_4_tests_vs_duration()
            self.graph_5_cache_effect()
            self.graph_6_parallel_vs_sequential()
            self.graph_7_step_execution_heatmap()
            self.graph_8_lead_time_trend()
            
            print(f"\n✅ All graphs generated successfully!")
            print(f"📁 Saved to: {GRAPHS_DIR}/")
            print(f"📊 Total graphs: 8\n")
            
        except Exception as e:
            print(f"❌ Error generating graphs: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main function."""
    if not os.path.exists(METRICS_CSV):
        print(f"❌ Error: {METRICS_CSV} not found!")
        print("   Please run collect_metrics.py first")
        return
    
    visualizer = WorkflowMetricsVisualizer(METRICS_CSV, METRICS_JSON)
    visualizer.generate_all()


if __name__ == "__main__":
    main()
