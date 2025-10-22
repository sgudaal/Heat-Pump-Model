# Case: Heat Pump Modeling Tool
# Author: Sakariye Gudaal

#==============================================================================
# Inputs
#==============================================================================

# Design Inputs
T_src_in = 40.0 # Heat Source Temperature [degC]
T_src_out = 10.0 # Evaporator Temperature [degC]
T_snk_in = 40.0 # Heat Sink Temperature [degC]
T_snk_out = 90.0 # Condensation Temperature [degC]
eta_comp = 0.85 # Compressor Efficiency [-]
Q_src = 1000.0 * 1e3 # Evaporator Heat [W] 
Q_snk = -1012.0 * 1e3 # Condenser Heat [W]


# Assumed Design Inputs
p_amb = 1.0 # Ambient Air Pressure [bar]
p_sink = 1.0 # Heating Source Pressure [bar]
x_g = 1.0 # Saturated gas stream [-]
x_l = 0.0 # Saturated liquid stream [-]
pr_cd1 = 1.0  # Condenser Pressure Ratio 1 [-]
pr_ev1 = 1.0 # Evaporator Pressure Ratio 1 [-]
pr_cd2 = 1.0  # Condenser Pressure Ratio 2 [-]
pr_ev2 = 1.0 # Evaporator Pressure Ratio 2 [-]
dt = 100 # Time Step [-]

#==============================================================================
# Setup TESPy Model
#==============================================================================

# Imports
from tespy.components import(Condenser, HeatExchanger, CycleCloser, 
                             Compressor, Valve, Source, Sink)

from tespy.connections import Connection, Ref
from tespy.networks import Network

# Setup Network
wf = "Water" # Working Fluid
nw = Network(p_unit="bar", T_unit="C", iterinfo=False) # Network

# Build Components
cp = Compressor("compressor")
ev = HeatExchanger("evaporator")
cd = Condenser("condenser")
va = Valve("expansion valve")
cc = CycleCloser("cycle closer")

# Source and Sink
so1 = Source("ambient air source")
si1 = Sink("ambient air sink")
so2 = Source("heating source")
si2 = Sink("heating sink")

# Build Connections
c0 = Connection(va, "out1", cc, "in1", label="0")
c1 = Connection(cc, "out1", ev, "in2", label="1")
c2 = Connection(ev, "out2", cp, "in1", label="2")
c3 = Connection(cp, "out1", cd, "in1", label="3")
c4 = Connection(cd, "out1", va, "in1", label="4")

# Source and Sink Connections
c11 = Connection(so1, "out1", ev, "in1", label="11")
c12 = Connection(ev, "out1", si1, "in1", label="12")

c21 = Connection(so2, "out1", cd, "in2", label="21")
c22 = Connection(cd, "out2", si2, "in1", label="22")

# Add Connections to Network
nw.add_conns(c0, c1, c2, c3, c4)
nw.add_conns(c11, c12, c21, c22)

#==============================================================================
# Design Conditon 
#==============================================================================

# Set Optimal Operation at Specified Parameters 
c2.set_attr(T=T_src_out)
c4.set_attr(T=T_snk_out)
cp.set_attr(eta_s=eta_comp)
cd.set_attr(Q=Q_snk)

# Set Fluid's State at the Evaporator's and Condenser's Outlet and Pressure 
# Values at the Inlets
c2.set_attr(fluid={wf: 1}, x=x_g)
c11.set_attr(fluid={"air": 1}, p=p_amb, T=T_src_in)
c12.set_attr(T=Ref(c11, 1, -2))
c21.set_attr(fluid={"Water": 1}, p=p_sink, T=T_snk_in)
c22.set_attr(T=T_snk_out)
cd.set_attr(pr1=pr_cd1, pr2=pr_cd2)
ev.set_attr(pr1=pr_ev1, pr2=pr_ev2)

# Finalise Specification Values
ev.set_attr(ttd_u=5)
c2.set_attr(T=None)
cd.set_attr(ttd_u=5)
c4.set_attr(T=None)

# Run Model
nw.solve("design") # Solve Model
nw.print_results() # Print Results
nw.save("design-state") # Save Model with Design Conditions

# Model Outputs
COP = abs(cd.Q.val) / cp.P.val # Coefficient of Performance [-]
P_comp = cp.P.val * 1e-3 # Compressor Power [kW]
Q_ev = abs(ev.Q.val) * 1e-3 # Evaporator Heat Transfer [kW]
Q_cd = abs(cd.Q.val) * 1e-3 # Condensor Heat Transfer [kW]

Outputs_des = [COP, P_comp, Q_ev, Q_cd] # Collect Model Outputs
print(Outputs_des)

#==============================================================================
# Off-Design Conditon 
#==============================================================================

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Influence of Heat Source Temperature
T_range = np.linspace(T_src_in-5,
                      T_src_in,11) # Heat Source Temperature Range [degC]
COP = [] # Coefficient of Performance [-]
P_comp = [] # Compressor Power [kW]
Q_ev = [] # Evaporator Heat Transfer [kW]
Q_cd = [] # Condensor Heat Transfer [kW]

for i in T_range:
    c11.set_attr(T=i) # Set Heat Source Temperature Range [degC]
    nw.solve("offdesign", design_path="design-state") # Solve Model
    
    COP= np.append(COP,(abs(cd.Q.val) / cp.P.val)) # Coefficient of Performance [-]
    P_comp = np.append(P_comp,cp.P.val * 1e-3) # Compressor Power [kW]
    Q_ev = np.append(Q_ev,ev.Q.val * 1e-3) # Evaporator Heat Transfer [kW]
    Q_cd = np.append(Q_cd,cd.Q.val * 1e-3) # Condensor Heat Transfer [kW]

# Plots of Outputs against Ambient Temperature
fig, ax = plt.subplots(4)

ax[0].plot(T_range,COP)
ax[1].plot(T_range,P_comp)
ax[2].plot(T_range,abs(Q_ev))
ax[3].plot(T_range,abs(Q_cd))

ax[0].set_ylabel("COP [-]")
ax[1].set_ylabel("Compressor Power [W]")
ax[2].set_ylabel("Evaporator Heat Transfer [W]")
ax[3].set_ylabel("Condenser Heat Transfer [W]")

ax[3].set_xlabel("Ambient Air Temperature [degC]")

ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[3].grid()

# plt.close()

# Influence of Thermal Load
Q_range = np.linspace(1e-3,1.0,11) * Q_snk # Heat Range [W]
COP = [] # Coefficient of Performance [-]
P_comp = [] # Compressor Power [kW]
Q_ev = [] # Evaporator Heat Transfer [kW]
Q_cd = [] # Condensor Heat Transfer [kW]

for i in Q_range:
    cd.set_attr(Q=i) # Reduced Thermal Load [W]
    nw.solve("offdesign", design_path="design-state") # Solve Model
    
    COP= np.append(COP,(abs(cd.Q.val) / cp.P.val)) # Coefficient of Performance [-]
    P_comp = np.append(P_comp,cp.P.val * 1e-3) # Compressor Power [kW]
    Q_ev = np.append(Q_ev,ev.Q.val * 1e-3) # Evaporator Heat Transfer [kW]
    Q_cd = np.append(Q_cd,cd.Q.val * 1e-3) # Condensor Heat Transfer [kW]

# Plot Reuced Thermal Load
fig, ax = plt.subplots(4)

ax[0].plot(np.abs(Q_range),COP)
ax[1].plot(np.abs(Q_range),P_comp)
ax[2].plot(np.abs(Q_range),abs(Q_ev))
ax[3].plot(np.abs(Q_range),abs(Q_cd))

ax[0].set_ylabel("COP [-]")
ax[1].set_ylabel("Compressor Power [W]")
ax[2].set_ylabel("Evaporator Heat Transfer [W]")
ax[3].set_ylabel("Condenser Heat Transfer [W]")

ax[3].set_xlabel("Heat Production [W]")

ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[3].grid()

# plt.close()

#==============================================================================
# Dataset
#==============================================================================

# Imports
import pandas as pd

# Read Excel File and Extract Data
file_name = [r"C:\Users\sakar\Downloads\Work\HeatPumpModel\HP_case_data.xlsx"]
src_data = pd.read_excel(file_name[0],engine="openpyxl",sheet_name="Heat source")
snk_data = pd.read_excel(file_name[0],engine="openpyxl",sheet_name="Heat sink")

# Heat Source Data 
[temp_in_src,temp_out_src,p_src,m_src] = [src_data["T_in[degC"].tolist(),
                                          src_data["T_out[degC]"].tolist(),
                                          src_data["P[bar]"].tolist(),
                                          src_data["flow[kg/s]"].tolist()]

# Heat Sink Data
[temp_in_snk,temp_out_snk,p_snk,e_snk] = [snk_data["T_in[degC"].tolist(),
                                          snk_data["T_out[degC]"].tolist(),
                                          snk_data["P[bar]"].tolist(),
                                          snk_data["Energy[kWh]"].tolist()]

COP = [] # Coefficient of Performance [-]
P_comp = [] # Compressor Power [kW]
Q_ev = [] # Evaporator Heat Transfer [kW]
Q_cd = [] # Condensor Heat Transfer [kW]

time = np.linspace(1,len(temp_in_src)+1,dt) # Measurement time [hr]

for i in np.linspace(0,len(temp_in_src)-1,dt).astype(int):
    # Set Optimal Operation at Specified Parameters 
    c2.set_attr(T=temp_out_src[i])
    c4.set_attr(T=temp_out_snk[i])
    cp.set_attr(eta_s=eta_comp)
    cd.set_attr(Q=-e_snk[i]*1e3)
    
    # Set Fluid's State at the Evaporator's and Condenser's Outlet and Pressure
    # Values at the Inlets
    c2.set_attr(fluid={wf: 1}, x=x_g)
    c11.set_attr(fluid={"air": 1}, p=p_src[i], T=temp_in_src[i])
    c12.set_attr(T=Ref(c11, 1, -2))
    c21.set_attr(fluid={"Water": 1}, p=p_snk[i], T=temp_in_snk[i])
    c22.set_attr(T=temp_out_snk[i])
    cd.set_attr(pr1=pr_cd1, pr2=pr_cd2)
    ev.set_attr(pr1=pr_ev1, pr2=pr_ev2)
    
    # Finalise Specification Values
    ev.set_attr(ttd_u=5)
    c2.set_attr(T=None)
    cd.set_attr(ttd_u=5)
    c4.set_attr(T=None)
    
    # Run Model
    nw.solve("design") # Solve Model
    
    # Model Outputs
    COP= np.append(COP,(abs(cd.Q.val) / cp.P.val)) # Coefficient of Performance [-]
    P_comp = np.append(P_comp,cp.P.val * 1e-3) # Compressor Power [kW]
    Q_ev = np.append(Q_ev,abs(ev.Q.val) * 1e-3) # Evaporator Heat Transfer [kW]
    Q_cd = np.append(Q_cd,abs(cd.Q.val) * 1e-3) # Condensor Heat Transfer [kW]


# Plot Reuced Thermal Load
fig, ax = plt.subplots(4)

ax[0].plot(time,COP)
ax[1].plot(time,P_comp)
ax[2].plot(time,abs(Q_ev))
ax[3].plot(time,abs(Q_cd))

ax[0].set_ylabel("COP [-]")
ax[1].set_ylabel("Compressor Power [W]")
ax[2].set_ylabel("Evaporator Heat Transfer [W]")
ax[3].set_ylabel("Condenser Heat Transfer [W]")

ax[3].set_xlabel("Measurement Time [hr]")

ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[3].grid()

# plt.close()














