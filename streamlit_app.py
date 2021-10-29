# %%writefile leaderboard2.py


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

st.set_page_config(layout='wide')
st.config.get_option("server.enableCORS")


def formatfunc(*args, **kwargs):
    value = args[0]
    if value >= 0:
        return '${:,.2f}'.format(value)
    else:
        return '-${:,.2f}'.format(abs(value))

df = pd.read_csv('anon_trades_26_10_21.csv', error_bad_lines=False)
my_df = df[df.trade_time.str.startswith('2')]
closed = my_df.dropna(subset=['buy_timestamp'])
closed.twitter_screen_name = '@'+closed.twitter_screen_name
mean_group = closed.groupby('twitter_screen_name')['twitter_screen_name', 'percent_pnl'].agg('mean')
sum_group  = closed.groupby('twitter_screen_name')['twitter_screen_name', 'dollar_pnl'].agg('sum')

disp_df = mean_group.join(sum_group)
disp_df.columns = ['Avg PnL', 'Total PnL']
disp_df.index.name = 'Twitter Handle'

images = os.listdir('images')

# st.title("Leaderboard")
st.subheader('Crypto Twitter Leaderboard')

col1, col2, col3 = st.columns([1,1,1])

col2.dataframe(disp_df.style.format(formatter={'Avg PnL': "{:.2f}%", 'Total PnL': formatfunc}), width=800, height=1000)


st.subheader('Historical Signals')
all_users = sorted(set(['@'+'_'.join(i.split('_')[:-2]) for i in images if i.endswith('USDT.html')]),key=lambda x: x.lower())
all_users = tuple([i for i in all_users if i not in ['@ArbitrageDaddy', '@JPottuy']])

users = st.multiselect('Choose users to track ', all_users, default=['@elonmusk'])

for user in users:
#     coin_list = ['1INCH','ADA','ATOM','AXS','BNB','BTC','DOGE','DOT','ETH','LINK','LTC','LUNA','RUNE','SOL','SUSHI''UNI','XRP']

    anti_coins = ['OMG','OG','HNT','ICX','MKR','CVC']
    
    all_coins = sorted([i[len(user):].split('_')[0] for i in list(filter(lambda x : x.startswith(user[1:]) and x.endswith('USDT.html'), images))])
    all_coins = [i for i in all_coins if i not in anti_coins]
    coins = st.multiselect('Choose coins to plot', all_coins, default=['BTC' if 'BTC' in all_coins else all_coins[0]])

    for coin in coins:
        _, mid, _ = st.columns([1,1,1])
        mid.subheader('%s %s' % (user, coin))
#         st.image('images/%s_%s_BTC.png' % (user[1:], coin))
        
        HtmlFile = open('images/%s_%s_USDT.html' % (user[1:], coin), 'r', encoding='utf-8')
        source_code_2 = HtmlFile.read()
        components.html(source_code_2, height=700)
