def gantt_plot(order, tasks, start, end):
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    import matplotlib.dates as mdates

    data = {
        'Order': order,
        'Task': tasks,
        'Start': start,
        'End': end,
    }
    df = pd.DataFrame(data)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])

    # Create the Gantt chart using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))

    # --- Sort DataFrame by 'Order' column for correct plotting ---
    df['Order'] = df['Order'].astype(str)  # Ensure 'Order' is treated as string
    df = df.sort_values(by='Order', ascending=False)  # Sort in descending order

    # --- Calculate y_positions to group tasks and subtasks ---
    y_positions = {}
    current_position = 0
    for _, row in df.iterrows():
        task_order = row['Order']
        if '.' in task_order:
            parent_order = '.'.join(task_order.split('.')[:-1])
            if parent_order in y_positions:
                y_positions[task_order] = y_positions[parent_order] + 0.25
            else:
                y_positions[task_order] = current_position
                current_position += 1
        else:
            y_positions[task_order] = current_position
            current_position += 1

    for i, row in df.iterrows():
        ax.barh(y_positions[row['Order']], (row['End'] - row['Start']).days, left=row['Start'], height=0.2, color='gray')

        # Check for subtasks (assuming subtasks have '.' in their 'Order')
        if '.' in row['Order']:
            parent_order = '.'.join(row['Order'].split('.')[:-1])  # Get parent order
            parent_index = y_positions[parent_order]  # Find parent index
            ax.plot([row['Start'], row['Start']], [parent_index + 0.15, y_positions[row['Order']] + 0.15],
                    color='black', linewidth=1)

    # --- Seaborn Styling ---
    sns.set_theme(style="whitegrid")
    sns.despine()

    # Customize the chart
    ax.set_xlabel('Date')
    ax.set_ylabel('Tasks')
    plt.title('Project Time line')

    # --- Format x-axis for date ---
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    # Set y-tick positions and labels
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(df['Task'])  # Use 'Task' column for labels

    plt.tight_layout()
    plt.show()
