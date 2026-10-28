import streamlit as st
import pandas as pd
from datetime import date
st.set_page_config(page_title='Options Hunter',page_icon='🎯',layout='wide')
st.title('🎯 Options Hunter')
st.caption('Automatic rule-based PAPER simulation • synthetic option quotes • no brokerage connection')
if 'accounts' not in st.session_state:
 st.session_state.accounts={'Aggressive':{'cash':100.,'trades':[]},'Balanced':{'cash':100.,'trades':[]}}
if 'tick' not in st.session_state: st.session_state.tick=0
if 'running' not in st.session_state: st.session_state.running=False
st.warning('Demo uses synthetic market prices, not real option quotes. Returns are not forecasts. No real orders are placed.')
col1,col2=st.columns(2)
for col,name in [(col1,'Aggressive'),(col2,'Balanced')]:
 a=st.session_state.accounts[name]
 with col:
  st.subheader(name)
  st.metric('Simulated cash',f"${a['cash']:.2f}")
  st.metric('Completed paper trades',len(a['trades']))
  if a['trades']: st.dataframe(pd.DataFrame(a['trades']),hide_index=True,use_container_width=True)
st.divider()
st.write('Each click runs one **synthetic trading cycle** for both accounts. The system automatically chooses and settles a fictional long option under its rules. This is a software demonstration, not a backtest or live trading.')
if st.button('Run next automatic paper cycle',type='primary'):
 import random
 rng=random.Random(7000+st.session_state.tick)
 for name in ['Aggressive','Balanced']:
  a=st.session_state.accounts[name]
  budget= min(a['cash'],25 if name=='Aggressive' else 15)
  if budget<1: continue
  premium=round(budget,2)
  # Synthetic outcomes, not empirical return assumptions
  multiplier=rng.choice([0,0,0.2,0.5,1.5,3.0,6.0]) if name=='Aggressive' else rng.choice([0,0.5,0.7,0.9,1.1,1.3,1.6])
  proceeds=round(premium*multiplier,2)
  a['cash']=round(a['cash']-premium+proceeds,2)
  a['trades'].append({'Cycle':st.session_state.tick+1,'Contract':'Synthetic CALL' if rng.random()>.5 else 'Synthetic PUT','Premium':premium,'Exit value':proceeds,'P/L':round(proceeds-premium,2)})
 st.session_state.tick+=1
 st.rerun()
if st.button('Reset both accounts'):
 st.session_state.accounts={'Aggressive':{'cash':100.,'trades':[]},'Balanced':{'cash':100.,'trades':[]}}
 st.session_state.tick=0
 st.rerun()
st.caption('Next production milestones: licensed delayed/live option chains, realistic bid-ask execution, expiration handling, historical replay, and scheduled unattended paper execution.')
