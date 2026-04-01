import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configuration des dossiers
os.makedirs('seeds', exist_ok=True)

# 1. Générer les Clients (Les Boutiques E-commerce)
business_types = ['Mode', 'High-Tech', 'Déco', 'Sport', 'Beauté']
countries = ['France', 'Belgique', 'Suisse', 'Luxembourg']

customers = []
for i in range(1, 151): # 150 boutiques pour plus de volume
    customers.append({
        'customer_id': f'SHOP_{i:03}',
        'shop_name': f'{np.random.choice(business_types)}_{i}',
        'country': np.random.choice(countries),
        'created_at': (datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 450))).strftime('%Y-%m-%d')
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv('seeds/raw_customers.csv', index=False)

# 2. Générer les Abonnements (Leurs contrats FlowPay)
subs = []
plans = {
    'Essential': {'price': 0, 'weight': 0.5},   # 50% des clients
    'Business': {'price': 49, 'weight(commission)': 0.4},  # 40% des clients
    'Custom': {'price': 299, 'weight': 0.1}    # 10% des clients
}

for _, row in df_customers.iterrows():
    plan = np.random.choice(['Essential', 'Business', 'Custom'], p=[0.5, 0.4, 0.1])
    status = np.random.choice(['active', 'cancelled'], p=[0.85, 0.15])
    
    start_dt = datetime.strptime(row['created_at'], '%Y-%m-%d')
    end_dt = start_dt + timedelta(days=np.random.randint(60, 300)) if status == 'cancelled' else None
    
    subs.append({
        'subscription_id': f'SUB_{row["customer_id"]}',
        'customer_id': row['customer_id'],
        'plan_name': plan,
        'monthly_fixed_fee': 29 if plan == 'Business' else (299 if plan == 'Custom' else 0),
        'status': status,
        'subscription_start_date': start_dt.strftime('%Y-%m-%d'),
        'subscription_end_date': end_dt.strftime('%Y-%m-%d') if end_dt else None
    })

df_subs = pd.DataFrame(subs)
df_subs.to_csv('seeds/raw_subscriptions.csv', index=False)

print("🚀 Données FinTech FlowPay générées avec succès !")