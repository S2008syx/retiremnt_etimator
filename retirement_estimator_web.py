#口令：streamlit run ~/PycharmProjects/PythonProject7/.venv/bin/web1.py
import streamlit as st
import matplotlib.pyplot as plt

# 【一、输入参数】
st.title("退休资产模拟器（sibo_song)")

store = st.number_input("每年给401k资金(退休前给)(没有给就是0)", value=30000)
prin = st.number_input("退休时非401k资产总额", value=5000000)
spend = st.number_input("每年退休生活支出", value=200000)
portion = st.slider("每年使用多少比例的401k", 0.0, 1.0, 0.5)
interest = st.number_input("投资年收益率(401k和本金投资)(税后)", value=1.06)
inflation = st.number_input("年通股率（你每年的支出要增长）", value=1.03)

# 【二、Ё累积阶段】
retire = 0
GroR = interest
for _ in range(30):
    retire = (retire + store) * GroR

# 【三、退休模拟】
x = 1
totalP = 0
prin_balance = prin
retire_balance = retire
retire_list = []
totalP_list = []
list_tax = []

def get_tax_rate(retire_spend):
    if 0 <= retire_spend <= 11925:
        return 1 - 0.10
    elif 11926 <= retire_spend <= 48475:
        return 1 - ((11925 / retire_spend) * 0.10 + (1 - 11925 / retire_spend) * 0.12)
    elif 48476 <= retire_spend <= 103350:
        return 1 - ((48475 / retire_spend) * 0.108 + (1 - 48475 / retire_spend) * 0.22)
    elif 103351 <= retire_spend <= 197300:
        return 1 - ((103350 / retire_spend) * 0.1708 + (1 - 103350 / retire_spend) * 0.24)
    elif 197301 <= retire_spend <= 250525:
        return 1 - ((197300 / retire_spend) * 0.2037 + (1 - 197300 / retire_spend) * 0.32)
    elif 250526 <= retire_spend <= 626350:
        return 1 - ((250255 / retire_spend) * 0.2248 + (1 - 250255 / retire_spend) * 0.35)
    elif retire_spend > 626350:
        return 1 - ((626350 / retire_spend) * 0.3014 + (1 - 626350 / retire_spend) * 0.37)
    else:
        raise ValueError("retire_spend 不在合理区间")

while x < 51:
    retire_spend = spend * (inflation ** x) * portion
    tax = get_tax_rate(retire_spend)
    list_tax.append(tax)

    prin_balance = prin_balance * interest - spend * (inflation ** x) * (1 - portion)
    retire_balance = retire_balance * interest - retire_spend / tax
    totalP = prin_balance + retire_balance

    retire_list.append(retire_balance)
    totalP_list.append(totalP)

    if retire_balance <= 0:
        totalP -= (1 - list_tax[-1]) * retire_list[-1]
        break
    x += 1

# 【四、401k耗尽后，仅用本金模拟】
while x < 51:
    totalP = totalP * interest - spend * (inflation ** x)
    totalP_list.append(totalP)
    if totalP <= 0:
        break
    x += 1

# 【五、图表显示】
fig, ax = plt.subplots()
ax.plot(range(1, len(totalP_list) + 1), totalP_list, label="Total Assets ($)")
ax.set_title("Total Retirement Asset Over Time")
ax.set_xlabel("Years After Retirement")
ax.set_ylabel("Total Assets ($)")
ax.legend()
st.pyplot(fig)

st.success("本模拟器默认州税为0，并且在401k部分里以结合取出时的分段税率")
