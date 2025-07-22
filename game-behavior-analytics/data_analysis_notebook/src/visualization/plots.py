"""
Clean plotting functions for the analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
import networkx as nx

# Helper functions
def prop_ci(data, col, categories):
    """Calculate proportions with confidence intervals."""
    n = len(data)
    props, ci_l, ci_u, counts = [], [], [], []
    for cat in categories:
        count = (data[col] == cat).sum()
        prop = count / n
        se = np.sqrt(prop * (1 - prop) / n)
        ci_low = max(0, prop - 1.96 * se)
        ci_high = min(1, prop + 1.96 * se)
        props.append(prop)
        ci_l.append(ci_low)
        ci_u.append(ci_high)
        counts.append(count)
    return props, ci_l, ci_u, counts

def create_bar_plot(ax, x, control_props, control_ci_l, control_ci_u, control_counts,
                   interv_props, interv_ci_l, interv_ci_u, interv_counts,
                   labels, title, ylabel, control_n, interv_n):
    """Create a single bar plot with error bars and annotations."""
    bar_width = 0.35
    font_large = 14
    
    bars1 = ax.bar(x - bar_width/2, control_props, bar_width, 
                   yerr=[np.array(control_props)-np.array(control_ci_l), 
                        np.array(control_ci_u)-np.array(control_props)],
                   capsize=5, label=f'Control (n={control_n})', 
                   color='gray', alpha=0.6)
    
    bars2 = ax.bar(x + bar_width/2, interv_props, bar_width,
                   yerr=[np.array(interv_props)-np.array(interv_ci_l), 
                        np.array(interv_ci_u)-np.array(interv_props)],
                   capsize=5, label=f'Intervention (n={interv_n})', 
                   color='black', alpha=0.6)
    
    # Annotate counts
    for bars, counts in zip([bars1, bars2], [control_counts, interv_counts]):
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    count, ha='center', va='bottom', fontweight='bold', fontsize=font_large)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=font_large)
    ax.set_title(title, fontsize=font_large + 2)
    ax.set_ylabel(ylabel, fontsize=font_large)
    ax.tick_params(axis='y', labelsize=font_large)

def create_boxplot_pair(ax, control_data, interv_data, labels, title, ylabel, 
                       control_n, interv_n, ylim=None):
    """Create paired boxplots for control vs intervention."""
    bp = ax.boxplot([control_data, interv_data], labels=labels, patch_artist=True)
    
    colors = ['gray', 'black']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.tick_params(axis='both', labelsize=12)
    ax.grid(True, alpha=0.3)
    
    if ylim:
        ax.set_ylim(ylim)

def create_grouped_boxplots(ax, control_data_list, interv_data_list, positions, 
                           labels, title, ylabel, ylim=None):
    """Create grouped boxplots by category."""
    bp1 = ax.boxplot(control_data_list, positions=[p - 0.2 for p in positions], 
                     widths=0.3, patch_artist=True, manage_ticks=False)
    bp2 = ax.boxplot(interv_data_list, positions=[p + 0.2 for p in positions], 
                     widths=0.3, patch_artist=True, manage_ticks=False)
    
    for patch in bp1['boxes']:
        patch.set_facecolor('gray')
        patch.set_alpha(0.6)
    for patch in bp2['boxes']:
        patch.set_facecolor('black')
        patch.set_alpha(0.6)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(True, alpha=0.3)
    
    if ylim:
        ax.set_ylim(ylim)

def plot_cheating_distribution(df):
    """Create cheating behavior distribution plots matching original style."""
    control = df[df['concept'] == 'control']
    intervention = df[df['concept'] != 'control']
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    
    # Plot 1: Binary cheating
    cats1 = [0, 1]
    control_p1, ci_l1, ci_u1, counts1 = prop_ci(control, 'cheated_binary', cats1)
    interv_p1, ci_l2, ci_u2, counts2 = prop_ci(intervention, 'cheated_binary', cats1)
    
    create_bar_plot(axes[0], np.arange(len(cats1)), control_p1, ci_l1, ci_u1, counts1,
                   interv_p1, ci_l2, ci_u2, counts2,
                   ['Not Cheated', 'Cheated'], 
                   'Proportion of Participants Who Cheated \nvs Did Not Cheat',
                   'Proportion', len(control), len(intervention))
    
    # Plot 2: Three-category cheating
    cats2 = [0, 1, 2]
    control_p2, ci_l3, ci_u3, counts3 = prop_ci(control, 'cheating_behavior', cats2)
    interv_p2, ci_l4, ci_u4, counts4 = prop_ci(intervention, 'cheating_behavior', cats2)
    
    create_bar_plot(axes[1], np.arange(len(cats2)), control_p2, ci_l3, ci_u3, counts3,
                   interv_p2, ci_l4, ci_u4, counts4,
                   ['Non-cheater', 'Partial cheater', 'Full cheater'],
                   'Proportion of Participants by Cheating \nBehavior (Non, Partial, Full)',
                   '', len(control), len(intervention))  # No ylabel for second plot
    
    # Common formatting
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2, fontsize=14)
    plt.suptitle('Cheating Distribution: Control vs Intervention', 
                 fontsize=18, fontweight='bold')
    plt.tight_layout(rect=[0, 0.1, 1, 0.96])
    plt.show()

def plot_performance_distribution(df):
    """Create performance distribution plots matching original style."""
    control = df[df['concept'] == 'control']
    intervention = df[df['concept'] != 'control']
    
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    
    # Overall performance
    create_boxplot_pair(axes[0], control['performance'], intervention['performance'],
                       ['Control', 'Intervention'], 'Performance Distribution', 
                       'Performance Score', len(control), len(intervention))
    
    # Performance by cheating behavior
    positions = [0, 1, 2]
    control_perf_by_cheat = [control[control['cheating_behavior'] == i]['performance'].values 
                            for i in range(3)]
    interv_perf_by_cheat = [intervention[intervention['cheating_behavior'] == i]['performance'].values 
                           for i in range(3)]
    
    create_grouped_boxplots(axes[1], control_perf_by_cheat, interv_perf_by_cheat, positions,
                          ['Non-cheater', 'Partial cheater', 'Full cheater'],
                          'Performance by Cheating Behavior', 'Performance Score')
    
    # Legend
    legend_elements = [Patch(facecolor='gray', alpha=0.6, label=f'Control (n={len(control)})'),
                       Patch(facecolor='black', alpha=0.6, label=f'Intervention (n={len(intervention)})')]
    fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), 
               ncol=2, fontsize=14)
    
    fig.suptitle('Performance: Control vs Intervention', fontsize=18, fontweight='bold')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15)
    plt.show()

def plot_experience_distribution(df):
    """Create experience distribution plots matching original style."""
    control = df[df['concept'] == 'control']
    intervention = df[df['concept'] != 'control']
    
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    
    # Overall experience
    create_boxplot_pair(axes[0], control['experience'], intervention['experience'],
                       ['Control', 'Intervention'], 'Experience Distribution', 
                       'Experience Rating (1-7)', len(control), len(intervention), ylim=(1, 7))
    
    # Experience by cheating behavior
    positions = [0, 1, 2]
    control_exp_by_cheat = [control[control['cheating_behavior'] == i]['experience'].values 
                           for i in range(3)]
    interv_exp_by_cheat = [intervention[intervention['cheating_behavior'] == i]['experience'].values 
                          for i in range(3)]
    
    create_grouped_boxplots(axes[1], control_exp_by_cheat, interv_exp_by_cheat, positions,
                          ['Non-cheater', 'Partial cheater', 'Full cheater'],
                          'Experience by Cheating Behavior', 'Experience Rating (1-7)', 
                          ylim=(1, 7))
    
    # Legend
    legend_elements = [Patch(facecolor='gray', alpha=0.6, label=f'Control (n={len(control)})'),
                       Patch(facecolor='black', alpha=0.6, label=f'Intervention (n={len(intervention)})')]
    fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), 
               ncol=2, fontsize=14)
    
    fig.suptitle('Experience: Control vs Intervention', fontsize=18, fontweight='bold')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15)
    plt.show()

def plot_descriptive_stats(df):
    """Create all descriptive statistics plots."""
    plot_cheating_distribution(df)
    plot_performance_distribution(df)
    plot_experience_distribution(df)

def plot_effect_with_hdi(ax, mean, hdi, title, xlabel, ylabel='Overall Effect'):
    """Plot a single effect with HDI."""
    ax.plot([hdi[0], hdi[1]], [0, 0], 'k-', linewidth=4)
    ax.plot(mean, 0, 'ks', markersize=12)
    ax.axvline(0, color='red', linestyle='--', alpha=0.7)
    
    ax.text(mean, -0.1, f'{mean:+.1f}%\n[{hdi[0]:+.1f}, {hdi[1]:+.1f}]', 
            ha='center', va='top', fontweight='bold', fontsize=12)
    
    ax.set_ylim(-0.2, 0.2)
    ax.set_yticks([0])
    ax.set_yticklabels([ylabel], fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.3)

def plot_cheating_effects(effects):
    """Plot intervention effects matching original forest plots exactly."""
    
    categories = ['Non', 'Partial', 'Full']
    titles = ['Non-cheater Rate Change', 'Partial Cheater Rate Change', 'Full Cheater Rate Change']
    overall_results = effects['overall_effects']
    control_probs = effects['control_probs']
    
    # Control baseline rates for labels
    control_rates = {
        'Non': control_probs[:, 0].mean() * 100,
        'Partial': control_probs[:, 1].mean() * 100,
        'Full': control_probs[:, 2].mean() * 100
    }
    
    # PLOT 1: Overall intervention effect
    fig1, axes1 = plt.subplots(1, 3, figsize=(14, 4))
    
    for idx, (cat, title) in enumerate(zip(categories, titles)):
        ax = axes1[idx]
        
        mean = overall_results[cat]['mean']
        hdi = overall_results[cat]['hdi']
        
        ax.plot([hdi[0], hdi[1]], [0, 0], color='black', linewidth=3)
        ax.plot(mean, 0, 's', color='black', markersize=12)
        
        ax.text(mean, -0.15, f'{mean:+.1f}\n[{hdi[0]:+.1f}, {hdi[1]:+.1f}]', 
                ha='center', va='center', fontweight='bold', fontsize=12)
        
        ax.axvline(0, color='black', linestyle='--', alpha=0.5)
        
        if idx == 0:
            ax.set_yticks([0])
            ax.set_yticklabels(['Overall Intervention Effect'], fontsize=14, fontweight='bold')
        else:
            ax.set_yticks([])
        
        ax.tick_params(axis='x', labelsize=14)
        ax.set_xlabel(f'Percentage Point Change from \nControl ({control_rates[cat]:.1f}%)', fontsize=14)
        ax.set_title(title, fontweight='bold', fontsize=16, pad=20)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.3, 0.3)
        
        xlim = ax.get_xlim()
        if cat == 'Non':
            ax.text(xlim[0] * 0.8, 0.25, 'Honest Test\nTaking ↓', ha='center', va='center', fontsize=12, style='italic')
            ax.text(xlim[1] * 0.8, 0.25, 'Honest Test\nTaking ↑', ha='center', va='center', fontsize=12, style='italic')
        else:
            ax.text(xlim[0] * 0.8, 0.25, 'Honest Test\nTaking ↑', ha='center', va='center', fontsize=12, style='italic')
            ax.text(xlim[1] * 0.8, 0.25, 'Honest Test\nTaking ↓', ha='center', va='center', fontsize=12, style='italic')

    plt.suptitle('Overall Intervention Effect: Concept-Based Messages Increase Honest\nTest-Taking by ~12% while Reducing Full Cheating by ~11%', 
                 fontsize=18, fontweight='bold', color="black", alpha=0.7, y=0.97)
    plt.tight_layout()
    plt.subplots_adjust(top=0.6)
    plt.show()
    
    # PLOT 2: By-concept effects (using concept_effects from the model)
    if 'concept_effects' in effects:
        concept_results = effects['concept_effects']
        
        # Theory organization
        theory_order_viz = ['Self-Determination Theory', 'Cognitive Dissonance Theory', 
                           'Self-Efficacy Theory', 'Social Norms Theory'][::-1]
        theory_colors = {'Self-Determination Theory': "#007C36", 
                        'Cognitive Dissonance Theory': '#4B0082',
                        'Self-Efficacy Theory': '#DC143C', 
                        'Social Norms Theory': "#C06900"}
        
        # Convert to DataFrame and sort by theory  
        df_results = pd.DataFrame(concept_results)
        df_results['theory'] = pd.Categorical(df_results['theory'], categories=theory_order_viz, ordered=True)
        df_results_sorted = df_results.sort_values(['theory', 'concept_label']).reset_index(drop=True)
        
        fig2, axes2 = plt.subplots(1, 3, figsize=(16, 10))
        
        for idx, (cat, title) in enumerate(zip(categories, titles)):
            ax = axes2[idx]
            means = df_results_sorted[f'{cat.lower()}_mean'].values
            hdis = np.array([row[f'{cat.lower()}_hdi'] for _, row in df_results_sorted.iterrows()])
            
            y_positions = np.arange(len(df_results_sorted))
            
            # Highlight best concept per theory
            highlight_indices = []
            for theory in theory_order_viz:
                indices = df_results_sorted.index[df_results_sorted['theory'] == theory].tolist()
                if indices:
                    theory_means = means[indices]
                    target_idx = indices[np.argmax(theory_means)] if cat == 'Non' else indices[np.argmin(theory_means)]
                    highlight_indices.append(target_idx)
            
            # Background shading by theory
            for theory in theory_order_viz:
                indices = df_results_sorted.index[df_results_sorted['theory'] == theory].tolist()
                if indices:
                    ax.axhspan(indices[0]-0.5, indices[-1]+0.5, alpha=0.1, color=theory_colors[theory])
            
            # Forest plot
            for i in range(len(df_results_sorted)):
                color = theory_colors[df_results_sorted.iloc[i]['theory']]
                alpha = 1.0 if i in highlight_indices else 0.4
                ax.plot([hdis[i][0], hdis[i][1]], [i, i], color=color, alpha=alpha, linewidth=2)
                ax.plot(means[i], i, 's', color=color, alpha=alpha, markersize=8)
            
            # Overall estimate diamond
            overall_mean = means.mean()
            overall_se = np.std(means) / np.sqrt(len(means))
            diamond_y = len(df_results_sorted) + 0.5
            diamond_x = [overall_mean - 1.96*overall_se, overall_mean, overall_mean + 1.96*overall_se, overall_mean, overall_mean - 1.96*overall_se]
            diamond_y_coords = [diamond_y, diamond_y + 0.2, diamond_y, diamond_y - 0.2, diamond_y]
            ax.fill(diamond_x, diamond_y_coords, color='black', alpha=0.7)
            
            ax.axvline(0, color='black', linestyle='--', alpha=0.5)

            if idx == 0:
                ax.set_yticks(list(y_positions) + [diamond_y])
                y_labels = df_results_sorted['concept_label'].tolist() + ['Overall estimate']
                ax.set_yticklabels(y_labels, fontsize=14, fontweight='bold')

                for tick_label, concept in zip(ax.get_yticklabels()[:-1], df_results_sorted['concept_label']):
                    theory = df_results_sorted.loc[df_results_sorted['concept_label'] == concept, 'theory'].values[0]
                    tick_label.set_color(theory_colors[theory])
                ax.get_yticklabels()[-1].set_color('black')
            else:
                ax.set_yticks([])

            ax.tick_params(axis='x', labelsize=14)
            ax.set_xlabel(f'Percentage Point Change from \nControl ({control_rates[cat]:.1f}%)', fontsize=14)
            ax.set_title(title, fontweight='bold', fontsize=16, pad=20)
            ax.grid(True, alpha=0.3)
            
            xlim = ax.get_xlim()
            if cat == 'Non':
                ax.text(xlim[0] * 0.8, len(df_results_sorted) + 1, 'Honest Test\nTaking ↓', ha='center', va='center', fontsize=12, style='italic')
                ax.text(xlim[1] * 0.8, len(df_results_sorted) + 1, 'Honest Test\nTaking ↑', ha='center', va='center', fontsize=12, style='italic')
            else:
                ax.text(xlim[0] * 0.8, len(df_results_sorted) + 1, 'Honest Test\nTaking ↑', ha='center', va='center', fontsize=12, style='italic')
                ax.text(xlim[1] * 0.8, len(df_results_sorted) + 1, 'Honest Test\nTaking ↓', ha='center', va='center', fontsize=12, style='italic')

        # Legend for theories
        import matplotlib.patches as patches
        legend_elements = [patches.Patch(color=color, label=f"Concepts of {theory}") for theory, color in theory_colors.items()]
        fig2.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=14)

        plt.suptitle('Message Related to \'Reference Group Identification\' Most Increases Honest \nTest-Taking Overall. Messages Focusing on \'Cognitive Inconsistency\' and \'Verbal\n Persuasion\' Can Reduce Full Cheating, While Effects on Partial Cheating Are Minimal', 
                 fontsize=20, fontweight='bold', color='black', alpha=0.7, y=0.95)

        plt.tight_layout()
        plt.subplots_adjust(top=0.75, bottom=0.1)
        plt.show()

def plot_performance_experience_effects(effects):
    """Plot performance and experience effects matching original style."""
    
    # Check if we have the multivariate results structure from original
    if 'multivariate_results' in effects:
        # Use the detailed multivariate results
        results = effects['multivariate_results']
        
        outcomes = [
            ('Performance', [
                (results['perf_non']['mean'], results['perf_non']['hdi']),
                (results['perf_partial']['mean'], results['perf_partial']['hdi']),
                (results['perf_full']['mean'], results['perf_full']['hdi'])
            ]),
            ('Experience', [
                (results['exp_non']['mean'], results['exp_non']['hdi']),
                (results['exp_partial']['mean'], results['exp_partial']['hdi']),
                (results['exp_full']['mean'], results['exp_full']['hdi'])
            ])
        ]
        groups = ['Non-Cheater', 'Partial Cheater', 'Full Cheater']
        control_baselines = {
            'Performance': effects['baselines']['performance_by_cheating'],
            'Experience': effects['baselines']['experience_by_cheating']
        }
        
    else:
        # Fallback for simple results structure
        if 'performance' in effects and 'experience' in effects:
            # Create simplified structure
            outcomes = [
                ('Performance', [(effects['performance']['mean'], effects['performance']['hdi'])]),
                ('Experience', [(effects['experience']['mean'], effects['experience']['hdi'])])
            ]
            groups = ['Overall Effect']
            control_baselines = {
                'Performance': [effects['baselines']['performance_by_cheating'][0]] if 'baselines' in effects else [20.0],
                'Experience': [effects['baselines']['experience_by_cheating'][0]] if 'baselines' in effects else [5.5]
            }
        else:
            print("⚠️ No performance/experience effects to plot")
            return
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    for idx, (outcome_name, group_effects) in enumerate(outcomes):
        ax = axes[idx]
        
        for i, (group, (mean, hdi)) in enumerate(zip(groups, group_effects)):
            # Plot effect with HDI
            ax.plot([hdi[0], hdi[1]], [i, i], color='black', linewidth=3)
            ax.plot(mean, i, 's', color='black', markersize=10)
            
            # Add value label
            ax.text(mean, i - 0.3, f'{mean:+.3f}\n[{hdi[0]:+.3f}, {hdi[1]:+.3f}]', 
                    ha='center', va='center', fontweight='bold', fontsize=10)
        
        ax.axvline(0, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.set_yticks(range(len(groups)))
        ax.set_yticklabels(groups, fontsize=12, fontweight='bold')
        
        if len(groups) == 3:  # Full multivariate results
            baseline_text = f"Non-: {control_baselines[outcome_name][0]:.1f}, " + \
                           f"Partial-: {control_baselines[outcome_name][1]:.1f}, " + \
                           f"Full cheater: {control_baselines[outcome_name][2]:.1f}"
        else:  # Simple results
            baseline_text = f"Baseline: {control_baselines[outcome_name][0]:.1f}"
        
        ax.set_xlabel(f'{outcome_name} Change from Control (Baselines -\n {baseline_text})', 
                     fontsize=11, fontweight='bold')
        ax.set_title(f'{outcome_name} Change', fontweight='bold', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.5, len(groups) - 0.5)
        
        # Add interpretation text
        xlim = ax.get_xlim()
        ax.text(xlim[0] * 0.8, len(groups) - 0.3, 'Worse ←', ha='center', va='center', 
                fontsize=10, style='italic', color='black')
        ax.text(xlim[1] * 0.8, len(groups) - 0.3, '→ Better', ha='center', va='center', 
                fontsize=10, style='italic', color='black')
    
    plt.suptitle('Overall Intervention Effect: Concept-Based Interventions Show No Meaningful Performance \nor Experience Costs. All Effects Near Zero with 95% Credible Intervals Spanning Zero', 
                 fontsize=16, fontweight='bold', color='black', alpha=0.7, y=0.95)
    plt.tight_layout()
    plt.subplots_adjust(top=0.7)
    plt.show()
    
def plot_control_vs_overall_networks(network_results, labels):
    """Plot 1: Control vs Overall Intervention Networks (2 subplots)"""
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # FIXED NODE POSITIONING - same for both subplots
    mechanism_nodes = ['need_satisfaction', 'need_frustration', 'self_efficacy', 'norm_perception', 'cognitive_discomfort']
    outcome_nodes = ['cheating', 'performance', 'experience']
    
    # Create fixed positions
    pos_fixed = {}
    
    # Mechanisms in a circle on the left side
    mechanism_angles = np.linspace(0, 2*np.pi, len(mechanism_nodes), endpoint=False)
    for i, mech in enumerate(mechanism_nodes):
        mech_idx = labels.index(mech)
        pos_fixed[mech_idx] = (
            0.3 + 0.25 * np.cos(mechanism_angles[i]),
            0.5 + 0.25 * np.sin(mechanism_angles[i])
        )
    
    # Outcomes in a vertical line on the right side
    for i, outcome in enumerate(outcome_nodes):
        outcome_idx = labels.index(outcome)
        pos_fixed[outcome_idx] = (0.8, 0.2 + i * 0.3)
    
    # Node colors and sizes
    node_colors = []
    node_sizes = []
    for label in labels:
        if label in mechanism_nodes:
            node_colors.append('lightblue')
            node_sizes.append(800)
        elif label in outcome_nodes:
            node_colors.append('salmon')
            node_sizes.append(1000)
        else:
            node_colors.append('lightgray')
            node_sizes.append(400)
    
    threshold = 0.15
    
    # Plot Control and Overall Intervention
    for i, (concept, title) in enumerate([('control', 'Control Group'), ('overall_intervention', 'Overall Intervention')]):
        ax = axes[i]
        
        if concept in network_results:
            matrix = network_results[concept]['partial_correlations']
            n = network_results[concept]['n_participants']
            
            # Create network graph
            G = nx.Graph()
            for j, label in enumerate(labels):
                G.add_node(j, label=label, pos=pos_fixed[j])
            
            # Add significant edges
            for j in range(len(labels)):
                for k in range(j+1, len(labels)):
                    weight = matrix[j, k]
                    if abs(weight) > threshold:
                        G.add_edge(j, k, weight=weight)
            
            pos = {node: pos_fixed[node] for node in G.nodes()}
            
            # Draw edges
            if G.edges():
                edge_weights = [abs(G[u][v]['weight']) * 5 for u, v in G.edges()]
                edge_colors = ['red' if G[u][v]['weight'] < 0 else 'green' for u, v in G.edges()]
                nx.draw_networkx_edges(G, pos, ax=ax, width=edge_weights, 
                                     edge_color=edge_colors, alpha=0.8)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, ax=ax, 
                                 node_color=[node_colors[node] for node in G.nodes()],
                                 node_size=[node_sizes[node] for node in G.nodes()], 
                                 alpha=0.9)
            
            # Draw labels
            label_dict = {}
            for j in G.nodes():
                if labels[j] in mechanism_nodes:
                    abbrev = {
                        'need_satisfaction': 'Need+',
                        'need_frustration': 'Need-', 
                        'self_efficacy': 'SelfEff',
                        'norm_perception': 'Norms',
                        'cognitive_discomfort': 'Discomf'
                    }
                    label_dict[j] = abbrev.get(labels[j], labels[j][:6])
                else:
                    label_dict[j] = labels[j].title()
            
            nx.draw_networkx_labels(G, pos, labels=label_dict, ax=ax, 
                                  font_size=10, font_weight='bold')
            
            # Title and info
            ax.set_title(f'{title}\n(n={n})', fontsize=14, fontweight='bold')
            
            # Network density
            if G.edges():
                density = len(G.edges()) / (len(labels) * (len(labels) - 1) / 2)
                ax.text(0.02, 0.98, f'Density: {density:.2f}', 
                       transform=ax.transAxes, fontsize=10, 
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        else:
            ax.text(0.5, 0.5, 'No Data\nAvailable', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=12, style='italic')
            ax.set_title(title, fontsize=14)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                  markersize=12, label='Psychological Mechanisms'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='salmon', 
                  markersize=12, label='Behavioral Outcomes'),
        plt.Line2D([0], [0], color='green', linewidth=3, label='Positive Correlation (r > +0.15)'),
        plt.Line2D([0], [0], color='red', linewidth=3, label='Negative Correlation (r < -0.15)')
    ]
    
    fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), 
               ncol=2, fontsize=11, frameon=True)
    
    plt.suptitle('Psychological Networks: Control vs Overall Intervention Comparison', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15, top=0.85)
    plt.show()

def plot_theory_networks_grid(network_results, labels):
    """Plot 2: Theory-Based Networks (4x4 grid organized by theory)"""
    
    # Theory organization
    theory_concepts = [
        ('Self-Determination Theory', ['autonomy', 'competence', 'relatedness', None]),  # 4th slot empty
        ('Cognitive Dissonance Theory', ['self_concept', 'cognitive_inconsistency', 'dissonance_arousal', 'dissonance_reduction']),
        ('Self-Efficacy Theory', ['performance_accomplishments', 'vicarious_experience', 'verbal_persuasion', 'emotional_arousal']),
        ('Social Norms Theory', ['descriptive_norms', 'injunctive_norms', 'social_sanctions', 'reference_group_identification'])
    ]
    
    theory_colors = {
        'Self-Determination Theory': '#007C36',
        'Cognitive Dissonance Theory': '#4B0082', 
        'Self-Efficacy Theory': '#DC143C',
        'Social Norms Theory': '#C06900'
    }
    
    fig, axes = plt.subplots(4, 4, figsize=(20, 16))
    
    # FIXED NODE POSITIONING
    mechanism_nodes = ['need_satisfaction', 'need_frustration', 'self_efficacy', 'norm_perception', 'cognitive_discomfort']
    outcome_nodes = ['cheating', 'performance', 'experience']
    
    pos_fixed = {}
    
    # Mechanisms in a circle on the left side
    mechanism_angles = np.linspace(0, 2*np.pi, len(mechanism_nodes), endpoint=False)
    for i, mech in enumerate(mechanism_nodes):
        mech_idx = labels.index(mech)
        pos_fixed[mech_idx] = (
            0.3 + 0.25 * np.cos(mechanism_angles[i]),
            0.5 + 0.25 * np.sin(mechanism_angles[i])
        )
    
    # Outcomes in a vertical line on the right side
    for i, outcome in enumerate(outcome_nodes):
        outcome_idx = labels.index(outcome)
        pos_fixed[outcome_idx] = (0.8, 0.2 + i * 0.3)
    
    # Node colors and sizes
    node_colors = []
    node_sizes = []
    for label in labels:
        if label in mechanism_nodes:
            node_colors.append('lightblue')
            node_sizes.append(800)
        elif label in outcome_nodes:
            node_colors.append('salmon')
            node_sizes.append(1000)
        else:
            node_colors.append('lightgray')
            node_sizes.append(400)
    
    threshold = 0.15
    
    # Plot theory networks
    for row, (theory_name, concepts) in enumerate(theory_concepts):
        for col, concept in enumerate(concepts):
            ax = axes[row, col]
            theory_color = theory_colors[theory_name]
            
            if concept and concept in network_results:
                matrix = network_results[concept]['partial_correlations']
                n = network_results[concept]['n_participants']
                
                # Create network graph
                G = nx.Graph()
                for j, label in enumerate(labels):
                    G.add_node(j, label=label, pos=pos_fixed[j])
                
                # Add significant edges
                for j in range(len(labels)):
                    for k in range(j+1, len(labels)):
                        weight = matrix[j, k]
                        if abs(weight) > threshold:
                            G.add_edge(j, k, weight=weight)
                
                pos = {node: pos_fixed[node] for node in G.nodes()}
                
                # Draw edges
                if G.edges():
                    edge_weights = [abs(G[u][v]['weight']) * 5 for u, v in G.edges()]
                    edge_colors = ['red' if G[u][v]['weight'] < 0 else 'green' for u, v in G.edges()]
                    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_weights, 
                                         edge_color=edge_colors, alpha=0.8)
                
                # Draw nodes
                nx.draw_networkx_nodes(G, pos, ax=ax, 
                                     node_color=[node_colors[node] for node in G.nodes()],
                                     node_size=[node_sizes[node] for node in G.nodes()], 
                                     alpha=0.9)
                
                # Draw labels
                label_dict = {}
                for j in G.nodes():
                    if labels[j] in mechanism_nodes:
                        abbrev = {
                            'need_satisfaction': 'Need+',
                            'need_frustration': 'Need-', 
                            'self_efficacy': 'SelfEff',
                            'norm_perception': 'Norms',
                            'cognitive_discomfort': 'Discomf'
                        }
                        label_dict[j] = abbrev.get(labels[j], labels[j][:6])
                    else:
                        label_dict[j] = labels[j].title()
                
                nx.draw_networkx_labels(G, pos, labels=label_dict, ax=ax, 
                                      font_size=9, font_weight='bold')
                
                # Title
                title = concept.replace("_", " ").title()
                ax.set_title(f'{title}\n(n={n})', fontsize=11, fontweight='bold', color=theory_color)
                
                # Network density
                if G.edges():
                    density = len(G.edges()) / (len(labels) * (len(labels) - 1) / 2)
                    ax.text(0.02, 0.98, f'Density: {density:.2f}', 
                           transform=ax.transAxes, fontsize=8, 
                           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
            
            elif concept is None:
                # Empty slot (for Self-Determination Theory 4th position)
                ax.text(0.5, 0.5, '', ha='center', va='center', transform=ax.transAxes)
                ax.set_title('', fontsize=11)
            
            else:
                # No data available
                ax.text(0.5, 0.5, 'No Data\nAvailable', ha='center', va='center', 
                       transform=ax.transAxes, fontsize=10, style='italic')
                concept_title = concept.replace("_", " ").title() if concept else ""
                ax.set_title(concept_title, fontsize=11, color=theory_color)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Add theory label on the left
        fig.text(0.02, 0.875 - row * 0.225, theory_name, rotation=90, 
                va='center', ha='center', fontsize=14, fontweight='bold', 
                color=theory_colors[theory_name])
    
    # Enhanced legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                  markersize=15, label='Psychological Mechanisms'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='salmon', 
                  markersize=15, label='Behavioral Outcomes'),
        plt.Line2D([0], [0], color='green', linewidth=4, label='Positive Correlation (r > +0.15)'),
        plt.Line2D([0], [0], color='red', linewidth=4, label='Negative Correlation (r < -0.15)')
    ]
    
    fig.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.5, 0.02), 
               ncol=2, fontsize=12, frameon=True)
    
    plt.suptitle('Psychological Networks by Theory: Concept-Specific Mechanism → Outcome Patterns\n' +
                 'Left: Mechanisms (Need+/-, SelfEff, Norms, Discomf) | Right: Outcomes (Cheating, Performance, Experience)', 
                 fontsize=16, fontweight='bold', y=0.96)
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.08, bottom=0.12, top=0.88)
    plt.show()

def plot_concept_networks_two_plots(network_results, labels):
    """Create both network plots as requested"""
    
    # Plot 1: Control vs Overall Intervention
    plot_control_vs_overall_networks(network_results, labels)
    
    # Plot 2: Theory-based 4x4 grid
    plot_theory_networks_grid(network_results, labels)

def print_partial_correlation_tables(correlation_tables):
    """Print partial correlation matrices as tables"""
    
    print("\n" + "="*60)
    print("PARTIAL CORRELATION MATRICES")
    print("="*60)
    
    for concept, table in correlation_tables.items():
        print(f"\n{concept.upper()}:")
        print("-" * 40)
        
        # Round to 3 decimals for readability
        rounded_table = table.round(3)
        print(rounded_table.to_string())
        
        # Summary statistics
        abs_correlations = np.abs(table.values)
        np.fill_diagonal(abs_correlations, 0)  # Remove diagonal
        
        print(f"\nSummary for {concept}:")
        print(f"  Mean |correlation|: {abs_correlations.mean():.3f}")
        print(f"  Max |correlation|: {abs_correlations.max():.3f}")
        print(f"  Correlations > 0.2: {(abs_correlations > 0.2).sum()}")
       
def plot_pathway_effects(pathway_results):
    """Plot pathway analysis results matching original analysis style"""
    
    if pathway_results is None:
        print("⚠️ No pathway results to plot")
        return
    
    # Plot 1: Overall Intervention → Mechanisms
    create_concept_to_mechanisms_plot(pathway_results)
    
    # Plot 2: Mechanisms → Cheating Behavior  
    create_mechanisms_to_cheating_plot(pathway_results)
    
    # Plot 3: Mechanisms → Performance/Experience
    create_mechanisms_to_outcomes_plot(pathway_results)

def create_concept_to_mechanisms_plot(pathway_results):
    """Create 4x4 grid: Concepts → Mechanisms (by theory)"""
    
    mechanism_names = pathway_results['mechanism_names']
    all_concept_results = pathway_results['concept_to_mechanisms']
    
    # Theory order and colors
    theory_concepts = [
        ('Overall Intervention', ['overall_intervention']),
        ('Self-Determination Theory', ['autonomy', 'competence', 'relatedness']),
        ('Cognitive Dissonance Theory', ['self_concept', 'cognitive_inconsistency', 'dissonance_arousal', 'dissonance_reduction']),
        ('Self-Efficacy Theory', ['performance_accomplishments', 'vicarious_experience', 'verbal_persuasion', 'emotional_arousal']),
        ('Social Norms Theory', ['descriptive_norms', 'injunctive_norms', 'social_sanctions', 'reference_group_identification'])
    ]
    
    theory_colors = {
        'Overall Intervention': '#000000',
        'Self-Determination Theory': '#007C36',
        'Cognitive Dissonance Theory': '#4B0082', 
        'Self-Efficacy Theory': '#DC143C',
        'Social Norms Theory': '#C06900'
    }
    
    fig, axes = plt.subplots(4, 4, figsize=(16, 12))
    axes = axes.flatten()
    
    plot_idx = 0
    y_positions = np.arange(len(mechanism_names))
    
    for theory_name, concepts in theory_concepts:
        for concept in concepts:
            if plot_idx >= 16:  # 4x4 grid limit
                break
                
            ax = axes[plot_idx]
            color = theory_colors[theory_name]
            
            # Get concept-specific results
            if concept in all_concept_results:
                concept_results = all_concept_results[concept]
                title = 'Overall Intervention' if concept == 'overall_intervention' else concept.replace('_', ' ').title()
            else:
                # Skip if no data available
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
                ax.set_title(concept.replace('_', ' ').title(), fontweight='bold', fontsize=10)
                ax.axis('off')
                plot_idx += 1
                continue
            
            # Plot mechanism effects
            for i, mech_name in enumerate(mechanism_names):
                if mech_name in concept_results:
                    result = concept_results[mech_name]
                    mean = result['mean']
                    hdi = result['hdi']
                    
                    # Plot HDI and mean
                    ax.plot([hdi[0], hdi[1]], [i, i], color=color, linewidth=2, alpha=0.8)
                    ax.plot(mean, i, 's', color=color, markersize=6, alpha=0.8)
                    
                    # Add value label for significant effects
                    if hdi[0] > 0 or hdi[1] < 0:
                        ax.text(mean, i + 0.1, f'{mean:+.2f}', ha='center', va='bottom', 
                               fontweight='bold', fontsize=8, color=color)
            
            ax.axvline(0, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax.set_title(title, fontweight='bold', fontsize=10, color=color)
            ax.grid(True, alpha=0.2, axis='x')
            ax.set_ylim(-0.5, len(mechanism_names) - 0.5)
            
            # Y-axis labels only for leftmost plots
            if plot_idx % 4 == 0:
                ax.set_yticks(y_positions)
                ax.set_yticklabels([name[:8] + '...' if len(name) > 8 else name for name in mechanism_names], 
                                  fontsize=8)
            else:
                ax.set_yticks([])
            
            # X-axis labels only for bottom plots
            if plot_idx >= 12:
                ax.set_xlabel('Change from Control', fontsize=9)
            else:
                ax.set_xticks([])
            
            ax.tick_params(labelsize=8)
            plot_idx += 1
    
    # Hide unused subplots
    for idx in range(plot_idx, 16):
        axes[idx].set_visible(False)
    
    plt.suptitle('Concept → Psychological Mechanisms (by Theory)', 
                 fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

def create_mechanisms_to_cheating_plot(pathway_results):
    """Create forest plot: Mechanisms → Cheating Behavior"""
    
    mech_cheating_results = pathway_results['mechanisms_to_cheating']
    mechanism_names = pathway_results['mechanism_names']
    control_baselines = pathway_results['control_baselines']
    
    # Control baseline rates for labels
    control_probs = control_baselines['cheating_counts'] / control_baselines['cheating_counts'].sum()
    control_rates = {
        'Non': control_probs[0] * 100,
        'Partial': control_probs[1] * 100, 
        'Full': control_probs[2] * 100
    }
    
    categories = ['Non', 'Partial', 'Full']
    titles = ['Non-cheater Rate Change', 'Partial Cheater Rate Change', 'Full Cheater Rate Change']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    colors = ['#000000', '#36454F', '#818589']
    
    for idx, (cat, title, color) in enumerate(zip(categories, titles, colors)):
        ax = axes[idx]
        
        y_positions = np.arange(len(mechanism_names))
        
        for i, mech_name in enumerate(mechanism_names):
            if mech_name in mech_cheating_results:
                result = mech_cheating_results[mech_name][cat.lower()]
                mean = result['mean']
                hdi = result['hdi']
                
                # Plot HDI and mean
                ax.plot([hdi[0], hdi[1]], [i, i], color=color, linewidth=3, alpha=0.8)
                ax.plot(mean, i, 's', color=color, markersize=10, alpha=0.8)
                
                # Add value label for significant effects
                if hdi[0] > 0 or hdi[1] < 0:
                    ax.text(mean, i + 0.15, f'{mean:+.1f}', ha='center', va='bottom', 
                           fontweight='bold', fontsize=10, color=color)
        
        ax.axvline(0, color='black', linestyle='--', alpha=0.7, linewidth=2)
        
        if idx == 0:
            ax.set_yticks(y_positions)
            ax.set_yticklabels(mechanism_names, fontsize=12, fontweight='bold')
        else:
            ax.set_yticks([])
        
        ax.set_xlabel(f'{cat}-Cheater Rate Change (%) from \nControl ({control_rates[cat]:.1f}%)', 
                     fontsize=12, fontweight='bold')
        ax.set_title(title, fontweight='bold', fontsize=12, color=color)
        ax.grid(True, alpha=0.3, axis='x')
        ax.set_ylim(-0.5, len(mechanism_names) - 0.5)
        
        # Add interpretation text
        xlim = ax.get_xlim()
        if cat == 'Non':
            ax.text(xlim[0] * 0.9, len(mechanism_names) - 0.8, '← Less Honest', ha='center', va='center', 
                    fontsize=10, style='italic', color='black')
            ax.text(xlim[1] * 0.7, len(mechanism_names) - 0.8, 'More Honest →', ha='center', va='center', 
                    fontsize=10, style='italic', color='black')
        else:
            ax.text(xlim[0] * 0.7, len(mechanism_names) - 0.8, '← More Honest', ha='center', va='center', 
                    fontsize=10, style='italic', color='black')
            ax.text(xlim[1] * 0.9, len(mechanism_names) - 0.8, 'Less Honest →', ha='center', va='center', 
                    fontsize=10, style='italic', color='black')
    
    plt.suptitle('Psychological Mechanisms → Cheating Behavior', 
                 fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    plt.subplots_adjust(top=0.8)
    plt.show()

def create_mechanisms_to_outcomes_plot(pathway_results):
    """Create forest plot: Mechanisms → Performance/Experience"""
    
    mech_perf_results = pathway_results['mechanisms_to_performance']
    mech_exp_results = pathway_results['mechanisms_to_experience']
    mechanism_names = pathway_results['mechanism_names']
    control_baselines = pathway_results['control_baselines']
    
    outcomes = [
        ('Performance', mech_perf_results),
        ('Experience', mech_exp_results)
    ]
    groups = ['Non-Cheater', 'Partial Cheater', 'Full Cheater']
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 8))
    
    for idx, (outcome_name, results) in enumerate(outcomes):
        ax = axes[idx]
        
        # Colors for each group
        colors = ['#000000', '#36454F', '#818589']
        
        for j, mech_name in enumerate(mechanism_names):
            if mech_name in results:
                for i, (group, group_idx) in enumerate(zip(groups, [0, 1, 2])):
                    # Y positioning: each mechanism gets 3 positions (one per group)
                    y_pos = j * 3 + i
                    effect = results[mech_name]['by_group'][group_idx]
                    
                    mean = effect['mean']
                    hdi = effect['hdi']
                    
                    # Plot effect with CI
                    ax.plot([hdi[0], hdi[1]], [y_pos, y_pos], color=colors[i], linewidth=2, alpha=0.8)
                    ax.plot(mean, y_pos, 's', color=colors[i], markersize=8, alpha=0.8)
                    
                    # Add value label for significant effects
                    if hdi[0] > 0 or hdi[1] < 0:
                        ax.text(mean, y_pos + 0.15, f'{mean:+.3f}', ha='center', va='bottom', 
                               fontweight='bold', fontsize=9, color=colors[i])
        
        ax.axvline(0, color='red', linestyle='--', alpha=0.7, linewidth=2)
        
        # Add horizontal lines to separate mechanisms
        for j in range(1, len(mechanism_names)):
            ax.axhline(j * 3 - 0.5, color='gray', linestyle='-', alpha=0.3, linewidth=1)
        
        # Y-axis: mechanism labels at center of each group
        y_ticks = [j * 3 + 1 for j in range(len(mechanism_names))]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(mechanism_names, fontsize=12, fontweight='bold')
        ax.set_ylim(-0.5, len(mechanism_names) * 3 - 0.5)
        
        # Baselines for labels
        if outcome_name == 'Performance':
            baselines = control_baselines['performance_by_cheating']
            baseline_text = f"Non-: {baselines[0]:.1f}, Partial-: {baselines[1]:.1f}, Full: {baselines[2]:.1f}"
        else:
            baselines = control_baselines['experience_by_cheating']
            baseline_text = f"Non-: {baselines[0]:.1f}, Partial-: {baselines[1]:.1f}, Full: {baselines[2]:.1f}"
        
        ax.set_xlabel(f'{outcome_name} Change from Control\n(Baselines - {baseline_text})', 
                     fontsize=11, fontweight='bold')
        ax.set_title(f'Psychological Mechanism → {outcome_name}', fontweight='bold', fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add interpretation text
        xlim = ax.get_xlim()
        ax.text(xlim[0] * 0.8, len(mechanism_names) * 3 - 1, '← Worse', ha='center', va='center', 
                fontsize=10, style='italic', color='black')
        ax.text(xlim[1] * 0.8, len(mechanism_names) * 3 - 1, 'Better →', ha='center', va='center', 
                fontsize=10, style='italic', color='black')
    
    # Legend
    legend_elements = [plt.Line2D([0], [0], color=color, lw=3, label=group) 
                      for color, group in zip(['#000000', '#36454F', '#818589'], groups)]
    fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), 
              ncol=3, fontsize=12)
    
    plt.suptitle('Psychological Mechanisms → Performance/Experience', 
                 fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    plt.subplots_adjust(top=0.8, bottom=0.15)
    plt.show()

def print_pathway_summary(pathway_results):
    """Print pathway analysis summary tables matching original analysis"""
    
    if pathway_results is None:
        print("⚠️ No pathway results to summarize")
        return
    
    mechanism_names = pathway_results['mechanism_names']
    
    print("\n" + "="*80)
    print("PATHWAY ANALYSIS RESULTS")
    print("="*80)
    
    # Table 1: Overall Intervention → Mechanisms
    print(f"\n1. OVERALL INTERVENTION → PSYCHOLOGICAL MECHANISMS")
    print(f"{'Mechanism':<25} {'Effect Size':<20} {'95% HDI':<25}")
    print("-"*70)
    
    concept_mech_results = pathway_results['concept_to_mechanisms']
    for mech_name in mechanism_names:
        if mech_name in concept_mech_results:
            result = concept_mech_results[mech_name]
            mean = result['mean']
            hdi = result['hdi']
            effect_str = f"{mean:+.3f}"
            hdi_str = f"[{hdi[0]:+.3f}, {hdi[1]:+.3f}]"
            print(f"{mech_name:<25} {effect_str:<20} {hdi_str:<25}")
    
    # Table 2: Mechanisms → Cheating
    print(f"\n2. PSYCHOLOGICAL MECHANISMS → CHEATING BEHAVIOR")
    print(f"{'Mechanism':<20} {'Non-Cheater':<25} {'Partial Cheater':<25} {'Full Cheater':<25}")
    print("-"*95)
    
    mech_cheating_results = pathway_results['mechanisms_to_cheating']
    for mech_name in mechanism_names:
        if mech_name in mech_cheating_results:
            result = mech_cheating_results[mech_name]
            non_str = f"{result['non']['mean']:+.1f}% [{result['non']['hdi'][0]:+.1f}, {result['non']['hdi'][1]:+.1f}]"
            partial_str = f"{result['partial']['mean']:+.1f}% [{result['partial']['hdi'][0]:+.1f}, {result['partial']['hdi'][1]:+.1f}]"
            full_str = f"{result['full']['mean']:+.1f}% [{result['full']['hdi'][0]:+.1f}, {result['full']['hdi'][1]:+.1f}]"
            
            print(f"{mech_name:<20} {non_str:<25} {partial_str:<25} {full_str:<25}")
    
    # Table 3: Mechanisms → Performance
    print(f"\n3. PSYCHOLOGICAL MECHANISMS → PERFORMANCE (by Cheating Group)")
    print(f"{'Mechanism':<20} {'Group':<15} {'Mean':<8} {'95% HDI':<20}")
    print("-"*60)
    
    mech_perf_results = pathway_results['mechanisms_to_performance']
    for mech_name in mechanism_names:
        if mech_name in mech_perf_results:
            for i, group in enumerate(['Non', 'Partial', 'Full']):
                effect = mech_perf_results[mech_name]['by_group'][i]
                mean = effect['mean']
                hdi = effect['hdi']
                print(f"{mech_name:<20} {group:<15} {mean:+.3f} [{hdi[0]:+.3f}, {hdi[1]:+.3f}]")
    
    # Table 4: Mechanisms → Experience
    print(f"\n4. PSYCHOLOGICAL MECHANISMS → EXPERIENCE (by Cheating Group)")
    print(f"{'Mechanism':<20} {'Group':<15} {'Mean':<8} {'95% HDI':<20}")
    print("-"*60)
    
    mech_exp_results = pathway_results['mechanisms_to_experience']
    for mech_name in mechanism_names:
        if mech_name in mech_exp_results:
            for i, group in enumerate(['Non', 'Partial', 'Full']):
                effect = mech_exp_results[mech_name]['by_group'][i]
                mean = effect['mean']
                hdi = effect['hdi']
                print(f"{mech_name:<20} {group:<15} {mean:+.3f} [{hdi[0]:+.3f}, {hdi[1]:+.3f}]")
    
 




