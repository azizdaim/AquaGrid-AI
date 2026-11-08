"""Optional live dashboard: pip install -r requirements.txt && streamlit run app.py"""
import streamlit as st
import plotly.graph_objects as go

from aquagrid import SCENARIOS, run_scenario

st.set_page_config(page_title='AquaGrid AI | Live Simulation', page_icon='🌊', layout='wide')
st.markdown('''<style>
.stApp{background:#071525;color:#e8f7f8}
.block-container{padding-top:2rem;max-width:1450px}
[data-testid="stMetric"]{border:1px solid #22485a;border-radius:14px;padding:14px 18px;background:#102a3d}
h1,h2,h3{color:#e8f7f8!important}
</style>''', unsafe_allow_html=True)

st.caption('CS3081  /  MILESTONE 01  /  LIVE PYTHON ENGINE')
st.title('🌊 AquaGrid AI')
st.write('**Water distribution under pressure.** Explore how a simple multi-agent system responds to simulated crises.')

scenario = st.selectbox('Select an operating scenario', list(SCENARIOS),
                        format_func=lambda k: SCENARIOS[k]['label'])
result = run_scenario(scenario)  # runs the real Python engine on each rerun
m = result['metrics']
st.info(result['description'])

cols = st.columns(4)
cols[0].metric('Demand served', f"{m['satisfaction_pct']}%")
cols[1].metric('Water delivered', f"{m['delivered']} units")
cols[2].metric('Hospital coverage', f"{m['hospital_satisfaction_pct']}%")
cols[3].metric('Broken pipelines', str(m['failed_pipes']))

left, right = st.columns([1.65, 1])
with left:
    st.subheader('City network and pipe utilization')
    fig = go.Figure()
    nodes = {n['id']: n for n in result['nodes']}
    for p in result['pipes']:
        a, b = nodes[p['a']], nodes[p['b']]
        col = '#ff788a' if not p['active'] else '#52dbca' if p['used'] else '#28465c'
        fig.add_trace(go.Scatter(
            x=[a['x'], b['x']], y=[a['y'], b['y']], mode='lines',
            line=dict(color=col, width=2 + (4 * p['used'] / p['capacity'] if p['active'] else 1),
                      dash='dash' if not p['active'] else 'solid'),
            hoverinfo='text', text=[f"{p['a']} → {p['b']} | {p['used']}/{p['capacity']} units"] * 2,
            showlegend=False,
        ))
    groups = {
        'reservoir': ('#6bbcf0', 21),
        'junction': ('#7796a9', 11),
        'district': ('#54e0cb', 19),
    }
    for kind, (color, size) in groups.items():
        group = [n for n in result['nodes'] if n['kind'] == kind]
        fig.add_trace(go.Scatter(
            x=[n['x'] for n in group], y=[n['y'] for n in group], mode='markers+text',
            marker=dict(color=color, size=size, line=dict(color='#09263a', width=2)),
            text=[n['label'] for n in group], textposition='top center',
            textfont=dict(color='#ecf6fb', size=11), hoverinfo='text',
            hovertext=[n['label'] for n in group], showlegend=False,
        ))
    fig.update_layout(
        height=530, plot_bgcolor='#0c2131', paper_bgcolor='#0c2131',
        font=dict(color='#d9edef'), margin=dict(l=15, r=15, t=30, b=20),
        xaxis=dict(range=[-1, 110], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-7, 108], showgrid=False, zeroline=False, visible=False),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption('Green: used pipelines · Muted: unused pipelines · Red dashed: failed pipelines')
with right:
    st.subheader('District allocation results')
    st.dataframe([
        {'District': d['label'], 'Demand': d['demand'], 'Received': d['delivered'],
         'Service (%)': d['satisfaction_pct']}
        for d in result['districts']
    ], hide_index=True, use_container_width=True)
    st.progress(m['satisfaction_pct'] / 100, text=f"Overall coverage: {m['satisfaction_pct']}%")
    st.write(f"**Unmet demand:** {m['unmet']} units")
    st.write(f"**Dispatches:** {m['transfers']} transfers")

with st.expander('Inspect individual agent decisions'):
    for line in result['decision_log'][:40]:
        st.write('• ' + line)

st.caption('Research prototype: artificial city data, one allocation cycle. This is not a physically realistic hydraulic model or a production water control system.')
