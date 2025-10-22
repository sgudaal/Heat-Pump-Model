# 🔥 Heat Pump Modeling Tool (TESPy)

**Author:** Sakariye Gudaal  
**Language:** Python 3.10+  
**Main Libraries:** TESPy, CoolProp, pandas, matplotlib, numpy  

---

## 🎯 Objective  

This repository provides a **flexible heat pump modeling tool** developed using the **TESPy** library.  
The tool simulates both **design** and **off-design** conditions for a heat pump, allowing users to analyse system performance under varying heat source and sink conditions.  

The model also uses a supplied dataset to evaluate performance metrics over time — such as **Coefficient of Performance (COP)**, **Compressor Power**, and **Heat Transfer Rates**.

---

## 🧠 Model Overview  

The script models a **heat pump cycle** consisting of:

| Component | Description |
|------------|-------------|
| **Evaporator** | Absorbs heat from a low-temperature heat source |
| **Compressor** | Increases the pressure and temperature of the refrigerant |
| **Condenser** | Rejects heat to the high-temperature sink |
| **Expansion Valve** | Reduces pressure to complete the cycle |
| **Cycle Closer** | Maintains continuity of the working fluid |

The model is divided into three main parts:

### 1 Design Condition
Simulates the **optimal operation point** using predefined input parameters:  
- Heat source: 40 → 10 °C, 1000 kW  
- Heat sink: 40 → 90 °C, 1012 kW  
- Compressor isentropic efficiency: 0.85  

Key outputs:
- **COP (Coefficient of Performance)**
- **Compressor Power [kW]**
- **Evaporator Heat Transfer [kW]**
- **Condenser Heat Transfer [kW]**

---

### 2️ Off-Design Conditions  
Explores performance when system parameters deviate from the design point:
- Varying **heat source temperature** (e.g., -5 °C shift)
- Varying **thermal load** (part-load operation)

Plots are generated to show how COP and power consumption change with these parameters.

---

### 3️ Dataset-Driven Simulation  
Reads a time-series dataset (`HP_case_data.xlsx`) containing real or simulated source/sink conditions.  
For each timestep, the model:
- Updates boundary conditions
- Solves the TESPy network
- Stores key metrics for analysis

This allows evaluation of **seasonal performance** and **time-dependent COP**.

---

## ⚙️ How to Run  

### **1. Install Dependencies**
```bash
pip install tespy CoolProp pandas numpy matplotlib openpyxl
```

### **2. Run the Model**
```bash
python Heat_Pump_Model.py
```

### **3. View Results**
- Console output: Key performance metrics  
- Plots: COP, compressor power, and heat transfer vs. temperature/load/time  

---

## 📊 Key Outputs  

| Metric | Description |
|---------|-------------|
| **COP** | Coefficient of Performance = Q_cond / P_comp |
| **P_comp** | Compressor power [kW] |
| **Q_ev** | Evaporator heat absorbed [kW] |
| **Q_cd** | Condenser heat released [kW] |

The model produces graphs showing:
- COP vs. Ambient Temperature  
- COP vs. Thermal Load  
- COP and Power vs. Time (from dataset)

---

## 🧩 Parameter Definitions  

| Parameter | Description | Units |
|------------|--------------|--------|
| `T_src_in`, `T_src_out` | Source inlet/outlet temperature | °C |
| `T_snk_in`, `T_snk_out` | Sink inlet/outlet temperature | °C |
| `eta_comp` | Compressor efficiency | – |
| `Q_src`, `Q_snk` | Heat input/output | W |
| `p_amb`, `p_sink` | Source/sink pressure | bar |
| `x_g`, `x_l` | Gas/liquid saturation quality | – |

---

## 📘 Simulation Logic Summary  

1. **Define Inputs** – User sets all thermodynamic and boundary parameters.  
2. **Build TESPy Network** – Components and connections are created.  
3. **Design Simulation** – Model solves for steady-state optimal operation.  
4. **Off-Design Simulation** – Conditions are perturbed to test sensitivity.  
5. **Dataset Loop** – Model runs iteratively over measured data.  
6. **Visualisation & Output** – Key results are plotted and printed.  

---

## 📚 References  

- **TESPy Documentation:** [https://tespy.readthedocs.io](https://tespy.readthedocs.io)  
- **CoolProp:** [https://coolprop.org](https://coolprop.org)  
- **J.P. Holman. Heat Transfer, 10th edition. Mc-GrawHill Higher education, 2010.**  
- **J.Lienhard V J. Lienhard IV. A Heat Transfer Textbook, 5th edition. Phlogiston Press, 2020.**  

---

## 🧑‍💻 Author  

**Sakariye Gudaal**  
*MSc Aerospace Engineering – TU Delft*  
Focus: Performance & Propulsion 
