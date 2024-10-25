Part A - Calculating loyalty points:-

import pandas as pd
# Load data from Excel sheets
user_gameplay_data = pd.read_excel('data.xlsx', sheet_name='User', parse_dates=['Datetime'])
deposit_data = pd.read_excel('data.xlsx', sheet_name='Deposit', parse_dates=['Datetime'])
withdrawal_data = pd.read_excel('data.xlsx', sheet_name='Withdrawal', parse_dates=['Datetime'])
user_gameplay_data.head()
User ID	Games Played	Datetime
0	851	1	2022-01-10
1	717	1	2022-01-10
2	456	1	2022-01-10
3	424	1	2022-01-10
4	845	1	2022-01-10
deposit_data.head()
User Id	Datetime	Amount
0	357	2022-01-10 00:03:00	2000
1	776	2022-01-10 00:03:00	2500
2	492	2022-01-10 00:06:00	5000
3	803	2022-01-10 00:07:00	5000
4	875	2022-01-10 00:09:00	1500
withdrawal_data.head()
User Id	Datetime	Amount
0	190	2022-01-10 00:03:00	5872
1	159	2022-01-10 00:16:00	9540
2	164	2022-01-10 00:24:00	815
3	946	2022-01-10 00:29:00	23000
4	763	2022-01-10 00:40:00	9473
# Slot boundaries
s1_start = pd.Timestamp('12:00:00')
s1_end = pd.Timestamp('23:59:59')
s2_start = pd.Timestamp('00:00:00')
s2_end = pd.Timestamp('11:59:59')
# Function to calculate loyalty points for a given action type
def calculate_loyalty_points(action_type, amount=None, num_deposits=None, num_withdrawals=None, games_played=None):
    if action_type == 'deposit':
        return 0.01 * amount
    elif action_type == 'withdrawal':
        return 0.005 * amount
    elif action_type == 'deposit_withdrawal_diff':
        return 0.001 * max(num_deposits - num_withdrawals, 0)
    elif action_type == 'games_played':
        return 0.2 * games_played
# Initialize dictionary to store loyalty points earned by players
loyalty_points = {}

# Loop through each player's gameplay data
for _, row in user_gameplay_data.iterrows():
    user_id = row['User ID']
    datetime = row['Datetime']
    games_played = row['Games Played']
    
    # Determine the slot
    slot = None
    if s1_start <= datetime <= s1_end:
        slot = 'S1'
    elif s2_start <= datetime <= s2_end:
        slot = 'S2'
    
    # Initialize loyalty points for the player if not already present
    if user_id not in loyalty_points:
        loyalty_points[user_id] = {'S1': 0, 'S2': 0}
    
    # Calculate loyalty points for games played
    if slot:
        loyalty_points[user_id][slot] += calculate_loyalty_points('games_played', games_played=games_played)
# Loop through deposit data to calculate loyalty points
for _, row in deposit_data.iterrows():
    user_id = row['User Id']
    amount = row['Amount']
    datetime = row['Datetime']
    
    # Determine the slot
    slot = None
    if s1_start <= datetime <= s1_end:
        slot = 'S1'
    elif s2_start <= datetime <= s2_end:
        slot = 'S2'
    
    # Calculate loyalty points for deposit
    if slot:
        loyalty_points[user_id][slot] += calculate_loyalty_points('deposit', amount=amount)
# Loop through withdrawal data to calculate loyalty points
for _, row in withdrawal_data.iterrows():
    user_id = row['User Id']
    amount = row['Amount']
    datetime = row['Datetime']
    
    # Determine the slot
    slot = None
    if s1_start <= datetime <= s1_end:
        slot = 'S1'
    elif s2_start <= datetime <= s2_end:
        slot = 'S2'
    
    # Calculate loyalty points for withdrawal
    if slot:
        loyalty_points[user_id][slot] += calculate_loyalty_points('withdrawal', amount=amount)
# Loop through deposit and withdrawal data to calculate loyalty points for deposit-withdrawal difference
for user_id in loyalty_points.keys():
    num_deposits = deposit_data[deposit_data['User Id'] == user_id].shape[0]
    num_withdrawals = withdrawal_data[withdrawal_data['User Id'] == user_id].shape[0]
    
    for slot in loyalty_points[user_id].keys():
        loyalty_points[user_id][slot] += calculate_loyalty_points('deposit_withdrawal_diff', 
                                                                  num_deposits=num_deposits, 
                                                                  num_withdrawals=num_withdrawals)
# Convert loyalty points dictionary to DataFrame
loyalty_points_df = pd.DataFrame(loyalty_points).T

# Calculate overall loyalty points earned
loyalty_points_df['Overall Loyalty Points'] = loyalty_points_df['S1'] + loyalty_points_df['S2']

# Rank players based on overall loyalty points and number of games played
loyalty_points_df['Rank'] = loyalty_points_df['Overall Loyalty Points'].rank(ascending=False, method='min')
loyalty_points_df['Games Played'] = user_gameplay_data.groupby('User ID')['Games Played'].sum()

# Calculate average deposit amount
average_deposit_amount = deposit_data['Amount'].mean()

# Calculate average deposit amount per user
average_deposit_per_user = deposit_data.groupby('User Id')['Amount'].mean().mean()

# Calculate average number of games played per user
average_games_played_per_user = user_gameplay_data.groupby('User ID')['Games Played'].sum().mean()
# Print results
print("Playerwise Loyalty points earned:")
print(loyalty_points_df[['S1', 'S2']])
print("\nOverall Loyalty points and player ranking:")
print(loyalty_points_df[['Overall Loyalty Points', 'Rank', 'Games Played']].sort_values(by='Rank'))
print("\nAverage deposit amount:", average_deposit_amount)
print("Average deposit amount per user in a month:", average_deposit_per_user)
print("Average number of games played per user:", average_games_played_per_user)
Playerwise Loyalty points earned:
        S1     S2
851  0.043  0.043
717  0.050  0.050
456  0.003  0.003
424  0.057  0.057
845  0.000  0.000
..     ...    ...
159  0.007  0.007
422  0.000  0.000
408  0.037  0.037
384  0.002  0.002
969  0.001  0.001

[1000 rows x 2 columns]

Overall Loyalty points and player ranking:
     Overall Loyalty Points   Rank  Games Played
97                    0.430    1.0           694
837                   0.280    2.0           335
618                   0.276    3.0          7084
193                   0.258    4.0             1
548                   0.258    4.0            31
..                      ...    ...           ...
265                   0.000  814.0            26
180                   0.000  814.0            12
388                   0.000  814.0             2
883                   0.000  814.0            26
634                   0.000  814.0            24

[1000 rows x 3 columns]

Average deposit amount: 5492.185399701801
Average deposit amount per user in a month: 6900.275174462214
Average number of games played per user: 355.267




Part B :-

# Calculate loyalty points for each player
loyalty_points = {}

# Loop through each player's gameplay data
for _, row in user_gameplay_data.iterrows():
    user_id = row['User ID']
    games_played = row['Games Played']
    # Calculate loyalty points for games played
    loyalty_points[user_id] = loyalty_points.get(user_id, 0) + (0.2 * games_played)

# Loop through deposit data to calculate loyalty points
for _, row in deposit_data.iterrows():
    user_id = row['User Id']
    amount = row['Amount']
    # Calculate loyalty points for deposit
    loyalty_points[user_id] = loyalty_points.get(user_id, 0) + (0.01 * amount)

# Loop through withdrawal data to calculate loyalty points
for _, row in withdrawal_data.iterrows():
    user_id = row['User Id']
    amount = row['Amount']
    # Calculate loyalty points for withdrawal
    loyalty_points[user_id] = loyalty_points.get(user_id, 0) + (0.005 * amount)
# Determine top 50 players based on loyalty points
top_50_players = sorted(loyalty_points.items(), key=lambda x: x[1], reverse=True)[:50]
# Approach 1: Weighted Distribution based on Loyalty Points
total_loyalty_points = sum(loyalty_points.values())
bonus_distribution_1 = {user_id: (loyalty_points[user_id] / total_loyalty_points) * 50000 for user_id, _ in top_50_players}
# Approach 2: Combination of Loyalty Points and Number of Games Played
games_played_dict = user_gameplay_data.groupby('User ID')['Games Played'].sum().to_dict()
combined_scores = {user_id: loyalty_points[user_id] + games_played_dict.get(user_id, 0) for user_id, _ in top_50_players}
total_combined_score = sum(combined_scores.values())
bonus_distribution_2 = {user_id: (combined_scores[user_id] / total_combined_score) * 50000 for user_id, _ in top_50_players}
# Approach 3: Equal Distribution among Top 50 Players
equal_bonus_share = 50000 / 50
bonus_distribution_3 = {user_id: equal_bonus_share for user_id, _ in top_50_players}
# Approach 4: Hybrid Approach
# Define weights for loyalty points and games played
loyalty_points_weight = 0.7
games_played_weight = 0.3
hybrid_scores = {user_id: (loyalty_points_weight * loyalty_points[user_id] + 
                           games_played_weight * games_played_dict.get(user_id, 0)) 
                 for user_id, _ in top_50_players}
total_hybrid_score = sum(hybrid_scores.values())
bonus_distribution_4 = {user_id: (hybrid_scores[user_id] / total_hybrid_score) * 50000 for user_id, _ in top_50_players}
# Approach 1: # Print bonus distributions for each approach
print("Approach 1: Weighted Distribution based on Loyalty Points")
print(bonus_distribution_1)
print("\nApproach 2: Combination of Loyalty Points and Number of Games Played")
print(bonus_distribution_2)
print("\nApproach 3: Equal Distribution among Top 50 Players")
print(bonus_distribution_3)
print("\nApproach 4: Hybrid Approach")
print(bonus_distribution_4)

Approach 1: Weighted Distribution based on Loyalty Points
{634: 2893.785406371953, 99: 816.8029090032362, 672: 785.465567257278, 212: 766.1897309088905, 740: 663.0778638968852, 566: 661.0748322177528, 714: 578.6029753650718, 421: 533.121713879155, 369: 498.331226281604, 30: 485.03928960358064, 587: 470.7322902619355, 222: 460.7228267095069, 352: 450.0834789812505, 365: 443.6826477577914, 920: 432.6631261009452, 162: 430.86148478707065, 415: 424.677057606484, 569: 424.0207700665735, 786: 417.5251973602287, 2: 415.56737928495016, 238: 401.70388743149067, 992: 401.3231957898801, 28: 366.62365311305865, 538: 355.4476095527955, 208: 339.63285732232646, 989: 337.86642049389604, 978: 324.39725339160464, 915: 322.3600526530713, 678: 320.7197652308128, 78: 315.2837785079154, 909: 312.9730527231661, 182: 305.1364307208322, 93: 304.2347472088602, 200: 288.7382159154394, 259: 285.2736803773794, 306: 285.11491505086934, 344: 284.3832139808666, 601: 280.5328096709844, 515: 272.0616440756323, 294: 263.479170180716, 681: 260.63744340719364, 950: 258.79783647176225, 675: 245.14746981204186, 663: 240.950542919956, 438: 240.71774463140508, 619: 240.57778954466633, 245: 229.72997603986195, 547: 221.26761156587042, 612: 220.96009003126073, 949: 216.12982754320066}

Approach 2: Combination of Loyalty Points and Number of Games Played
{634: 6347.623318247169, 99: 1791.9309711373419, 672: 1723.211045589233, 212: 1680.2597203040627, 740: 1454.220509056875, 566: 1463.5272980993093, 714: 1269.2775472649055, 421: 1286.931042244798, 369: 1095.5952212126451, 30: 1064.6307435230958, 587: 1087.8267600463341, 222: 1011.0799039741294, 352: 1010.6817930453026, 365: 1250.497837338067, 920: 1019.3304880713582, 162: 944.9912191942078, 415: 933.2458114964878, 569: 932.7148707805712, 786: 916.1243925298369, 2: 918.6428604303533, 238: 948.942053887129, 992: 1067.994629498705, 28: 806.7725541326599, 538: 781.6590204265641, 208: 783.1568560314092, 989: 1003.617973085719, 978: 716.9743200059081, 915: 707.511616797432, 678: 704.2173623911215, 78: 736.9517686112068, 909: 686.3969787043721, 182: 854.2654471524789, 93: 704.0183069267083, 200: 633.4792566306221, 259: 635.1155985091846, 306: 625.533689081525, 344: 623.8534490397079, 601: 617.6804590482394, 515: 627.8648329233253, 294: 578.1641650377479, 681: 572.159577482903, 950: 567.822741699294, 675: 585.9496556639424, 663: 1012.851724666886, 438: 527.9476937339281, 619: 527.7164715119573, 245: 504.00389470559276, 547: 579.6763810753829, 612: 601.3295285331958, 949: 474.0286394190411}

Approach 3: Equal Distribution among Top 50 Players
{634: 1000.0, 99: 1000.0, 672: 1000.0, 212: 1000.0, 740: 1000.0, 566: 1000.0, 714: 1000.0, 421: 1000.0, 369: 1000.0, 30: 1000.0, 587: 1000.0, 222: 1000.0, 352: 1000.0, 365: 1000.0, 920: 1000.0, 162: 1000.0, 415: 1000.0, 569: 1000.0, 786: 1000.0, 2: 1000.0, 238: 1000.0, 992: 1000.0, 28: 1000.0, 538: 1000.0, 208: 1000.0, 989: 1000.0, 978: 1000.0, 915: 1000.0, 678: 1000.0, 78: 1000.0, 909: 1000.0, 182: 1000.0, 93: 1000.0, 200: 1000.0, 259: 1000.0, 306: 1000.0, 344: 1000.0, 601: 1000.0, 515: 1000.0, 294: 1000.0, 681: 1000.0, 950: 1000.0, 675: 1000.0, 663: 1000.0, 438: 1000.0, 619: 1000.0, 245: 1000.0, 547: 1000.0, 612: 1000.0, 949: 1000.0}

Approach 4: Hybrid Approach
{634: 6510.8251803267, 99: 1837.8596967729077, 672: 1767.3614054501181, 212: 1723.697883908102, 740: 1491.7647575535614, 566: 1493.2816662470927, 714: 1301.85828230921, 421: 1251.1528458929142, 369: 1122.3058971461276, 30: 1091.6049540983406, 587: 1083.4114509050796, 222: 1036.801407295499, 352: 1022.9492928232232, 365: 1120.1589536180945, 920: 1004.3576082024404, 162: 969.3573983997313, 415: 956.243190043043, 569: 955.1660855957805, 786: 939.5216994939424, 2: 938.1121629341783, 238: 933.6117952716935, 992: 985.4653259757567, 28: 826.0089445224635, 538: 800.6004604669486, 208: 780.9288428974454, 989: 875.5864743868843, 978: 732.2452304152911, 915: 725.4659779508905, 678: 721.9089987157749, 78: 729.3130172374548, 909: 704.1155061141978, 182: 767.8468018122358, 93: 700.6296831020288, 200: 649.6952489892839, 259: 645.9609615353385, 306: 641.5440623962629, 344: 639.8647089817576, 601: 632.2009120124707, 515: 625.7887546686316, 294: 592.9043194171102, 681: 586.6112364385598, 950: 582.339644629273, 675: 572.7615622420514, 663: 755.0590358002693, 438: 541.5657978216019, 619: 541.2842232745265, 245: 516.9136328715563, 547: 539.3054369311925, 612: 548.4301826337983, 949: 486.2514014711711}



Part C :- 
Evaluating the Fairness of the Loyalty Point Formula:-

To ensure the loyalty point formula is fair, it’s essential that the system:-

Transparency: Provides clear, understandable rules, so players know how their actions translate to loyalty points.
Equity: Treats all players equally, avoiding favoritism of specific actions or behaviors unless there’s a solid reason (e.g., promoting positive engagement).
Feedback Mechanism: Allows players to share their thoughts or concerns about the loyalty system, enabling adjustments based on user experience and preferences.

Suggestions to Make the Loyalty Point Formula More Robust:-

Collect Regular Feedback: Continuously gather insights from players on their experiences with the loyalty system. This can reveal any perceived biases or areas for improvement.
Behavioral Analysis: Use player data to identify trends, such as daily activity levels, spending patterns, and frequency of deposits. This analysis can inform adjustments that better reward sustained engagement and fair participation.
Gamification Enhancements: Incorporate elements like achievement levels, badges, and challenges to make the loyalty system more engaging. These features can encourage ongoing participation by offering a more interactive, rewarding experience.
