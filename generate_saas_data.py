import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

os.makedirs('seeds', exist_ok=True)

np.random.seed(42)

# ─────────────────────────────────────────
# CONFIG MÉTIER
# ─────────────────────────────────────────
PLANS = {
    'Essential': {'price': 0,   'commission': 0.029, 'fixed_fee': 0.30, 'weight': 0.5},
    'Business':  {'price': 49,  'commission': 0.015, 'fixed_fee': 0.15, 'weight': 0.4},
    'Custom':    {'price': 299, 'commission': 0.008, 'fixed_fee': 0.00, 'weight': 0.1},
}

# ─────────────────────────────────────────
# 1. RAW_CUSTOMERS (les boutiques e-commerce)
# ─────────────────────────────────────────
business_types = ['Mode', 'High-Tech', 'Déco', 'Sport', 'Beauté']
countries = ['France', 'Belgique', 'Suisse', 'Luxembourg']

customers = []
for i in range(1, 151):
    customers.append({
        'customer_id':  f'SHOP_{i:03}',
        'shop_name':    f'{np.random.choice(business_types)}_{i}',
        'country':      np.random.choice(countries),
        'created_at':   (datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 450))).strftime('%Y-%m-%d'),
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv('seeds/raw_customers.csv', index=False)
print(f"✅ raw_customers      : {len(df_customers)} lignes")

# ─────────────────────────────────────────
# 2. RAW_SUBSCRIPTIONS (les contrats FlowPay)
# ─────────────────────────────────────────
plan_names   = list(PLANS.keys())
plan_weights = [PLANS[p]['weight'] for p in plan_names]

subs = []
for _, row in df_customers.iterrows():
    plan   = np.random.choice(plan_names, p=plan_weights)
    status = np.random.choice(['active', 'cancelled'], p=[0.85, 0.15])

    start_dt = datetime.strptime(row['created_at'], '%Y-%m-%d')
    end_dt   = start_dt + timedelta(days=np.random.randint(60, 300)) if status == 'cancelled' else None

    subs.append({
        'subscription_id':        f'SUB_{row["customer_id"]}',
        'customer_id':            row['customer_id'],
        'plan_name':              plan,
        'monthly_fixed_fee':      PLANS[plan]['price'],   # ✅ corrigé via le dict
        'commission_rate':        PLANS[plan]['commission'],
        'per_transaction_fee':    PLANS[plan]['fixed_fee'],
        'status':                 status,
        'subscription_start_date': start_dt.strftime('%Y-%m-%d'),
        'subscription_end_date':  end_dt.strftime('%Y-%m-%d') if end_dt else None,
    })

df_subs = pd.DataFrame(subs)
df_subs.to_csv('seeds/raw_subscriptions.csv', index=False)
print(f"✅ raw_subscriptions  : {len(df_subs)} lignes")

# ─────────────────────────────────────────
# 3. RAW_TRANSACTIONS (le cœur du projet)
# ─────────────────────────────────────────

# Volume moyen de transactions par plan (par mois)
MONTHLY_TX = {'Essential': 80, 'Business': 400, 'Custom': 2000}

# Montant moyen du panier par plan (€)
AVG_BASKET = {'Essential': 45, 'Business': 120, 'Custom': 350}

PAYMENT_METHODS = ['card_visa', 'card_mastercard', 'apple_pay', 'paypal']
TX_STATUSES     = ['success', 'success', 'success', 'success', 'success',
                   'failed', 'chargeback']   # ~71% success, ~14% failed, ~14% chargeback

transactions = []
tx_id = 1

for _, sub in df_subs.iterrows():
    plan     = sub['plan_name']
    start_dt = datetime.strptime(sub['subscription_start_date'], '%Y-%m-%d')
    end_dt   = (datetime.strptime(sub['subscription_end_date'], '%Y-%m-%d')
                if pd.notna(sub['subscription_end_date'])
                else datetime(2025, 6, 30))

    # Durée en mois (arrondi, min 1)
    nb_months = max(1, round((end_dt - start_dt).days / 30))

    monthly_volume = MONTHLY_TX[plan]
    avg_basket     = AVG_BASKET[plan]

    for month_offset in range(nb_months):
        period_start = start_dt + timedelta(days=30 * month_offset)
        period_end   = period_start + timedelta(days=30)

        # Croissance organique (+2% / mois pour simuler la Negative Churn)
        growth_factor = 1 + 0.02 * month_offset
        nb_tx = max(1, int(np.random.poisson(monthly_volume * growth_factor)))

        for _ in range(nb_tx):
            tx_date   = period_start + timedelta(seconds=np.random.randint(0, 30 * 86400))
            tx_date   = min(tx_date, end_dt)
            amount    = round(max(5, np.random.normal(avg_basket, avg_basket * 0.4)), 2)
            status    = np.random.choice(TX_STATUSES)

            # FlowPay ne perçoit ses commissions que sur les transactions réussies
            if status == 'success':
                flowpay_revenue = round(
                    amount * sub['commission_rate'] + sub['per_transaction_fee'], 4
                )
                net_amount = amount
            elif status == 'chargeback':
                flowpay_revenue = round(
                    -(amount * sub['commission_rate'] + sub['per_transaction_fee']), 4
                )
                net_amount = -amount   # remboursement forcé
            else:
                flowpay_revenue = 0.0
                net_amount      = 0.0

            transactions.append({
                'transaction_id':    f'TX_{tx_id:07}',
                'customer_id':       sub['customer_id'],
                'subscription_id':   sub['subscription_id'],
                'transaction_date':  tx_date.strftime('%Y-%m-%d %H:%M:%S'),
                'amount':            amount,
                'net_amount':        net_amount,
                'currency':          'EUR',
                'payment_method':    np.random.choice(PAYMENT_METHODS),
                'status':            status,
                'flowpay_revenue':   flowpay_revenue,
                'is_chargeback':     1 if status == 'chargeback' else 0,
            })
            tx_id += 1

df_tx = pd.DataFrame(transactions)
df_tx.to_csv('seeds/raw_transactions.csv', index=False)
print(f"✅ raw_transactions   : {len(df_tx):,} lignes")

# ─────────────────────────────────────────
# RÉSUMÉ RAPIDE
# ─────────────────────────────────────────
print("\n📊 Aperçu des métriques générées :")
success_tx = df_tx[df_tx['status'] == 'success']
print(f"   GMV total         : {success_tx['amount'].sum():>14,.2f} €")
print(f"   Revenu FlowPay    : {df_tx['flowpay_revenue'].sum():>14,.2f} €")
print(f"   Taux de chargeback: {(df_tx['is_chargeback'].sum() / len(df_tx) * 100):>13.2f} %")
print(f"   Transactions/plan :")
for p in plan_names:
    n = len(df_tx[df_tx['customer_id'].isin(
        df_subs[df_subs['plan_name'] == p]['customer_id'])])
    print(f"     {p:<12}: {n:>8,} tx")

print("\n🚀 Données FlowPay générées avec succès dans seeds/")