
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

st.set_page_config(layout='wide')

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

st.title("LazyTrade Leaderboard")
st.subheader('Leaderboard')

col1, col2, col3 = st.columns([1,1,1])

col2.dataframe(disp_df.style.format(formatter={'Avg PnL': "{:.2f}%", 'Total PnL': formatfunc}), width=800, height=1000)

# st.table(disp_df.style.format(formatter={'Avg PnL': "{:.2f}%", 'Total PnL': formatfunc}))

st.subheader('Historical Signals')

users = st.multiselect('Choose users to track ', tuple(['@binance', '@CoinDesk', '@CryptoKaleo', '@cz_binance', '@TheCryptoDog', 
                                                        '@thescalpingpro', '@Whale_Sniper', '@WhaleTrades']), default=['@CoinDesk'])

for user in users:
    coin_list = ['1INCH','ADA','ATOM','AXS','BNB','BTC','DOGE','DOT','ETH','LINK','LTC','LUNA','RUNE','SOL','SUSHI''UNI','XRP']
    
    all_coins = [i[len(user):].split('_')[0] for i in list(filter(lambda x : x.startswith(user[1:]), images))]
    coin_subset = [i for i in coin_list if i in all_coins]
        
    coins = st.multiselect('Choose coins to plot', coin_subset, default=['LTC'])

    for coin in coins:
        st.write('User: %s\n\nCoin: %s' % (user, coin))
#         st.image('images/%s_%s_BTC.png' % (user[1:], coin))
        
        HtmlFile = open('images/%s_%s_BTC.html' % (user[1:], coin), 'r', encoding='utf-8')
        source_code_2 = HtmlFile.read()
        components.html(source_code_2, height=700)
